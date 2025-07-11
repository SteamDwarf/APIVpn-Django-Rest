from anymail.message import AnymailMessage
from ton_backend.celery import app

@app.task
def send_mail(to, user_name, activate_url):
    print(f"[CELERY] Preparing to send email to {to}...")

    message = AnymailMessage(
        to=[to],
    )
    message.template_id = "registration"  # ID шаблона из Mailgun
    message.merge_data = {
        "email": {
            "user_name": user_name,
            "confirm_url": activate_url,
        }
    }
    message.send()

    print(f"[CELERY] Email sent to {to}")