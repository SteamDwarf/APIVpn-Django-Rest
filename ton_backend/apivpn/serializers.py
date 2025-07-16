from rest_framework import serializers
from apivpn.models import Todo
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ['title']

class PublicUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Убери email, если хочешь ограничить


class CustomRegisterSerializer(RegisterSerializer):
    def validate_email(self, email):
        email = super().validate_email(email)

        if get_user_model().objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return email


