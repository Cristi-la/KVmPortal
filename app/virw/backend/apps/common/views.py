from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpRequest,  Http404
from apps.common.tasks import my_task, my_shared_task
from apps.kvm.tasks import simple

class DebugView(TemplateView):
    template_name = "debug.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        simple.delay()
        if not settings.DEBUG:
            raise Http404("This view is only available in debug mode.")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        # collect_data.delay(12)
        return super().get(request, *args, **kwargs)





