from rest_framework import serializers

from api.models import Register, TimeList, ScheduleApi, ApiCall


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Register
        fields = ['id', 'email', 'password']


class TimeListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TimeList
        fields = ['id', 'day', 'month', 'year', 'token_id']


class ScheduleApiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScheduleApi
        fields = ['id', 'day', 'month', 'year', 'hours', 'minutes', 'company_name', 'token_id']


class ApiCallsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ApiCall
        fields = ['id', 'token_id', 'api_credits']
