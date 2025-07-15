from rest_framework import serializers
from apivpn.models import Todo
from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from rest_framework import serializers
from apivpn.tasks import send_reset_password_email
from allauth.account.models import EmailConfirmationHMAC
from django.template.loader import get_template
from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from apivpn.tasks import send_reset_password_email
from allauth.account.utils import user_pk_to_url_str
from apivpn.forms import CeleryPasswordResetForm


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ['title']



class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_password_reset_form(self):
        return CeleryPasswordResetForm

    def save(self):
        request = self.context.get("request")
        form_class = self.get_password_reset_form()
        form = form_class(data=self.data)  # передаём данные в форму

        if form.is_valid():  # Важно!
            form.save(
                use_https=request.is_secure(),
                from_email=None,
                request=request,
                email_template_name="account/email/reset_password_message.txt",
                subject_template_name="account/email/reset_password_subject.txt",
            )

    """ def save(self):
        request = self.context.get("request")  # <--- получаем request безопасно
        email = self.validated_data["email"]
        user = get_user_model().objects.filter(email=email).first()

        if not user or not request:
            return

        uid = user_pk_to_url_str(user)
        token = default_token_generator.make_token(user)
        reset_url = f"http://127.0.0.1:8000/api/v1/password/reset/confirm/{uid}/{token}/"

        send_reset_password_email.delay(email, reset_url, user.get_username()) """
    """ def get_email_options(self):
        print(get_template('account/email/reset_password_message.txt'))
        return {
            'email_template_name': 'account/email/reset_password_message.txt'
        } """