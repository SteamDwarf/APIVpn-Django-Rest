from rest_framework import serializers
from apivpn.models import Todo

class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ['title']