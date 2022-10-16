from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import authenticate
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(blank=True, max_length=11)

class Logs(models.Model):
    logs_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_logs")
    status = models.CharField(max_length=10)
    timestamp = models.DateTimeField(default=timezone.now)
