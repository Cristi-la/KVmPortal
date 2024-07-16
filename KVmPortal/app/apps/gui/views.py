from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.conf import settings


class HomeView(TemplateView):
    template_name = 'home.html'


def handler404(request, exception):
    response = render(request, settings.ERROR_TEMPLATE)
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, settings.ERROR_TEMPLATE)
    response.status_code = 500
    return response


def handler403(request, exception):
    response = render(request, settings.ERROR_TEMPLATE)
    response.status_code = 403
    return response


def handler400(request, exception):
    response = render(request, settings.ERROR_TEMPLATE)
    response.status_code = 400
    return response
