from rest_framework import serializers
from users.models import User, Patient, Doctor
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password1', 'password2', 'is_doctor']

    def validate_is_doctor(self, value):
        if value is None:
            raise serializers.ValidationError("User must be either doctor or patient.")

        return value

    def validate(self, data):
        password = data['password1']

        errors = dict()
        try:
            validate_password(password=password, user=User)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if data['password1'] != data['password2']:
            errors['non_field_errors'] = ['Passwords must match.']

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(data)

    def save(self, request):
        user = User(
            email=self.validated_data['email'],
            is_doctor=self.validated_data['is_doctor'],
        )

        user.set_password(self.validated_data['password1'])
        user.save()

        is_doctor = self.validated_data['is_doctor']
        Role = Doctor if is_doctor else Patient
        Role.objects.create(user=user)

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'gender', 'profile_picture', 'is_doctor']


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(many=False, read_only=True)

    class Meta:
        model = Patient
        fields = ['height', 'weight', 'medical_record', 'user']


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(many=False, read_only=True)

    class Meta:
        model = Doctor
        fields = ['degree', 'cv', 'user']
