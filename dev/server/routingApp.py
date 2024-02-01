# https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=59.9420%2C30.3851%3B59.9382%2C30.3607

#curl 'http://router.project-osrm.org/route/v1/driving/13.388860,52.517037;13.397634,52.529407;13.428555,52.523219?overview=false'

# import http.client

# conn = http.client.HTTPSConnection("www.openstreetmap.org")

# # headers = {
# #     'X-RapidAPI-Key': "30f5044164msh7d8e19696e327d1p127bbdjsn8ae06efdd89d",
# #     'X-RapidAPI-Host': "opentripmap-places-v1.p.rapidapi.com"
# # }

# conn.request("GET", "/directions?engine=fossgis_osrm_car&route=59.9420%2C30.3851%3B59.9382%2C30.3607")#, headers=headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))

import http.client

connOnFoot = http.client.HTTPConnection("127.0.0.1:5000")
# connOnCar = http.client.HTTPSConnection("router.project-osrm.org")

# headers = {
#     'X-RapidAPI-Key': "30f5044164msh7d8e19696e327d1p127bbdjsn8ae06efdd89d",
#     'X-RapidAPI-Host': "opentripmap-places-v1.p.rapidapi.com"
# }

#59.9420%2C30.3851%3B59.9382%2C30.3607


import json
import time

# data["features"][1]

f = open('data.json')
data = json.load(f)

for startObj in data["features"]:
    for endObj in data["features"]:
        if startObj['id'] == endObj['id']:
            continue
        startLon = startObj['geometry']['coordinates'][0]
        startLat = startObj['geometry']['coordinates'][1]
        endLon = endObj['geometry']['coordinates'][0]
        endLat = endObj['geometry']['coordinates'][1]

        connOnFoot.request("GET", "/route/v1/foot/" + str(startLon) + "," + str(startLat) + ";" + str(endLon) + "," + str(endLat) + "?overview=false")
        resOnFoot = connOnFoot.getresponse()
        dataOnFoot = resOnFoot.read()
        totalResponse = json.loads(dataOnFoot.decode("utf-8"))['routes']
        distance = json.loads(dataOnFoot.decode("utf-8"))['routes'][0]['legs'][0]['distance']


startObj = data["features"][1]
endObj = data["features"][10]
# print(obj['geometry']['coordinates'][0])
# print(obj['geometry']['coordinates'][1])

startLon = startObj['geometry']['coordinates'][0]
startLat = startObj['geometry']['coordinates'][1]
endLon = endObj['geometry']['coordinates'][0]
endLat = endObj['geometry']['coordinates'][1]




start_time = time.time()

# connOnCar.request("GET", "/route/v1/driving/30.3851,59.9420;30.3607,59.9382?overview=false")#, headers=headers)
connOnFoot.request("GET", "/route/v1/foot/" + str(startLon) + "," + str(startLat) + ";" + str(endLon) + "," + str(endLat) + "?overview=false")#, headers=headers)

# resOnCar = connOnCar.getresponse()
resOnFoot = connOnFoot.getresponse()

# dataOnCar = resOnCar.read()
dataOnFoot = resOnFoot.read()

end_time = time.time()

elapsed_time = end_time - start_time
print('Elapsed time: ', elapsed_time)
print('expected total time : ', (elapsed_time * 315 * (315 - 1) / 2) / 60 / 60)

# print(dataOnCar.decode("utf-8"))

print()



print(json.loads(dataOnFoot.decode("utf-8"))['routes'])
print(json.loads(dataOnFoot.decode("utf-8"))['routes'][0]['legs'][0]['distance'])




