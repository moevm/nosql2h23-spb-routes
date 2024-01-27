from neo4j import GraphDatabase
import json

import http.client

from http.client import RemoteDisconnected

class DataBaseDriver:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def createSightNode(self, node):
        with self.driver.session() as session:
            # greeting = session.execute_write(self._create_and_return_greeting, message)
            nodeName = session.execute_write(self._create_sight_return_name, node)
            return nodeName

    @staticmethod
    def _create_sight_return_name(tx, node):
        query = ("CREATE (node"+str(node['id'])+":Sight:"+(':'.join(node['properties']['kinds'].split(',')))+" {type: $type,\
                                    id: $id,\
                                    lon : $lon,\
                                    lat : $lat,\
                                    name : $name,\
                                    rate : $rate,\
                                    properties : $properties,\
                                    kinds : $kinds,\
                                    lat : $lat}) "
             "RETURN node"+str(node['id'])+".name AS nodeName")
        result = tx.run(query, 
                            type = node['type'],
                            id = node['id'],
                            # geometry = node['geometry'],
                            lon = node['geometry']['coordinates'][0],
                            lat = node['geometry']['coordinates'][1],
                            name = node['properties']['name'],
                            rate = node['properties']['rate'],
                            properties = str(node['properties']),
                            kinds = node['properties']['kinds'])
        record = result.single()
        return record
    
    def createSightRoute(self, startNode, finishNode, route):
        with self.driver.session() as session:
            # greeting = session.execute_write(self._create_and_return_greeting, message)
            nodeName = session.execute_write(self._create_route_between_sights_return_name, startNode, finishNode, route)
            return nodeName
        

    @staticmethod
    def _create_route_between_sights_return_name(tx, startNode, finishNode, route):
        query = ("MATCH (start:Sight), (end:Sight) WHERE start.id = $startId AND end.id = $endId "
                "CREATE (start)-[r:FOOT_ROUTE {distance:$distance, totalResponse:$totalResponse}]->(end) "
                "RETURN start,end"
                )
                
        result = tx.run(query, 
                            startId = startNode['id'],
                            endId = finishNode['id'],
                            # geometry = node['geometry'],
                            distance = route['routes'][0]['legs'][0]['distance'],
                            totalResponse = str(route))
        record = result.single()
        return record


if __name__ == "__main__":
    loader = DataBaseDriver("bolt://localhost:7687", "neo4j", "Andrew_07072002")
    f = open('data.json')
    data = json.load(f)

    createNodes = True
    createRoutes = True


    if createNodes:
        print ('start creating nodes')
        for obj in data['features']:
            loader.createSightNode(obj)
        print('success')

    if createRoutes:
        connOnFoot = http.client.HTTPConnection("127.0.0.1:5000")
        print ('start creating routes')
        for startObjidx in range(len(data["features"])):
            startObj = data["features"][startObjidx]
            for endObjIdx in range(startObjidx, len(data["features"])):
                endObj = data["features"][endObjIdx]
                if startObj['id'] == endObj['id']:
                    continue
                startLon = startObj['geometry']['coordinates'][0]
                startLat = startObj['geometry']['coordinates'][1]
                endLon = endObj['geometry']['coordinates'][0]
                endLat = endObj['geometry']['coordinates'][1]

                connOnFoot.request("GET", "/route/v1/foot/" + str(startLon) + "," + str(startLat) + ";" + str(endLon) + "," + str(endLat) + "?overview=false")
                try:
                    resOnFoot = connOnFoot.getresponse()
                except RemoteDisconnected:
                    print("point : ")
                    print('startLon = ', startLon, 'startLat = ', startLat)
                    print('endLon = ', endLon, 'endLat = ', endLat)
                    print ()
                    continue
                dataOnFoot = resOnFoot.read()
                # totalResponse = json.loads(dataOnFoot.decode("utf-8"))['routes']
                # distance = json.loads(dataOnFoot.decode("utf-8"))['routes'][0]['legs'][0]['distance']
                loader.createSightRoute(startObj, endObj, json.loads(dataOnFoot.decode("utf-8")))

        print('success')


    loader.close()
    f.close()




# query = ("""CREATE (node$id:Sight {type: $type,
#                                     id: $id,
#                                     lon : $lon,
#                                     lat : $lat,
#                                     name : $name,
#                                     rate : $rate,
#                                     osm : $osm,
#                                     wikidata : $wikidata,
#                                     kinds : $kinds,
#                                     lat : $lat}) """
#              "RETURN $id .name AS nodeName")
#         result = tx.run(query, 
#                             type = node['type'],
#                             id = node['id'],
#                             # geometry = node['geometry'],
#                             lon = node['geometry']['coordinates'][0],
#                             lat = node['geometry']['coordinates'][1],
#                             name = node['properties']['name'],
#                             rate = node['properties']['rate'],
#                             osm = node['properties']['osm'],
#                             wikidata = node['properties']['wikidata'],
#                             kinds = node['properties']['kinds'])





# import json
 
# # Opening JSON file
# f = open('data.json')
 
# # returns JSON object as 
# # a dictionary
# data = json.load(f)
 
# # Iterating through the json
# # list
# print(data.keys())
# # print(data["type"])

# # print(len(data["features"]))
# # print(data["features"][1]['type'])
# # print(data["features"][1]['id'])
# print('is = ', type(data["features"][1]['id']))
# # # print(data["features"][1]['properties'])
# # print(data["features"][1]['properties']['name'])
# # print(data["features"][1]['properties']['rate'])
# # print(data["features"][1]['properties']['osm'])
# # print(data["features"][1]['properties']['wikidata'])
# # print(data["features"][1]['properties']['kinds'])

# # count_empty=0
# # for obj in data['features']:
# #     # print(['properties']['name'])
# #     if obj['properties']['name'] == '':
# #         count_empty += 1

# # print('count_empty = ', count_empty)

# objs_names = [obj['geometry']['type'] for obj in data['features']]
# # objs_ids = [obj['id'] for obj in data['features']]



# # uniq_names_list = list(set(objs_names))
# # uniq_ids_list = list(set(objs_ids))

# # num_values = len(uniq_names_list)
# # num_ids_values = len(uniq_ids_list)

# from collections import Counter

# print([(item, count) for item, count in Counter(objs_names).items() if count > 1])




# # print(num_values)
# # print(objs_names)

# print(len(data))

 
# # Closing file
# f.close()