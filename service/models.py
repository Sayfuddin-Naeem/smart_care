from django.db import models
import os

def get_upload_to(instance, filename):
    return os.path.join('service/images/', filename)

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    image = models.ImageField(upload_to=get_upload_to)
    def __str__(self) -> str:
        return self.name