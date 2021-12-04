from django.urls import path
from .views import *


urlpatterns = [
    # Doctor Search
    path('', DoctorSearchView.as_view(), name='rest_search'),
]
