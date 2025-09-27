import os

from django.core.wsgi import get_wsgi_application

settings_module = os.environ.get(
    "DJANGO_SETTINGS_MODULE", "booking_clone.settings.dev"
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

application = get_wsgi_application()
