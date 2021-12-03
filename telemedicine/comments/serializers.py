from rest_framework import serializers
from users.models import Patient
from accounts.serializers import PatientProfileSerializer
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    patient = PatientProfileSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['patient', 'body', 'created_on']

