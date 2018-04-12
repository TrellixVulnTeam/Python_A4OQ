from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(
            max_length = None, use_url=True
        )   
    class Meta:
        model = Task
        fields = ('image')