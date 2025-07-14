import os
from celery import Celery
from decouple import config

environment = config("DJANGO_ENVIRONMENT", default="development")
settings_module = f"backend.settings.{environment}"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = Celery("backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
