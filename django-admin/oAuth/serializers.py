from django.contrib.auth.models import User
from oAuth.models import NewUser, Books
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['url', 'username', 'email', 'is_staff']


class Bookerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'
