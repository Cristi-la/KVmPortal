from django.shortcuts import render
from apps.term.tasks import SessionTask, debug_task
from apps.term.models import Session

def test(request):
    # SessionTask.delay(
    #     object_id=1,
    #     content_type='hypervisor',
    # )
    
    # debug_task.delay()

    # s = Session.manager.get_sessions(sid=25)
    # print('-----------------------')
    # print(s)
    return render(
        request,
        template_name='term.html'
    )
