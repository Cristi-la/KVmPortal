from django_tenants.middleware.main import TenantMainMiddleware
from django.http import Http404, HttpResponse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils.timezone import now
from django.urls import reverse
from django.db import connection

class ServiceUnavailable(HttpResponse):
    status_code = 503


class TenantMiddleware(TenantMainMiddleware):
    paths_to_ignore = ['/401','/404', '/500', '/503']

    """
    Field is_active can be used to temporary disable tenant and
    block access to their site. Modifying get_tenant method from
    TenantMiddleware allows us to check if tenant should be available
    """
    def process_request(self, request):
        super().process_request(request)

        tenant = connection.tenant
        redired_path = None

        if tenant.type == 'public':
            return
        
        if tenant.enabled_until and tenant.enabled_until < now().date():
            redired_path = "/401"

        if not tenant.is_active:
            redired_path = "/404"
        
        if tenant.on_maintenance:
            redired_path = "/503"

        if redired_path and request.path not in redired_path:
            return HttpResponseRedirect(redired_path)