from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# DB table to save Schemas


class Schema(models.Model):
    user_create = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    schema = models.CharField(max_length=600)
    schema_name = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)
    modified = models.CharField(max_length=20)
    generated = models.BooleanField()
    file_path = models.CharField(max_length=255)




