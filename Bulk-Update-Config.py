#Version 2.0.0 GUI 
#By Aman Basra
from tkinter import *
import tkinter as TK
from tkinter import scrolledtext
from tkinter import filedialog
import meraki
import pandas as pd
import time

tmp = []

def browse():
    path = filedialog.askopenfilename()
    printCSVPathlbl.config(text=path)
    tmp.append(path)
    return(path)

def getOrgID():
    API_KEY = getAPI.get(1.0, 'end-1c')
    dashboard = meraki.DashboardAPI(API_KEY)
    response = dashboard.organizations.getOrganizations()
    orgidlbl.config(text=response)
    output = []
    for l in response:
        for x in l.values():
            output.append(x)
    orgID = output[0]
    orgName = output[1]
    Output.insert(TK.INSERT, orgName + "\n" + orgID + "\n")
    return orgID, orgName

def getNetworkID():
    orgID = getOrgID()
    API_KEY = getAPI.get(1.0, 'end-1c')
    dashboard = meraki.DashboardAPI(API_KEY)
    response = dashboard.organizations.getOrganizationNetworks(orgID[0])
    data = []
    for l in response:
        for x in l.values():
            data.append(x)
    NetworkID = data[0]
    NetworkName = data[2]
    Output.insert(TK.INSERT, NetworkName + "\n"+ NetworkID + "\n")
    return NetworkID, NetworkName

def update():
    netID = getNetworkID()
    # API Setup
    API_KEY = getAPI.get(1.0, 'end-1c')
    dashboard = meraki.DashboardAPI(API_KEY)
    network_id = netID[0]


    # Import CSV
    cols = ["Name", "Serial", "Notes"]

    df = pd.read_csv(tmp[0], usecols=cols)

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
frame.geometry('1000x500')

APIlbl  = TK.Label(frame, text="API Key", pady=5)
getAPI = TK.Text(frame,
                    height= 1,
                    width = 50,)

CSVPathlbl  = TK.Label(frame, text="CSV", pady=5)
printCSVPathlbl  = TK.Label(frame, text="", pady=5)
orgidlbl  = TK.Label(frame, text="", pady=5)

browseButton =TK.Button(frame, text='Browse', command=browse)
submitButton =TK.Button(frame, text='Submit', command=update)

Output = scrolledtext.ScrolledText(frame, height='20', width='100', wrap="word")

APIlbl.pack()
getAPI.pack()
CSVPathlbl.pack()
printCSVPathlbl.pack()
orgidlbl.pack()
browseButton.pack()
submitButton.pack()

Output.pack()

frame.mainloop()

