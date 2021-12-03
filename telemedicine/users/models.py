from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(ugettext_lazy('Users must have an email address'))

        if not password:
            raise ValueError(ugettext_lazy('Users must have a password'))

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name  = models.CharField(max_length=30, blank=True)
    gender = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['is_doctor']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    medical_record = models.TextField(max_length=1e+4, blank=True)
    height = models.IntegerField(
        validators=[
            MaxValueValidator(500),
            MinValueValidator(0)
        ],
        default=0
    )
    weight = models.FloatField(
        validators=[
            MaxValueValidator(500),
            MinValueValidator(0)
        ],
        default=0
    )


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    degree = models.IntegerField(
        validators=[
            MaxValueValidator(3),
            MinValueValidator(0)
        ],
        default=0
    )
    degree_picture = models.ImageField(upload_to='degrees', blank=True)
    cv = models.TextField(max_length=1e+4, blank=True)
    location = models.TextField(max_length=1e+4, blank=True)
