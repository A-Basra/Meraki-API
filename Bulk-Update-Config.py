#Version 2.0.0 GUI 
#By Aman Basra

import tkinter as TK
from tkinter import filedialog
import meraki
import pandas as pd
import time

path = None
orgID = None

def browse():
    path = filedialog.askdirectory()
    return(path)

def getOrgID():
    API_KEY = getAPI.get(1.0, 'end-1c')
    dashboard = meraki.DashboardAPI(API_KEY)
    response = dashboard.organizations.getOrganizations()
    orgidlbl.config(text=response)
    return response

def update():
    # API Setup
    API_KEY = getAPI.get(1.0, 'end-1c')
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

#Create GUI Window
frame = TK.Tk()
frame.title("Meraki Bulk Update Tool")
frame.geometry('500x500')

APIlbl  = TK.Label(frame, text="API Key", anchor= "w", pady=5)
getAPI = TK.Text(frame,
                    height= 1,
                    width = 50,)

CSVPathlbl  = TK.Label(frame, text="CSV", anchor= "w", pady=5)
printCSVPathlbl  = TK.Label(frame, text=path, anchor= "w", pady=5)
orgidlbl  = TK.Label(frame, text="", anchor= "w", pady=5)

browseButton =TK.Button(frame, text='Browse', command=browse)

submitButton =TK.Button(frame, text='Submit', command=getOrgID)


APIlbl.pack()
getAPI.pack()
CSVPathlbl.pack()
printCSVPathlbl.pack()
orgidlbl.pack()
browseButton.pack()
submitButton.pack()

frame.mainloop()

