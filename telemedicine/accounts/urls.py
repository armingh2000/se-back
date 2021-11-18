from django.urls import path, include, re_path
from .views import UserProfileView


urlpatterns = [
    # User Profile (Preview)
    path('profile/', UserProfileView.as_view()),
]
