from celery import shared_task, Task
import time
import asyncio
# from channels.layers import get_channel_layer
# from apps.term.control.interface import SSHInterface
# from apps.term.models import Auth

# def prep_channel(room_group_name):
#     channel_layer = get_channel_layer()

#     def send_message(data):
#         asyncio.run(channel_layer.group_send(
#             room_group_name, {
#                 "type": "group_message", 
#                 "message": data
#             }
#         ))
#     return send_message


# # @shared_task(bind=True)
# # def update(self, num):
# #     self.room_id = '5'
# #     self.room_group_name = "session_%s" % self.room_id
# #     channel_layer = get_channel_layer()


# #     for i in range(5):
# #         loop = asyncio.new_event_loop()
# #         asyncio.set_event_loop(loop)
        
# #         print(i)
# #         time.sleep(1)

# #         loop.run_until_complete(channel_layer.group_send(
# #             self.room_group_name, {
# #                 "type": "group_message", 
# #                 "message": f'Data{i}'
# #             }
# #         ))


# #     loop = asyncio.new_event_loop()
# #     asyncio.set_event_loop(loop)
    
# #     print(i)
# #     time.sleep(1)

# #     loop.run_until_complete(channel_layer.group_send(
# #         self.room_group_name, {
# #             "type": "group_message", 
# #             "message": 'test'
# #         }
# #     ))

# #     return 'Done'


# @shared_task(bind=True)
# def session_tasks(self, ip_fqdn, username, password):

#     commands = ["ls --color=auto", "uname -a", "sleep 5","echo -e 'e[1;33mYellow Text\e[0m'", "uname -a", 'htop']
#     room_id = '5'
#     room_group_name = "session_%s" % room_id



    
#     auth = Auth.from_data(ip_fqdn, username, password)

#     ssh = SSHInterface(auth, timeout=10)
#     ssh.run(
#         actions=commands,
#         reader_handler=prep_channel(room_group_name)
#     )

from apps.term.models import Session
from backend.celery import app

class SessionTask(Task):
    name = 'apps.term.tasks.SessionTask'

    def prepare(self):
        return Session.init(
            object_id=self.object_id,
            content_type=self.content_type,
        )
        
    def run(
            self, 
            object_id, 
            content_type,
        ):
        
        self.object_id = object_id
        self.content_type = content_type
        self.session = self.prepare()
        print(self.session)

        time.sleep(5)
        self.session.delete()

        return 'Task completed'
    


    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('Task failed')

    def on_success(self, retval, task_id, args, kwargs):
        print('Task success')


    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print('Task retry')


    def on_revoked(self, request):
        print('Task revoked')

SessionTask = app.register_task(SessionTask())