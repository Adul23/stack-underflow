# Python modules
import os

# Django modules
from django.core.wsgi import get_wsgi_application

# Project modules
from stack_underflow.conf import ENV_ID

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"stack_underflow.env.{ENV_ID}")

application = get_wsgi_application()
