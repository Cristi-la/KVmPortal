from celery import shared_task
from utils.control.tasks import Processor, BaseChannel, BaseStep
from apps.kvm.models import XMLData, Hypervisor
from ping3 import ping

@shared_task(
    bind=True, 
    base=BaseChannel, 
    name='Ping Host',
)
def ping_host(self, host: str):
    try:
        result = ping(host, timeout=4)

        if result is not None:
            self.send_message({
                'host': host, 
                'fail': False, 
                'detail': f'Pinging {host} success'
            })
            return True

        self.send_message({
            'host': host, 
            'fail': True, 
            'detail': f'Pinging {host} failed: Unreachable'
        })
    
    except Exception as e:
        self.send_message({
            'host': host, 
            'fail': True, 
            'detail': f'Pinging {host} failed: Unexpected error: {str(e)}'
        })

    return False



@shared_task(
    bind=True, 
    base=BaseStep, 
    name='Collect Hypervizor data',
)
def collect_data(
    self: BaseStep,
    hypervisor_id: int,
    skip: bool = True
):
    def collect():
        data = ""
        with open('P:\\WKVM\\backend\\capabilities.xml', 'r') as f:
            data = f.read()

        return XMLData.XMLType.CAPABILITIES, data
    
    tasks = [
        collect
    ]

    obj = Hypervisor.objects.get(id=hypervisor_id)
    proc = Processor(tasks)
    buffer, _ = self.run_process(proc, skip)
    out = obj.proccess_bulk_xml(buffer)

    return out


