from anymail.message import AnymailMessage
from ton_backend.celery import app
from celery import shared_task
from django.template.loader import render_to_string
from django.template.loader import get_template


@shared_task()
def send_confirmation_mail(to, user_name, activate_url):
    context = {
        "user_name": user_name,
        "confirm_url": activate_url,
    }

    subject = render_to_string("account/email/email_confirmation_subject.txt").strip()
    body = render_to_string("account/email/email_confirmation_message.txt", context)
    html_body = render_to_string("account/email/email_confirmation_message.html", context)

    message = AnymailMessage(
        to=[to],
        subject=subject,
        body=body
    )
    message.attach_alternative(html_body, "text/html")

    message.send()

@shared_task()
def send_reset_password_email(to, reset_url, user_name):
    context = {
        "user_name": user_name,
        "reset_url": reset_url,
    }

    subject = render_to_string("account/email/reset_password_subject.txt").strip()
    body = render_to_string("account/email/reset_password_message.txt", context)
    html_body = render_to_string("account/email/reset_password_message.html", context)

    message = AnymailMessage(
        to=[to],
        subject=subject,
        body=body
    )
    message.attach_alternative(html_body, "text/html")

    message.send()