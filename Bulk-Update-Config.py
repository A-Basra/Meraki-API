#Version 1.0.1

import meraki
import pandas as pd
import time

# API Setup
API_KEY = '<API_KEY>'
dashboard = meraki.DashboardAPI(API_KEY)
network_id = '<NETWORK-ID>'


# Import CSV
cols = ["Name", "Serial", "Notes"]

df = pd.read_csv("<PATH TO CSV>", usecols=cols)

Serials = []
Assets = []
Names = []

# Convert to string
for l in df["Serial"]:
    Serials.append(str(l))

for l in df["Notes"]:
    Assets.append(str(l))

for l in df["Name"]:
    Names.append(str(l))

# Submit request for each line in CSV

for num, asset in enumerate(Assets):
    try:
        device_fields = {'name': Names[num], 'notes': asset}
        print(device_fields)
        response = dashboard.sm.updateNetworkSmDevicesFields(
            network_id, device_fields,
            serial=Serials[num]
        )
        print(response)
    except:
        continue
