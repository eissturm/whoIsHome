from django.db import models
from django.utils import timezone

# Create your models here.
class Device(models.Model):
    owner = models.ForeignKey('auth.user', null=True)
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    known_ip = models.CharField(max_length=64)
    mac_address = models.CharField(max_length=64, unique=True)
