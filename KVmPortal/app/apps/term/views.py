from django.shortcuts import render
from django.views.generic import TemplateView


def test(request):
    return render(
        request,
        'test.html',
        {'user': 'user'}
    )


class Terminal(TemplateView):
    template_name = 'terminal.html'
