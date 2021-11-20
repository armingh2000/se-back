from django.urls import path, include, re_path
from .views import UserProfileView, UserEditView


urlpatterns = [
    # User Profile Preview
    path('profile/', UserProfileView.as_view()),

    # User Profile Edit
    path('profile/edit/', UserEditView.as_view(), name='rest_edit')
]
