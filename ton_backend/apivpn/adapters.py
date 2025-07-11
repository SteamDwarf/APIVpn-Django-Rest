from allauth.account.adapter import DefaultAccountAdapter
from anymail.message import AnymailMessage
from django.conf import settings
from django.template.loader import render_to_string
from apivpn.tasks import send_mail

class MailgunTemplateAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        # Получаем пользователя
        user = emailconfirmation.email_address.user
        email = emailconfirmation.email_address.email
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)

        send_mail.delay(email, user.get_username(), activate_url)
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