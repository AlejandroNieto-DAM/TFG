from Models.DeviceModel import DeviceModel
from Models.CenterModel import CenterModel


class DoorController:
    def __init__(self):
        self.__door_model = DeviceModel()
        self.__center_model = CenterModel()

    """
    *   @brief Call a model method to get all the devices of the centre in which the student is registered
    *   @param id_student which is the student of we want to know the center to give him the devices
    *   @pre the user and the center have to been registered in the system
    *   @return returns all the devices that arent in maintenance
    """

    def get_all_doors(self, id_student):
        datos = self.__door_model.get_all_devices(id_student)
        return datos

    """
    *   @brief Call a model method to get all the devices of the centre
    *   @param id_center which is the center of we want to know their devices
    *   @pre the center has to been registered in the system
    *   @return returns all the devices that arent in maintenance of the centre
    """

    def get_all_doors_by_id_center(self, id_center):
        datos = self.__door_model.get_all_devices_by_center_id(id_center)
        return datos

    """
    *   @brief Call a model method to get the status of a specific device
    *   @param id_device which is the id of the device we want to know his status
    *   @pre a center has to been registered and has devices.
    *   @return returns the status of the specific device
    """

    def door_status(self, id_device):
        return self.__door_model.devices_status(id_device)

    """
    *   @brief Call a model method to set the status of a specific device to open
    *   @param id_device which is the id of the device we want to open
    *   @pre the selected device has to be not in maintenance
    *   @post the status of the device will be changed
    """

    def open_door(self, id_device):
        self.__door_model.open_device(id_device)

    """
    *   @brief Call a model method to set the status of a specific device to close
    *   @param id_device which is the id of the device we want to close
    *   @pre the selected device has to be not in maintenance
    *   @post the status of the device will be changed
    """

    def close_door(self, id_device):
        self.__door_model.close_device(id_device)

    def get_door_by_id(self, id_device):
        data = self.__door_model.get_device_by_id(id_device)
        return data

    def delete_device_by_id(self, id_device):
        self.__door_model.delete_device_by_id(id_device)

    def add_device(self, id_admin, name, state, maintenance, pin_led, pin_button, pin_servo):
        id_center = self.__center_model.get_center_by_id_admin(id_admin)
        self.__door_model.add_device(id_center, name, state, maintenance, pin_led, pin_button, pin_servo)

    def update_device_by_id(self, id_device, name, state, maintenance, pin_led, pin_button, pin_servo):
        self.__door_model.update_device_by_id(id_device, name, state, maintenance, pin_led, pin_button, pin_servo)

    def get_devices_for_center(self, id_center):
        return self.__door_model.get_devices_for_center(id_center)

    """
        *   @brief Call a model method to get all the devices of the centre
        *   @param id_center which is the center of we want to know their devices
        *   @pre the center has to been registered in the system
        *   @return returns all the devices that arent in maintenance of the centre
        """

    def get_all_doors_by_id_center_to_web(self, id_center):
        datos = self.__door_model.get_all_doors_by_id_center_for_web(id_center)
        return datos
