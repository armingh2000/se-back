from django.db import models
from users.models import Doctor, Patient
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Rate(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='%(class)s_doctor')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='%(class)s_patient')
    rate = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']
