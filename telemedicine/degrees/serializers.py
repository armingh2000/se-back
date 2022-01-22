from rest_framework import serializers
from .models import *
from accounts.serializers import UserProfileSerializer
from users.models import Doctor

class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = ['pk', 'name', 'picture']

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.picture = validated_data['picture']
        instance.save()

        return instance


