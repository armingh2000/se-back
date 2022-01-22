from .models import Degree
from users.models import Doctor
from rest_framework.views import APIView
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class DegreeAddView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        if (request.data['name'] == '') or (len(request.FILES) == 0):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        doctor = Doctor.objects.get(user=user)
        degree = Degree.objects.create(doctor=doctor, name=request.data['name'], picture=request.data['picture'])

        return Response("successfully created", status=status.HTTP_201_CREATED)


class DegreeEditView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        degree_pk = request.data['degree_pk']
        user = request.user
        doctor = Doctor.objects.get(user=user)

        degree = get_object_or_404(Degree, pk=degree_pk, doctor=doctor)
        degree.delete()

        return Response("successfully deleted")

    def put(self, request):
        user = request.user
        user_type = user.is_doctor

        if not user_type:
            return Response("user is not doctor", status=status.HTTP_409_CONFLICT)

        degree_pk = request.data['degree_pk']
        doctor = Doctor.objects.get(user=user)
        degree = get_object_or_404(Degree, pk=degree_pk, doctor=doctor)
        serializer = DegreeSerializer(degree, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("successfully updated")
