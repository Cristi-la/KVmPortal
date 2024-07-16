from django.shortcuts import render
from django.views.generic import TemplateView


def test(request):
    return render(
        request,
        'test.html',
        {'user': 'user'}
    )


class BaseTerminal(TemplateView):
    template_name = 'terminal.html'


class Terminal(BaseTerminal):
    template_name = 'terminal.html'


class MultiTerminal(BaseTerminal):
    template_name = 'terminal.html'


class ScriptTerminal(BaseTerminal):
    template_name = 'terminal.html'
