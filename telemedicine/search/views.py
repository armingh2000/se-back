from degrees.models import Degree
from users.models import Doctor
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from degrees.serializers import DegreeSerializer
from .serializers import DoctorSearchSerializer


# Create your views here.

class DoctorSearchView(APIView):
    def get(self, request):
        query = request.GET['query']

        if query.strip() == '':
            return Response('query is empty', status=status.HTTP_400_BAD_REQUEST)

        degree_queryset = Degree.objects.filter(
            Q(name__contains=query)
        )

        doctor_queryset = Doctor.objects.filter(
            Q(user__first_name__contains=query) |
            Q(user__last_name__contains=query)
        )

        doctors = []

        for degree in degree_queryset:
            doctor = degree.doctor

            if doctor not in doctors:
                doctors.append(degree.doctor)

        for doctor in doctor_queryset:
            if doctor not in doctors:
                doctors.append(doctor)

        doctors_list = []

        for doctor in doctors:
            degrees = Degree.objects.filter(doctor=doctor)
            degs = DegreeSerializer(degrees, many=True).data

            doc = DoctorSearchSerializer(doctor, many=False).data
            doc['degrees'] = degs

            doctors_list.append(doc)


        return Response(doctors_list)



