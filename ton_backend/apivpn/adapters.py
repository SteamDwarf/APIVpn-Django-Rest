from allauth.account.adapter import DefaultAccountAdapter
from anymail.message import AnymailMessage
from django.conf import settings
from django.template.loader import render_to_string
from apivpn.tasks import send_confirmation_mail, send_reset_password_email
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

class MailgunTemplateAccountAdapter(DefaultAccountAdapter):
    """ def clean_email(self, email):
        email = super().clean_email(email)
        if EmailAddress.objects.filter(email__iexact=email).exists():
            raise ValidationError(gettext_lazy("This email address is already in use."))
        return email """
    
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