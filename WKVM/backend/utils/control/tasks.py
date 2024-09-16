import time
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import Task
import inspect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Processor:
    def __init__(self, tasks=None, context={}):
        self.context = context
        self.tasks = self._bind_context_to_tasks(tasks)
        self.total_tasks = len(self.tasks)
        self.current_task_index = 0

    def _bind_context_to_tasks(self, tasks):
        bound_tasks = []
        for task in tasks:
            if callable(task):
                # Wrap the task with a context checker
                bound_tasks.append(self._wrap_task_with_context(task))
            else:
                raise ValueError(f"Task {task} is not callable")
        return bound_tasks

    def _wrap_task_with_context(self, task):

        task_signature = inspect.signature(task)
        if 'context' in task_signature.parameters:
            # Task accepts `context`, so pass it along with other args/kwargs
            def wrapped_task(*args, **kwargs):
                return task(context=self.context, *args, **kwargs)
        else:
            # Task does not accept `context`, so pass args/kwargs without context
            def wrapped_task(*args, **kwargs):
                return task(*args, **kwargs)

        return wrapped_task

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_task_index < self.total_tasks:
            task = self.tasks[self.current_task_index]
            self.current_task_index += 1
            return task
        else:
            raise StopIteration

    def get_total_tasks(self):
        return self.total_tasks
    
    def get_steps(self) -> list[int, int]:
        return self.current_task_index, self.total_tasks
    

class BaseChannel(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info(f"Task {task_id} failed due to {exc}")
        self.send_message({'detail': "Task failed"})

    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"Task {task_id} succeeded with result: {retval}")
        self.send_message({'detail': "Task succeeded"})

    def send_message(self, message: dict):      
        channel_layer = get_channel_layer()

        if not channel_layer:
            logger.info(f"Channel layer is not available. Cannot send progress updates for task {self.request.id}")
            return
        
        try:
            group_name = f'task_progress_{self.request.id}'
            async_to_sync(channel_layer.group_send)(group_name, {
                'type': 'task_progress',
                'data': {
                    'task_id': self.request.id,
                    **message,
                }
            })
            logger.info(f"Message sent to WebSocket for task {self.request.id}: {message}")
        except Exception as e:
            logger.warning(f"Failed to send message for task {self.request.id}. Error: {e}")

class BaseStep(BaseChannel):
    def before_start(self, *args, **kwargs):
        self.request.total_steps = 0
        self.request.last_step = 0

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        self.request.total_steps = 0
        self.request.last_step = 0

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        self.request.total_steps = 0
        self.request.last_step = 0

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info(f"Task {task_id} failed due to {exc}")
        self.send_progress(self.request.last_step, detail="Task failed", fail=True)

    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"Task {task_id} succeeded with result: {retval}")
        self.send_progress(self.request.total_steps, detail="Task succeeded")
    
    def send_progress(self, step: int, detail: str = None, fail=False):
        if step > self.request.total_steps:
            logger.error(f"Step {step} exceeds total steps {self.request.total_steps} for task {self.request.id}")
            return
        
        self.request.last_step = step

        self.send_message({
            'step': step,
            'total_steps': self.request.total_steps,
            'detail': detail,
            'fail': fail
        })

    def send_next_step(self, detail: str = None, fail=False):
        self.request.last_step += 1
        self.send_progress(self.request.last_step, detail, fail=fail)

    def run_process(self, proc: Processor, skip: bool = True, **kwargs):
        self.request.last_step, self.request.total_steps = proc.get_steps()
        self.request.skip = skip

        buffer = []

        for num, task in enumerate(proc):
            try:
                output = task()
                buffer.append(output)
                self.send_next_step(f"Processing step {num}, ended with output: {output}")
            except Exception as e:
                self.send_next_step(f"Processing step {num}, ended with error: {e}", fail=True)
        return buffer, proc.context