web: gunicorn app:app
worker: celery -A worker.tasks worker --pool=solo -l info -E