from celery import Celery
import os



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ton_backend.settings")
app = Celery("ton_backend", broker="redis://192.168.0.104:6379", backend="redis://192.168.0.104:6379")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

