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
    
    def createSightRoute(self, startNode, finishNode, route):
        with self.driver.session() as session:
            # greeting = session.execute_write(self._create_and_return_greeting, message)
            nodeName = session.execute_write(self._create_route_between_sights_return_name, startNode, finishNode, route)
            return nodeName

    @staticmethod  
    def _get_user_by_email(tx, email):
        query = "match (a:User) where a.email = '"+ email +"' return a"
        result = tx.run(query)
        # values = [record.values() for record in result]
        # return values
        return result.single().value()._properties

    def getUserByEmail(self, email):
        with self.driver.session() as session:
            values = session.execute_read(self._get_user_by_email, email)
            return values
        

    @staticmethod  
    def _get_user_roles_by_email(tx, email):
        query = "MATCH (r:User {email:'"+ email +"'}) RETURN labels(r);"
        result = tx.run(query)
        
        return result.single().value()


    def getUserRolesByEmail (self, email):
        with self.driver.session() as session:
            values = session.execute_read(self._get_user_roles_by_email, email)
            return values

    @staticmethod  
    def _get_all_routes(tx):
        query = "match (n:UserRoute) return n"
        result = tx.run(query)
        return [record for record in result.data()]

    def getAllRoutes(self):
        with self.driver.session() as session:
            values = session.execute_read(self._get_all_routes)
            return values


    @staticmethod 
    def _get_all_sight_labels(tx):
        query = "MATCH (a:Sight) WITH LABELS(a) AS temp UNWIND temp AS LABELLIST return DISTINCT LABELLIST;"
        result = tx.run(query)
        return [record for record in result.data()]

    def getAllSightLabels(self):
        with self.driver.session() as session:
            values = session.execute_read(self._get_all_sight_labels)
            return values

        
    
    @staticmethod
    def _create_User(tx, newUser):
        query = ("CREATE (:User {email : $email,\
                                password : $password,\
                                firstName : $firstName,\
                                lastName : $lastName,\
                                phone : $phone,\
                                address : $address})")
        result = tx.run(query, 
                            email = newUser['email'],
                            password = newUser['password'],
                            firstName = newUser['firstName'],
                            lastName = newUser['lastName'],
                            phone = newUser['phone'],
                            address = newUser['address'])
        
        return result
    
    def createUser(self, newUser):
        with self.driver.session() as session:
            # greeting = session.execute_write(self._create_and_return_greeting, message)
            nodeName = session.execute_write(self._create_User, newUser)
            return nodeName


    @staticmethod  
    def _get_sights_in_bbox(tx, bbox):
        query = "match (a:Sight) where a.lat > $latMin \
                                    and a.lat < $latMax \
                                    and a.lon > $lonMin \
                                    and a.lon < $lonMax \
                                    return a.id, a.lat, a.lon"
        result = tx.run(query,
                        latMin = bbox['latMin'],
                        latMax = bbox['latMax'],
                        lonMin = bbox['lonMin'],
                        lonMax = bbox['lonMax'])
        values = [record.values() for record in result]
        return values
        # return result

    def getSightsInBbox(self, bbox):
        with self.driver.session() as session:
            values = session.execute_read(self._get_sights_in_bbox, bbox)
            return values
        

    @staticmethod  
    def _get_sight_by_id(tx, id):
        query = "match (a:Sight) where a.id = '"+ str(id) +"' return a"
        result = tx.run(query)
        # values = [record.values() for record in result]
        # return values
        return result.single().value()._properties

    def getSightById(self, id):
        with self.driver.session() as session:
            values = session.execute_read(self._get_sight_by_id, id)
            return values
        
    @staticmethod  
    def _generate_routes_by_start_point(tx, startPoint, stringWithTags):
        query = "MATCH (node)\
                WHERE exists(node.lat) AND exists(node.lon)\
                WITH node, distance(point({latitude: node.lat, longitude: node.lon}), point({latitude: "+str(startPoint['lat'])+", longitude: "+str(startPoint['lon'])+"})) AS dist\
                MATCH (p:Sight {name:node.name})\
                CALL apoc.path.expand(p, 'FOOT_ROUTE', "+stringWithTags+", 2, 4)\
                YIELD path\
                RETURN nodes(path), relationships(path), length(path) AS hops\
                ORDER BY dist, hops\
                LIMIT 5"
        result = tx.run(query)
        # values = [record.values() for record in result]
        # return values
        return [{"nodes" : [dict(nodes) for nodes in paths.values()[0]],
                  "relationships" : [dict(arrow) for arrow in paths.values()[1]], 
                  "length": paths.values()[2]} for paths in result]

    def generateRoutesByStartPoint(self, startPoint, stringWithTags):
        with self.driver.session() as session:
            values = session.execute_read(self._generate_routes_by_start_point, startPoint, stringWithTags)
            return values
        

    @staticmethod  
    def _generate_routes_by_start_and_finish_point(tx, startPoint, endPoint, stringWithTags, body):
        print('startPoint[id]', startPoint['id'])
        print('endPoint[id]', endPoint['id'])
        query = "MATCH (p:Sight {id: '"+startPoint['id']+"'})\
                MATCH (joe:Sight {id: '"+endPoint['id']+"'})\
                CALL apoc.path.expandConfig(p, {\
                    relationshipFilter: 'FOOT_ROUTE',\
                    labelFilter: "+stringWithTags+",\
                    minLevel: 1,\
                    maxLevel: "+str(body["numberOfSightsOnTheRoute"])+",\
                    terminatorNodes: [joe]\
                })\
                YIELD path\
                RETURN nodes(path), length(path) AS hops\
                ORDER BY hops\
                LIMIT 3"
        
        result = tx.run(query)
        # print(dict(result))
        print()
        values = [record.values() for record in result]
        return [{"sightsSubsequenceIds" : [dict(node)['id'] for node in routes[0] ], "name" : routes[1]} for routes in values]

        # return [{"nodes" : [dict(nodes) for nodes in paths.values()[0]],
        #           "relationships" : [dict(arrow) for arrow in paths.values()[1]], 
        #           "length": paths.values()[2]} for paths in result]

    def generateRoutesByStartAndFinishPoint(self, startPoint, endPoint, stringWithTags, body):
        with self.driver.session() as session:
            values = session.execute_read(self._generate_routes_by_start_and_finish_point, startPoint, endPoint, stringWithTags, body)
            return values
        

    @staticmethod  
    def _find_the_nearest_point(tx, pointToAproximate):
        query = "MATCH (node)\
                WHERE exists(node.lat) AND exists(node.lon)\
                WITH node, distance(point({latitude: node.lat, longitude: node.lon}), point({latitude: "+str(pointToAproximate['lat'])+", longitude: "+str(pointToAproximate['lon'])+"})) AS dist\
                RETURN node, dist\
                ORDER BY dist\
                LIMIT 1"
        result = tx.run(query)
        # values = [record.values() for record in result]
        # return values
        return [dict(dict(point)['node']) for point in result]

    def findTheNearestPoint(self, pointToAproximate):
        with self.driver.session() as session:
            values = session.execute_read(self._find_the_nearest_point, pointToAproximate)
            return values
        

    @staticmethod
    def _create_User_route(tx, user, route):
        query = (
                "CREATE (ur:UserRoute{id : '"+ route["id"] +"',\
                                     name : '"+ route["name"] +"',\
                                     description : '"+ route["description"] +"', \
                                     sightsSubsequenceIds : " + route["sightsSubsequenceIds"] + "})\
                WITH ur \
                MATCH (user:User)\
                WHERE user.email = '"+user["email"]+"' \
                CREATE (user)-[:IS_AUTHOR]->(ur)\
                WITH ur\
                MATCH (sight:Sight)\
                WHERE sight.id IN ur.sightsSubsequenceIds \
                CREATE (ur)-[:CONTAINS]->(sight)"
                )
                
        result = tx.run(query)
        record = result.single()
        return record
        
    def createUserRoute(self, user, route):
        with self.driver.session() as session:
            # greeting = session.execute_write(self._create_and_return_greeting, message)
            nodeName = session.execute_write(self._create_User_route, user, route)
            return nodeName
    
    @staticmethod  
    def _export_all_ti_json(tx):
        query = "CALL apoc.export.json.all('all.json',{useTypes:true});"
        result = tx.run(query)
        # values = [record.values() for record in result]
        # return values
        return result.value()

    def exportAllToJSON(self):
        with self.driver.session() as session:
            values = session.execute_read(self._export_all_ti_json)
            return values
        
    
    @staticmethod  
    def _check_if_users_exist(tx):
        query = "match (n:User) return n"
        result = tx.run(query)
        # values = [record.values() for record in result]
        # return values
        return result.value()

    def checkIfUsersExist(self):
        with self.driver.session() as session:
            values = session.execute_read(self._check_if_users_exist)
            return values


    @staticmethod
    def _create_Default_User(tx):
        query = ('CREATE (:User {email : "user@gmail.com",password : "2301",firstName : "Andrew",lastName : "Zlobin",phone : "89530595753",address : "Saint Petersburg"})')
        result = tx.run(query,)
        
        return result
    
    def createDefaultUser(self):
        with self.driver.session() as session:
            # greeting = session.execute_write(self._create_and_return_greeting, message)
            nodeName = session.execute_write(self._create_Default_User)
            return nodeName
    
    @staticmethod
    def _create_Default_Admin(tx):
        query = ('CREATE (:User:Admin {email : "admin@gmail.com",password : "2301",firstName : "Andrew",lastName : "Admin",phone : "89530595753",address : "Saint Petersburg"})')
        result = tx.run(query)
        
        return result
    
    def createDefaultAdmin(self):
        with self.driver.session() as session:
            # greeting = session.execute_write(self._create_and_return_greeting, message)
            nodeName = session.execute_write(self._create_Default_Admin)
            return nodeName

    

if __name__ == "__main__":
    loader = DataBaseDriver("bolt://0.0.0.0:7687", "neo4j", "Andrew_07072002")
    f = open('data.json')
    data = json.load(f)

    createNodes = False
    createRoutes = False


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

    print(loader.checkIfUsersExist() == [])

    loader.close()
    f.close()

    # print(type(loader.getUserByEmail('zlobinandrey0707@gmail.com')))
    # bbox = {'latMin' : 59.92991679946971,
    #         'latMax' : 59.931309097050196,
    #         'lonMin' : 30.361646111301685,
    #         'lonMax' : 30.368458922200304}
    # print (loader.getSightById(7099552))



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