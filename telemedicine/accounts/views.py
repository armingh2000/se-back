from users.models import Patient, Doctor, User
from rest_framework.views import APIView
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class UserEditView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        user_type = int(request.data['type'])

        if (user_type and not user.is_doctor) or (not user_type and not user.is_patient):
            return Response("user does not have that type", status=status.HTTP_409_CONFLICT)

        (Role, Serializer) = (Doctor, DoctorEditSerializer) if user_type \
            else (Patient, PatientEditSerializer)

        Person = Role.objects.get(user=user)
        serializer = Serializer(Person, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = UserEditSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("successfully updated", status=status.HTTP_200_OK)

class UserCreateTypeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_type = int(request.data['type'])
        user = request.user

        if (user_type and user.is_doctor) or (not user_type and user.is_patient):
            return Response("user already has that type", status=status.HTTP_409_CONFLICT)

        Role = Doctor if user_type else Patient
        Role.objects.create(user=user)

        if user_type:
            user.is_doctor = 1
        else:
            user.is_patient = 1
        user.save()

        return Response("successfully updated", status=status.HTTP_200_OK)

class UserProfileView(APIView):
    def get(self, request):
        user_pk = request.GET['user_pk']
        user_type = int(request.GET['type'])
        user = get_object_or_404(User, pk=user_pk)
        (Role, Serializer) = (Doctor, DoctorProfileSerializer) if user_type \
            else (Patient, PatientProfileSerializer)

        profile = Serializer(get_object_or_404(Role, user=user), many=False).data

        return Response(profile)
