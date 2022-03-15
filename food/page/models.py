from django.db import models
from django.utils import (
    timezone
)

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    

class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)