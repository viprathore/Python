import datetime
from django.utils import timezone

from rest_framework import serializers


from core.models import User
from expectations.models import ManagingExpectation


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username')

    def validate(self, data):
        username = data.get('email').split('@')[0]
        try:
            user = User.objects.get(username=username)
            if user:
                raise serializers.ValidationError("USER_NAME_ALREADY_EXIST")
        except User.DoesNotExist:
            pass
        check_email = User.objects.filter(email=data.get("email"))
        if check_email:
            raise serializers.ValidationError("EMAIL_ALREADY_EXIST")
        data['username'] = username
        return data


class GithubAuthSerializer(serializers.Serializer):
    pass


class GetExpectationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = ManagingExpectation
        fields = ("user", "expected_role", "expected_finished_time")

    def get_user(self, obj):
        return obj.user.username


class ExpectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagingExpectation
        fields = ("id", "expected_role", "expected_finished_time")

    def validate(self, data):
        expected_finished_time = data.get('expected_finished_time')
        if timezone.now() > expected_finished_time:
            raise serializers.ValidationError('Expected finished time can not be less than current time')
        return data