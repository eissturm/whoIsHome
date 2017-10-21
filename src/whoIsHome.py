#!/usr/bin/env python3
# whoIsHome.py - Checks router DHCP tables, and inputs that into DB
import requests
import os
import sys
import xml.etree.ElementTree as Etree
# your imports, e.g. Django models

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "whoIsHome.settings")
import django
django.setup()
from netmon.models import Device
from django.utils import timezone
from datetime import timedelta


ROUTER_IP = os.environ.get('WH_ROUTER_IP', '192.168.0.1')

# Request DHCP_CLIENTS list from DLINK Router.
r = requests.get('http://{}/dhcp_clients.asp'.format(ROUTER_IP))
# Check if failed
if r.status_code != 200:
    print("There was an error.  {} responded with status code {}".format(
        ROUTER_IP,
        r.status_code
    ))
    sys.exit(r.status_code)

# Parse results into XML tree
clients = [client for client in Etree.fromstring(r.content).findall('client')]
print("Found {} clients".format(len(clients)))


def clients_as_dicts(clients):
    for client in clients:
        client_dict = {}
        for element in client:
            client_dict[element.tag] = element.text
        yield client_dict


for client in clients_as_dicts(clients):
    try:
        c = Device.objects.get(mac_address=client['mac'])
        c.update(name=client['host_name'],
                 known_ip=client['ip_address'])
        print("Updated {}".format(c))
    except Exception as e:
        print("New MAC found.  Registering new device")
        c = Device(name=client['host_name'],
                   known_ip=client['ip_address'],
                   mac_address=client['mac'])
    c.save()

for d in Device.objects.all():
    if d.last_update < timezone.now() - timedelta(minutes=30):
        print("{} is inactive".format(d))
        d.flip_active()

print("Script done!")
