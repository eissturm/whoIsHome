from django.contrib import admin
from .models import Device
# Register your models here.


class DeviceAdmin(admin.ModelAdmin):
    model = Device
    list_display = ('name', 'known_ip', 'last_update')

admin.site.register(Device, DeviceAdmin)
