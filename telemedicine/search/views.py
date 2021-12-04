from rest_framework import filters
from users.models import Doctor
from .serializers import DoctorSearchSerializer
from rest_framework import generics


# Create your views here.


class DoctorSearchView(generics.ListCreateAPIView):
    search_fields = ['degree', 'user__first_name', 'user__last_name']
    filter_backends = (filters.SearchFilter,)
    queryset = Doctor.objects.all()
    serializer_class = DoctorSearchSerializer
    # ordering_fields = ['rate']

