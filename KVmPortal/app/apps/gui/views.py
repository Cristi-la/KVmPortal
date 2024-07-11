from django.views.generic import TemplateView
from django.shortcuts import redirect, render


error_template = 'error.html'


class HomeView(TemplateView):
    template_name = 'home.html'


def error_404(request, exception):
    return render(request, error_template, status=404)


def error_500(request):
    return render(request, error_template, status=500)
