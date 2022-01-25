from .models import Rate
from users.models import Doctor, Patient
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class RateAddView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user

        if not user.is_patient:
            return Response('user must be patient to rate', status=status.HTTP_409_CONFLICT)

        if not request.data['rate']:
            return Response('field cannot be empty', status.HTTP_400_BAD_REQUEST)

        if isinstance(request.data['doctor_pk'], str):
            return Response('invalid pk', status.HTTP_400_BAD_REQUEST)

        doctor = get_object_or_404(Doctor, pk=request.data['doctor_pk'])

        if doctor.user == user:
            return Response('patient and doctor are same', status.HTTP_400_BAD_REQUEST)

        patient = Patient.objects.get(user=user)

        if Rate.objects.filter(doctor=doctor, patient=patient).exists():
            return Response('patient cannot double rate', status.HTTP_409_CONFLICT)

        if isinstance(request.data['rate'], str) or int(request.data['rate']) < 0 or int(request.data['rate']) > 5:
            return Response('invalid rate', status.HTTP_400_BAD_REQUEST)

        Rate.objects.create(doctor=doctor, patient=patient, rate=request.data['rate'])

        return Response("successfully created", status=status.HTTP_201_CREATED)


class RateEditView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        rate_pk = request.data['rate_pk']
        user = request.user
        patient = get_object_or_404(Patient, user=user)

        rate = get_object_or_404(Rate, pk=rate_pk, patient=patient)
        rate.delete()

        return Response("successfully deleted")

    def put(self, request):
        rate_pk = request.data['rate_pk']
        user = request.user

        if not user.is_patient:
            return Response('user must be patient to rate', status=status.HTTP_409_CONFLICT)

        if not request.data['rate']:
            return Response('field cannot be empty', status.HTTP_400_BAD_REQUEST)

        if isinstance(request.data['rate'], str) or int(request.data['rate']) < 0 or int(request.data['rate']) > 5:
            return Response('invalid rate', status.HTTP_400_BAD_REQUEST)

        if isinstance(request.data['rate_pk'], str):
            return Response('invalid pk', status.HTTP_400_BAD_REQUEST)


        patient = Patient.objects.get(user=user)
        rate = get_object_or_404(Rate, pk=rate_pk, patient=patient)
        rate.rate = request.data['rate']
        rate.save()

        return Response("successfully updated")
