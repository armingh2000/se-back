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
            is_patient=not self.validated_data['is_doctor']
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
        fields = ['pk', 'email', 'first_name', 'last_name', 'gender', 'profile_picture', 'is_doctor', 'is_patient']


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


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'profile_picture']

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.gender = validated_data['gender']
        instance.profile_picture = validated_data['profile_picture']
        instance.save()

        return instance


class PatientEditSerializer(serializers.ModelSerializer):
    user = UserEditSerializer(many=False, read_only=True)

    class Meta:
        model = Patient
        fields = ['height', 'weight', 'medical_record', 'user']

    def update(self, instance, validated_data):
        instance.height = validated_data['height']
        instance.weight = validated_data['weight']
        instance.medical_record = validated_data['medical_record']
        instance.save()

        return instance

class DoctorEditSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(many=False, read_only=True)

    class Meta:
        model = Doctor
        fields = ['degree', 'degree_picture', 'cv', 'location', 'user']

    def update(self, instance, validated_data):
        instance.degree = validated_data['degree']
        instance.cv = validated_data['cv']
        instance.location = validated_data['location']
        instance.degree_picture = validated_data['degree_picture']
        instance.save()

        return instance
