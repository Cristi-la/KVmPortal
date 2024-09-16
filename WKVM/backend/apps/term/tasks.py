from celery import shared_task, Task
# from utils.control.ssh import SSHInterface
# from utils.control.interface import Message
from apps.term.models import Session
from backend.celery import app
from channels.layers import get_channel_layer
import asyncio

def prep_channel(sid):
    channel_layer = get_channel_layer()

    def send_message(data):
        asyncio.run(channel_layer.group_send(
            sid, {
                "type": "group.message",
                # "message": Message.data(data, sid)
            }
        ))
    return send_message


# class SessionDettach(Task):
#     def prepare(self) -> Session:
#         return Session.init(
#             object_id=self.object_id,
#             content_type=self.content_type,
#         )

# class SessionAttach(SessionDettach):
#     ...

# class ReadOnlySession(SessionAttach):
#     ...

# class ReadWriteSession(SessionAttach):
#     ...

# class SwapSession(SessionAttach):
#     ...

# class SessionTask(SessionAttach):

#     def run(
#             self, 
#             object_id, 
#             content_type,
#         ):
        
#         self.object_id = object_id
#         self.content_type = content_type
#         self.session = self.prepare()
#         auth = self.session.content_object.auth
#         mgt_ip = self.session.content_object.mgt_ip
#         sid = str(self.session.pk)

#         ssh = SSHInterface(mgt_ip, auth)
#         ssh.buffer_handler = prep_channel(sid)


#         self.session.status = Session.Status.FAILED

#         if ssh.run(
#                 actions=['ls --color=auto', 'uname -a', 'sleep 5', 'echo -e ddd', 'uname -a', 'htop'],
#             ):
#             self.session.status = Session.Status.COMPLETED


#         self.session.output = ssh.output
#         self.session.save()

#         return 'Task completed'
    


#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         print('Task failed')

#     def on_success(self, retval, task_id, args, kwargs):
#         print('Task success')


#     def on_retry(self, exc, task_id, args, kwargs, einfo):
#         print('Task retry')


#     def on_revoked(self, request):
#         print('Task revoked')

# SessionTask = app.register_task(SessionTask())

# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')