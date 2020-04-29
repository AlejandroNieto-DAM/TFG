from ServerPython.venv.Models.Door_Model import Door_Model

class Door_Controller:
    def __init__(self):
        self.__door_model = Door_Model()

    def getAllDoors(self):
        datos = self.__door_model.getAllDoors()
        return datos

    def doorStatus(self, idDoor):
        return self.__door_model.doorStatus(idDoor)

    def openDoor(self, idDoor):
        self.__door_model.openDoor(idDoor)

    def closeDoor(self, idDoor):
        self.__door_model.closeDoor(idDoor)

    def doorInMaintenance(self, idDoor):
        self.__door_model.doorInMaintenance(idDoor)

    def doorNotInMaintenance(self, idDoor):
        self.__door_model.doorNotInMaintenance(idDoor)
