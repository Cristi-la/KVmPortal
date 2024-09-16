```bash
cd backend
celery -A backend worker --pool=solo
celery -A backend worker -E --loglevel=info --pool=threads
```