from django.shortcuts import render
from apps.term.tasks import SessionTask

def test(request):
    SessionTask.delay(
        object_id=1, 
        content_type='hypervisor',
    )

    return render(
        request, 
        template_name='term.html'
    )