# from celery import shared_task
# from utils.control.tasks import Processor, BaseChannel, BaseStep
# from apps.kvm.models import XMLData, Hypervisor
from apps.kvm.models import Hypervisor, Domain
from backend.celery import app
import logging
from apps.kvm.virt.utils import ping_host, ping_hosts
from apps.kvm.models import Hypervisor, Domain
from backend.celery import app
from concurrent.futures import ThreadPoolExecutor, as_completed
from celery import shared_task

logger = logging.getLogger(__name__)


from django.db import connection
@app.task
def simple():
    print(f"Simple task executedL {connection.schema_name}")
    return None


def get_hypervisor_hosts():
    hypervisors = Hypervisor.objects.all()
    hosts = {hypervisor.hostname: hypervisor.mgt_ip for hypervisor in hypervisors}
    return hosts


def get_domain_hosts():
    domains = Domain.objects.all()
    # Ensure that the Domain model has an 'ip' field
    hosts = {domain.name: domain.ip for domain in domains if domain.ip}
    return hosts


@app.task
def all_host_ping_task():
    """
    Celery task to ping all hypervisors and return a dictionary with hostname/IP as keys
    and ping results as values.
    """
    hosts = get_hypervisor_hosts()
    results = ping_hosts(hosts)
    return results


@app.task 
def all_domains_ping_task():
    """
    Celery task to ping all domains and return a dictionary with domain name/IP as keys
    and ping results as values.
    """
    hosts = get_domain_hosts()
    results = ping_hosts(hosts)
    return results

@app.task
def all_host_collect_data():
    """
    Dispatches tasks to collect data from all hypervisors concurrently.
    """
    hypervisor_ids = Hypervisor.objects.values_list('id', flat=True)

    # Dispatch a separate task for each hypervisor
    for hypervisor_id in hypervisor_ids:
        host_collect_data.delay(hypervisor_id)

@app.task
def host_collect_data(hypervisor_id):
    """
    Collects data from a single hypervisor.
    """
    try:
        hypervisor = Hypervisor.objects.get(id=hypervisor_id)
        collect_data(hypervisor)
    except Hypervisor.DoesNotExist:
        logger.error(f"Hypervisor with ID {hypervisor_id} does not exist.")
    except Exception as e:
        logger.error(f"Error collecting data for hypervisor ID {hypervisor_id}: {e}")

def collect_data(hypervisor):
    """
    Collects data from the given hypervisor efficiently.
    """
    from concurrent.futures import ThreadPoolExecutor

    def collect_stats():
        print(f"Collecting stats for {hypervisor.hostname}")
        pass

    def collect_vm_info():
        print(f"Collecting VM info for {hypervisor.hostname}")
        pass

    def collect_network_info():
        print(f"Collecting network info for {hypervisor.hostname}")
        hypervisor.hostname = f"test{hypervisor.id}"
        hypervisor.save()
        pass

    tasks = [collect_stats, collect_vm_info, collect_network_info]

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(task) for task in tasks]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error in data collection task for {hypervisor.hostname}: {e}")




# @shared_task(
#     bind=True, 
#     base=BaseStep, 
#     name='Collect Hypervizor data',
# )
# def collect_data(
#     self: BaseStep,
#     hypervisor_id: int,
# ):
#     def collect():
#         data = ""
#         with open('P:\\WKVM\\backend\\domains.xml', 'r') as f:
#             data = f.read()

#         return XMLData.XMLType.DOMAIN, data
    

#     obj: Hypervisor = Hypervisor.objects.get(id=hypervisor_id)
#     data = [collect()]
#     obj.save_bulk_xml(data)

#     vm = obj.vms.get(id=2)
#     vm.parse_xmls(data)
#     vm.save()

#     # # Rmove this code after development
#     # obj.parse_xmls(data) 
#     # obj.save()

#     # obj.
    
#     # tasks = [
        
#     # ]

    
#     # proc = Processor(tasks)
#     # buffer, _ = self.run_process(proc)
    

#     return None


