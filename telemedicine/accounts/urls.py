from django.urls import path
from .views import *


urlpatterns = [
    # user profile preview
    path('profile/', UserProfileView.as_view(), name='rest_profile_preview'),

    # user profile edit
    path('profile/edit/', UserEditView.as_view(), name='rest_profile_edit'),

    # user type creation
    path('create_type/', UserCreateTypeView.as_view(), name='rest_create_user_type'),

]
