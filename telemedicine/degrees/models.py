from django.db import models
from users.models import Doctor


# Create your models here.

class Degree(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='%(class)s_doctor')
    name = models.CharField(max_length=30)
    picture = models.ImageField(upload_to='degrees')


