from django.urls import path
from .views import *


urlpatterns = [
    # Rate Edit
    path('edit/', RateEditView.as_view(), name='rest_edit_rate'),

    # Rate Add
    path('add/', RateAddView.as_view(), name='rest_add_rate'),

]



