```bash
cd backend
celery -A backend.celery worker --pool=solo
celery -A backend worker -l INFO   
```