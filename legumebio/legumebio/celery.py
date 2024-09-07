import os
from celery import Celery

# Définissez le nom de l'application Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legumebio.settings')

app = Celery('legumebio')

# Importez les configurations de votre projet
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatiquement découvre les tâches dans les applications Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')