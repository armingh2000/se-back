from users.models import Patient, Doctor, User
from rest_framework.views import APIView
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class UserEditView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        if request.user.pk != int(request.data['pk']):
            return Response("user is not authorized to edit this profile", status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, id=request.data['pk'])
        Role = Doctor if user.is_doctor else Patient
        Serializer = DoctorEditSerializer if user.is_doctor else PatientEditSerializer

        Person = get_object_or_404(Role, user=user)
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
        if request.user.pk != int(request.data['pk']):
            return Response("user is not authorized to edit this profile", status=status.HTTP_403_FORBIDDEN)

        user_type = int(request.data['type'])
        user = get_object_or_404(User, id=request.data['pk'])

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
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user_id = request.GET['user_id']
        user_type = int(request.GET['type'])
        user = get_object_or_404(User, id=user_id)
        (Role, Serializer) = (Doctor, DoctorProfileSerializer) if user_type \
            else (Patient, PatientProfileSerializer)

        profile = Serializer(get_object_or_404(Role, user=user), many=False).data

        return Response(profile)
