from rest_framework import serializers
from apivpn.models import Todo
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User



class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ['title']

class PublicUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Убери email, если хочешь ограничить

