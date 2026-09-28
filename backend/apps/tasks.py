from typing import Any

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_confirmation_mail(user_email : Any | str) -> int:
    subject = "Confirmation Mail"
    message = "If you are seeing this then the email that you sent is correct"
    return send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[user_email])


@shared_task
def cleanup_expired_sessions():
    from django.utils import timezone

    now = timezone.now().isoformat()
    return f'Periodic health check at {now}'

