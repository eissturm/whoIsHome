#!/usr/bin/env python3
# whoIsHome.py - Checks router DHCP tables, and inputs that into DB

import requests
import os
import sys
import xml.etree.ElementTree as Etree

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

for client in clients:
    client_dict = {}
    for element in client:
        client_dict[element.tag] = element.text
    print(client_dict)
