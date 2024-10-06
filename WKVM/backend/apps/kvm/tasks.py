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
):
    def collect():
        data = ""
        with open('P:\\WKVM\\backend\\domains.xml', 'r') as f:
            data = f.read()

        return XMLData.XMLType.DOMAIN, data
    

    obj: Hypervisor = Hypervisor.objects.get(id=hypervisor_id)
    data = [collect()]
    obj.save_bulk_xml(data)

    vm = obj.vms.get(id=2)
    vm.parse_xmls(data)
    vm.save()

    # # Rmove this code after development
    # obj.parse_xmls(data) 
    # obj.save()

    # obj.
    
    # tasks = [
        
    # ]

    
    # proc = Processor(tasks)
    # buffer, _ = self.run_process(proc)
    

    return None
