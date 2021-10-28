from .serializers import JWTSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from users.models import User


# Create your views here.
class JWTObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = JWTSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
