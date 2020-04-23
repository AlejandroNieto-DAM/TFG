from Door_Model import Door_Model

class Door_Controller:
    def __init__(self):
        self.door_model = Door_Model()

    def getAllDoors(self):
        datos = self.door_model.getAllDoors()
        return datos

    def doorStatus(self, idDoor):
        return self.door_model.doorStatus(idDoor)

    def openDoor(self, idDoor):
        self.door_model.openDoor(idDoor)
