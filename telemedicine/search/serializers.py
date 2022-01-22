from rest_framework import serializers
from users.models import User, Doctor
from degrees.models import Degree


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'email', 'first_name', 'last_name', 'gender', 'profile_picture']


class DoctorSearchSerializer(serializers.ModelSerializer):
    user = UserSearchSerializer(many=False, read_only=True)

    class Meta:
        model = Doctor
        fields = ['user']
