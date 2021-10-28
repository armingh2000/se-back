from django.urls import path
from .views import JWTObtainTokenPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', JWTObtainTokenPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('register/', RegisterView.as_view()),
]
