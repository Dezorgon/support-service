from django.contrib.auth.models import User
from django.core.mail import send_mail

from support.celery import app
from support.settings import EMAIL_HOST_USER


@app.task
def send_email_to_all_users(text):
    emails = User.objects\
        .filter(is_active=True)\
        .exclude(email='')\
        .values_list('email', flat=True)

    send_mail('Support', text, EMAIL_HOST_USER, emails)

    return text
