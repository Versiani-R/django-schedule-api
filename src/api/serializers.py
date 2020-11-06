from rest_framework import serializers

from api.models import Register


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Register
        fields = ['id', 'email', 'password']
