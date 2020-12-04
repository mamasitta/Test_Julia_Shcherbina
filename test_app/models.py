from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# DB table to save Schemas

# class Schemas(models.Model):
#     user_create = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author1")
#     full_name = models.CharField(max_length=255, blank=True, null=True)
#     job = models.CharField(max_length=255, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     domain_name = models.CharField(max_length=255, blank=True, null=True)
#     phone_number = models.CharField(max_length=10, blank=True, null=True)
#     company_name = models.CharField(max_length=255, blank=True, null=True)
#     text = models.TextField(blank=True, null=True)
#     integer_from = models.IntegerField(blank=True, null=True)
#     integer_to = models.IntegerField(blank=True, null=True)
#     address = models.CharField(max_length=255, null=True, blank=True)
#     date = models.DateTimeField(auto_now_add=True)


class CsvStorage(models.Model):
    user_create = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    file_name = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    file_path = models.CharField(max_length=255)


class Schema(models.Model):
    user_create = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    schema = models.CharField(max_length=600)
    schema_name = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)
    modified = models.CharField(max_length=20)
