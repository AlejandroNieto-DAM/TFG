from ServerPython.Models.Device_Model import Door_Model

class Door_Controller:
    def __init__(self):
        self.__door_model = Door_Model()

    """
    *   @brief Call a model method to get all the devices of the centre in which the student is registered
    *   @param id_student which is the student of we want to know the center to give him the devices
    *   @pre the user and the center have to been registered in the system
    *   @return returns all the devices that arent in maintenance
    """
    def getAllDoors(self, id_student):
        datos = self.__door_model.getAllDoors(id_student)
        return datos

    """
    *   @brief Call a model method to get all the devices of the centre
    *   @param id_center which is the center of we want to know their devices
    *   @pre the center has to been registered in the system
    *   @return returns all the devices that arent in maintenance of the centre
    """
    def getAllDoorsByIdCenter(self, id_center):
        datos = self.__door_model.getAllDoorsByCenterId(id_center)
        return datos

    """
    *   @brief Call a model method to get the status of a specific device
    *   @param id_device which is the id of the device we want to know his status
    *   @pre a center has to been registered and has devices.
    *   @return returns the status of the specific device
    """
    def doorStatus(self, id_device):
        return self.__door_model.doorStatus(id_device)

    """
    *   @brief Call a model method to set the status of a specific device to open
    *   @param id_device which is the id of the device we want to open
    *   @pre the selected device has to be not in maintenance
    *   @post the status of the device will be changed
    """
    def openDoor(self, id_device):
        self.__door_model.openDoor(id_device)

    """
    *   @brief Call a model method to set the status of a specific device to close
    *   @param id_device which is the id of the device we want to close
    *   @pre the selected device has to be not in maintenance
    *   @post the status of the device will be changed
    """
    def closeDoor(self, id_device):
        self.__door_model.closeDoor(id_device)

    """
    *   @brief Call a model method to set the maintenance of a specific device to up
    *   @param id_device which is the id of the device we want to put in maintenance
    *   @pre the selected device has to be not in maintenance
    *   @post the state of maintenance of the device will be changed
    """
    def doorInMaintenance(self, id_device):
        self.__door_model.doorInMaintenance(id_device)

    """
    *   @brief Call a model method to set the maintenance of a specific device to not in maintenance
    *   @param id_device which is the id of the device we want to put not in maintenance
    *   @pre the selected device has to be in maintenance
    *   @post the state of maintenance of the device will be changed
    """
    def doorNotInMaintenance(self, id_device):
        self.__door_model.doorNotInMaintenance(id_device)
