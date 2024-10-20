# VIRW

```bash
docker compose build
docker compose up -d
docker compose logs
```

### App Proxy statements:
- *./virw/app/entrypoint_backend.sh* - remove/add proxy to pip install

### Docker Proxy setup:
```bash
mkdir /etc/systemd/system/docker.service.d
cat .proxy > /etc/systemd/system/docker.service.d/http-proxy.conf
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl show --property Environment docker
```

### Run localy:
```bash
cd backend
celery -A backend worker --pool=solo
celery -A backend worker -E --loglevel=info --pool=threads
celery -A backend beat --loglevel=INFO --scheduler backend.scheduler:ReadyTenantAwareScheduler

python.exe .\manage.py create_default  

```


python manage.py create_public_tenant --domain_url localhost --owner_email admin@localhost
python manage.py createsuperuser
python.exe .\manage.py runserver


```bash

from apps.common.models import Client, TenantUser
u = TenantUser.objects.get(username='test')
t = Client.objects.all()[2]
t.add_user(u)
```