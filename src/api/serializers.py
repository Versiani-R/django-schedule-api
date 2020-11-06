from rest_framework import serializers

from api.models import Register, TimeList


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Register
        fields = ['id', 'email', 'password']


class TimeListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TimeList
        fields = ['id', 'day', 'month', 'year', 'token_id']
