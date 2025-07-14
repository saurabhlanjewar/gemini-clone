"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from decouple import config

# environment = config("DJANGO_ENVIRONMENT", default="development")
# settings_module = f"backend.settings.{environment}"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
application = get_asgi_application()
