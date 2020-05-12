from Models.Device_Model import Door_Model

class Door_Controller:
    def __init__(self):
        self.__door_model = Door_Model()

    def getAllDoors(self, id_student):
        datos = self.__door_model.getAllDoors(id_student)
        return datos

    def getAllDoorsByIdCenter(self, id_center):
        datos = self.__door_model.getAllDoorsByCenterId(id_center)
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
