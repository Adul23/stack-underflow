# Python imports
import os

from decouple import config

# Project modules


# ----------------------------------------------
# Env id
#
ENV_POSSIBLE_OPTIONS = (
    "local",
    "prod",
)

ENV_ID = config("STACK_UNDERFLOW_ENV_ID", cast=str)
SECRET_KEY = config("STACK_UNDERFLOW_SECRET_KEY")



REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'origin',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]


# Redis configuration

REDIS_HOST = os.environ.get("STACK_UNDERFLOW_REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("STACK_UNDERFLOW_REDIS_PORT", "6379"))
REDIS_CELERY_DB = int(os.environ.get("CELERY_STACK_UNDERFLOW_REDIS_DB", "1"))

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# REDIS_DJANGORLAR_DB = config("STACK_UNDERFLOW_REDIS_DB", cast=int, default=2)

# Channels configuration
STACK_UNDERFLOW_CHANNELS_REDIS_HOST = os.environ.get("STACK_UNDERFLOW_CHANNELS_REDIS_HOST", "localhost")
STACK_UNDERFLOW_CHANNELS_REDIS_PORT = int(os.environ.get("STACK_UNDERFLOW_CHANNELS_REDIS_PORT", "6379"))
