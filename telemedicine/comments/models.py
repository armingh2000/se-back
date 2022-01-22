from django.db import models
from users.models import Doctor, Patient

# Create your models here.

class Comment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='%(class)s_doctor')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='%(class)s_patient')
    body = models.TextField(max_length=1e+4)
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']
