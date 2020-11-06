from rest_framework import serializers

from api.models import Register, ScheduledDate


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Register
        fields = ['id', 'email', 'password']


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScheduledDate
        fields = ['id', 'date', 'count']
