from django.db import models
from django.contrib.auth.models import User
import os

def get_upload_to(instance, filename):
    return os.path.join('patient/images/', filename)

class Patient(models.Model):
    user = models.OneToOneField(User, related_name='patient', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_to)
    mobile_no = models.CharField(max_length=12)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
