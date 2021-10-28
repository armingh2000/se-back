from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from users.models import User
from django.contrib.auth.hashers import make_password


class JWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # admin / not admin
        return token

    def validate(self, attrs):
        credentials = {"username": "", "password": attrs.get("password")}

        user = User.objects.filter(email=attrs.get("username")).first()
        email_address = EmailAddress.objects.filter(user=user, verified=True).exists()

        if email_address and user:
            credentials["username"] = user.username
            return super().validate(credentials)
        elif user and not email_address:
            return {"message": "Email not verified"}
        else:
            return {"message": "This email does not exist, please create a new account"}


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=250,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            UnicodeUsernameValidator(),
        ],
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields do not match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            password=make_password(validated_data["password"]),
        )

        user.save()

        return user

    def __str__(self):
        return self.username
