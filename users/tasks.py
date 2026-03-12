from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_welcome_email(email, name):

    subject = "Welcome to Library System"

    message = f"""
    Hi {name},

    Welcome to our Library Management System.
    Your account has been successfully created.

    Thanks and regards,
    Susanta Kumar Behera
    """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )