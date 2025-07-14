import os
from decouple import config

# Default to development settings
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    config("DJANGO_SETTINGS_MODULE", default="backend.settings.development"),
)

# Determine which settings to use based on environment
ENVIRONMENT = config("DJANGO_ENVIRONMENT", default="development")

if ENVIRONMENT == "production":
    from .production import *
else:
    from .development import *
