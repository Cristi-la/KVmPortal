from django.core.management.base import BaseCommand
from apps.kvm.models import (
    Hypervisor,
    Network,
    NetworkPort,
    HostInterface,
    NodeDevice,
    StoragePool,
    Domain,
    HostDevice,
    StorageVolume,
    NetworkInterface,
    NetworkFilter,
    Snapshot,
    DomainCheckpoint,
    KeyFile,
    Auth,
    Tag,
)
import uuid
from apps.common.models import Client, ClientDomain, TenantUser
from tenant_users.tenants.tasks import provision_tenant
from tenant_users.tenants.utils import create_public_tenant
from django_tenants.utils import tenant_context
from django.db import models
from django.core.management import call_command
from django.conf import settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django_celery_beat.models import PeriodicTask, CrontabSchedule



class Command(BaseCommand):
    help = 'Create default objects'

    def __create(self, model: models.Model, data: list[dict]):
        for row in data:
            instance, created = model.objects.update_or_create(
                **row
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'{model.__class__.__name__} {list(row.keys())[0] } created'))
            else:
                self.stdout.write(self.style.SUCCESS(f'{model.__class__.__name__} {list(row.keys())[0] } updated'))



    def create_auth(self):
        data = [
            {'username':'admin', 'port': 22},
        ]
        self.__create(Auth, data)

    def create_tags(self):
        data = [
            {"name": "KVM", "color": "#FF5733"},
            {"name": "Virtualization", "color": "#33FF57"},
            {"name": "Hypervisor", "color": "#3357FF"},
            {"name": "VM", "color": "#F39C12"},
            {"name": "QEMU", "color": "#8E44AD"},
            {"name": "Libvirt", "color": "#27AE60"},
            {"name": "Snapshot", "color": "#E74C3C"},
            {"name": "Live Migration", "color": "#1ABC9C"},
        ]
        self.__create(Tag, data)

    def create_hypervisors(self):
        data = [
            {
                'hostname': 'hypervisor1',
                'mgt_ip': '8.8.4.4',
                'capabilities_xml': '<capabilities>...</capabilities>',
                'capabilities_xml_hash': '',
                'sysinfo_xml': '<sysinfo>...</sysinfo>',
                'sysinfo_xml_hash': '',
            },
            {
                'hostname': 'hypervisor2',
                'mgt_ip': '8.8.8.8',
                'capabilities_xml': '<capabilities>...</capabilities>',
                'capabilities_xml_hash': '',
                'sysinfo_xml': '<sysinfo>...</sysinfo>',
                'sysinfo_xml_hash': '',
            },
        ]
        self.__create(Hypervisor, data)


    def create_domains(self):
        hypervisor1 = Hypervisor.objects.get(id=1)
        hypervisor2 = Hypervisor.objects.get(id=2)
        data = [
            {
                'hypervisor': hypervisor1,
                'name': 'vm1',
                'uuid': str(uuid.uuid4()),
                'state': 'running',
                'memory': 2048,  # Memory in KiB
                'vcpus': 2,
            },
            {
                'hypervisor': hypervisor1,
                'name': 'vm2',
                'uuid': str(uuid.uuid4()),
                'state': 'shutoff',
                'memory': 4096,
                'vcpus': 4,
            },
            {
                'hypervisor': hypervisor2,
                'name': 'vm3',
                'uuid': str(uuid.uuid4()),
                'state': 'paused',
                'memory': 1024,
                'vcpus': 1,
            },
        ]
        self.__create(Domain, data)

    def recreate_database(self, db_name, user, password, host, port):
        """
        Drops the existing database and creates a new one with the same name.
        """
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        try:
            cur.execute(f'DROP DATABASE IF EXISTS {db_name};')
            self.stdout.write(self.style.SUCCESS(f'Database {db_name} dropped successfully.'))
        except psycopg2.Error as e:
            self.stdout.write(self.style.ERROR(f"Error dropping database {db_name}: {e}"))

        try:
            cur.execute(f'CREATE DATABASE {db_name};')
            self.stdout.write(self.style.SUCCESS(f'Database {db_name} created successfully.'))
        except psycopg2.Error as e:
            self.stdout.write(self.style.ERROR(f"Error creating database {db_name}: {e}"))

        cur.close()
        conn.close()
        

    def create_tenents(self):
        db_config = settings.DATABASES['default']
        self.recreate_database(
            db_name=db_config['NAME'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            host=db_config['HOST'],
            port=db_config['PORT'],
        )

        
        # Migration
        call_command('makemigrations')
        call_command('migrate_schemas', '--shared')
        call_command('migrate_schemas')

        #  Public tenant + admin user
        public_tenant, domain, profile = create_public_tenant(
            'localhost',
            'admin@localhost',
            is_staff=True,
            is_superuser=True,
            username='admin',
            password='admin',
        )

        # additional domain for public tenant
        ClientDomain.objects.create(
            domain='127.0.0.1', 
            tenant=public_tenant,
        ).save()

        ClientDomain.objects.create(
            domain='web', 
            tenant=public_tenant,
        ).save()

        # Private tenant + test user
        user = TenantUser.objects.create(
            email="test@localhost.com", 
            username="test",
            is_active=True,
        )
        user.set_password("test")
        user.save()
        public_tenant.add_user(user, is_superuser=True, is_staff=True)


        tenant, domain = provision_tenant(
            "Test", 
            "test", 
            user,
            is_staff=True,
            is_superuser=True,
            tenant_type=Client.ClientType.PRIVATE
        )

    def handle(self, *args, **kwargs):
        self.create_tenents()

        tenant = Client.objects.filter(name='Test').first()

        if tenant is None:
            self.stdout.write(self.style.ERROR('Tenant was creation failed!'))
            return

        with tenant_context(tenant):
            self.create_auth()
            self.create_tags()

            self.create_hypervisors()
            self.create_domains()

        self.stdout.write(self.style.SUCCESS('Default tags have been created/updated.'))
