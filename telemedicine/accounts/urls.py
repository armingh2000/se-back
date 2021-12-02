from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    # User Profile Preview
    path('profile/', UserProfileView.as_view(), name='rest_profile_preview'),

    # User Profile Edit
    path('profile/edit/', UserEditView.as_view(), name='rest_profile_edit'),

    # User Type Creation
    path('create_type', UserCreateTypeView.as_view(), name='rest_create_user_type'),
]
