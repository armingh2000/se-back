from users.models import Patient, Doctor, User
from rest_framework.views import APIView
from .serializers import PatientProfileSerializer, DoctorProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions
from rest_framework.response import Response

# Create your views here.


class UserProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]


    def get(self, request):
        user_id = request.GET['user_id']
        user = get_object_or_404(User, id=user_id)
        Role = Doctor if user.is_doctor else Patient
        Serializer = DoctorProfileSerializer if user.is_doctor else PatientProfileSerializer

        profile = Serializer(get_object_or_404(Role, user=user), many=False).data

        return Response(profile)

