from django.urls import path
from .views import *


urlpatterns = [
    # Degree Edit
    path('edit/', DegreeEditView.as_view(), name='rest_edit_degree'),

    # Degree Add
    path('add/', DegreeAddView.as_view(), name='rest_add_degree'),

]



