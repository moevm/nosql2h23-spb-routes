from DBdriver import DataBaseDriver

import uuid


class ServerLogic:
    def __init__(self):
        self.__dataBaseDriver = DataBaseDriver("bolt://localhost:7687", "neo4j", "Andrew_07072002")

    def isUserExists(self):
        pass

    def getUserByEmail(self, email : str):
        return self.__dataBaseDriver.getUserByEmail(email)

    def createUser(self, user:dict):
        return self.__dataBaseDriver.createUser(user)
    

    def getSightInArea(self, area):
        bbox = {'latMin' : area['extent']['bottom'],
            'latMax' : area['extent']['top'],
            'lonMin' : area['extent']['left'],
            'lonMax' : area['extent']['right']}
        
        listOfSightsIdsAndPos = self.__dataBaseDriver.getSightsInBbox(bbox)
        listOfSightsIdsAndPos = [{'id' : i[0],
                                  'lat' : i[1],
                                  'lon' : i[2]} for i in listOfSightsIdsAndPos]
        return listOfSightsIdsAndPos
    
    def getSightById(self, id):
        return self.__dataBaseDriver.getSightById(id)
    
    def createNewRoute(self, user, newRoute):
        name = newRoute['newRouteName']
        description = newRoute['newRouteDescription']
        sightsSubsequenceIds = [i["id"] for i in newRoute["newRouteList"]]
        route = {"id" : str(uuid.uuid4()),
                 "name" : name,
                 "description" : description,
                 "sightsSubsequenceIds": str(sightsSubsequenceIds)}
        self.__dataBaseDriver.createUserRoute(user, route)