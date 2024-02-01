# import os

# print(__file__)
# print(os.path.abspath(os.path.join( os.path.dirname(__file__), '..', 'client', 'pages')))

import http.client

conn = http.client.HTTPSConnection("opentripmap-places-v1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "30f5044164msh7d8e19696e327d1p127bbdjsn8ae06efdd89d",
    'X-RapidAPI-Host': "opentripmap-places-v1.p.rapidapi.com"
}

conn.request("GET", "/en/places/bbox?lon_max=30.3450&lat_min=59.9325&lon_min=30.3307&lat_max=59.9372", headers=headers)
# conn.request("GET", "/en/places/bbox?lon_max=30.420626&lat_min=59.884713&lon_min=30.348598&lat_max=59.939402", headers=headers)

res = conn.getresponse()
data = res.read()


f = open("data.json", "a")
f.write(data.decode("utf-8"))
f.close()

#open and read the file after the appending:
# f = open("data.json", "r")
# print(f.read())