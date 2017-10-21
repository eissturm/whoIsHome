from django.db import models
from django.utils import timezone

# Create your models here.
class Device(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    known_ip = models.CharField(max_length=64)
    mac_address = models.CharField(max_length=64, unique=True)
    created_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def flip_active(self):
        self.active = not self.active
        self.save()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v
        self.last_update = timezone.now()
        self.save()
