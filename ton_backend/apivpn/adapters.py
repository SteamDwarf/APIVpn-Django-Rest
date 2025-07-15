from allauth.account.adapter import DefaultAccountAdapter
from anymail.message import AnymailMessage
from django.conf import settings
from django.template.loader import render_to_string
from apivpn.tasks import send_confirmation_mail, send_reset_password_email

class MailgunTemplateAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        key = emailconfirmation.key
        return f"http://127.0.0.1:8000/api/v1/account-confirm-email/{key}/"
    
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        # Получаем пользователя
        user = emailconfirmation.email_address.user
        email = emailconfirmation.email_address.email
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)

        send_confirmation_mail.delay(email, user.get_username(), activate_url)

    def send_mail(self, template_prefix, email, context):
        print("SEND MAIL", template_prefix, email, context)
        send_reset_password_email.delay(
            email, 
            context['password_reset_url'],
            context['user'].get_username()
        )
        # Формируем письмо с использованием Mailgun Template
        """ message = AnymailMessage(
            to=[email],
        )
        message.template_id = "registration"  # ID шаблона из Mailgun
        message.merge_data = {
            email: {
                "user_name": user.get_username(),
                "confirm_url": activate_url,
            }
        }
        message.send() """