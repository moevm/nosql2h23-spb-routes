from DBdriver import DataBaseDriver

class ServerLogic:
    def __init__(self):
        self.__dataBaseDriver = DataBaseDriver("bolt://localhost:7687", "neo4j", "Andrew_07072002")

    def isUserExists(self):
        pass

    def getUserByEmail(self, email : str):
        return self.__dataBaseDriver.getUserByEmail(email)

    def createUser(self, user:dict):
        return self.__dataBaseDriver.createUser(user)
    