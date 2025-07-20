from allauth.account.adapter import DefaultAccountAdapter
from apivpn.tasks import send_confirmation_mail, send_reset_password_email
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.contrib.auth import get_user_model
from allauth.exceptions import ImmediateHttpResponse
from django.http import JsonResponse

class MailgunTemplateAccountAdapter(DefaultAccountAdapter):
    """ def clean_email(self, email):
        email = super().clean_email(email)
        if EmailAddress.objects.filter(email__iexact=email).exists():
            raise ValidationError(gettext_lazy("This email address is already in use."))
        return email """
    
    def get_email_confirmation_url(self, request, emailconfirmation):
        key = emailconfirmation.key
        return f"http://localhost:5173/auth/confirm-email/{key}/"
    
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


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = user_email(sociallogin.user)

        if not email:
            return

        if sociallogin.is_existing:
            return

        User = get_user_model()

        try:
            existing_user = User.objects.get(email=email)
            sociallogin.connect(request, existing_user)

        except User.DoesNotExist:
            pass

    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        raise ImmediateHttpResponse(JsonResponse({
            "error": str(error) if error else "Authentication failed",
        }, status=400))