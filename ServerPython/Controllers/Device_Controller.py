from Models.DeviceModel import DeviceModel
from Models.CenterModel import CenterModel


class DeviceController:
    def __init__(self):
        self.__door_model = DeviceModel()
        self.__center_model = CenterModel()

    """
    *   @brief Call a model method to get all the devices of the centre in which the student is registered
    *   @param id_student which is the student of we want to know the center to give him the devices
    *   @pre the user and the center have to been registered in the system
    *   @return returns all the devices that arent in maintenance
    """

    def get_all_devices(self, id_student):
        datos = self.__door_model.get_all_devices(id_student)
        return datos

    """
    *   @brief Call a model method to get all the devices of the centre
    *   @param id_center which is the center of we want to know their devices
    *   @pre the center has to been registered in the system
    *   @return returns all the devices that arent in maintenance of the centre
    """

    def get_all_devices_by_id_center(self, id_center):
        datos = self.__door_model.get_all_devices_by_center_id(id_center)
        return datos

    """
    *   @brief Call a model method to get the status of a specific device
    *   @param id_device which is the id of the device we want to know his status
    *   @pre a center has to been registered and has devices.
    *   @return returns the status of the specific device
    """

    def device_status(self, id_device):
        return self.__door_model.devices_status(id_device)

    """
    *   @brief Call a model method to set the status of a specific device to open
    *   @param id_device which is the id of the device we want to open
    *   @pre the selected device has to be not in maintenance
    *   @post the status of the device will be changed
    """

    def open_device(self, id_device):
        self.__door_model.open_device(id_device)

    """
    *   @brief Call a model method to set the status of a specific device to close
    *   @param id_device which is the id of the device we want to close
    *   @pre the selected device has to be not in maintenance
    *   @post the status of the device will be changed
    """

    def close_device(self, id_device):
        self.__door_model.close_device(id_device)

    """
    *   @brief Get all the info of a device by his id
    *   @param id_device which is the id of the device we want the info
    *   @pre an admin has logged successfully
    *   @return all the info of the selected device
    """

    def get_device_by_id(self, id_device):
        data = self.__door_model.get_device_by_id(id_device)
        return data

    """
    *   @brief Delete a device by his id
    *   @param id_device which is the id of the device we want to delete
    *   @pre an admin has logged successfully
    *   @post the selected device will be deleted 
    """

    def delete_device_by_id(self, id_device):
        self.__door_model.delete_device_by_id(id_device)

    """
    *   @brief Updates a device of a center.
    *   @param id_device which is the id of the device that will be updated
    *   @param name which is the name that will be set to the device
    *   @param state which is the state that will be set to the device
    *   @param maintenance which is the maintenance state that will be set to the device
    *   @param pin_led which is the pin of the led that will be set to the device
    *   @param pin_button which is the pin of the button that will be set to the device
    *   @param pin_servo which is the pin of the servo that will be set to the device
    *   @pre an admin has logged successfully
    *   @post a new device will be updated
    """

    def add_device(self, id_admin, name, state, maintenance, pin_led, pin_button, pin_servo):
        id_center = self.__center_model.get_center_by_id_admin(id_admin)
        self.__door_model.add_device(id_center, name, state, maintenance, pin_led, pin_button, pin_servo)

    """
    *   @brief Adds a new device to the center that we get with the id.
    *   @param id_center is the center in which the device will be added
    *   @param id_device which is the id of the device that will be added
    *   @param name which is the name that will be set to the device
    *   @param state which is the state that will be set to the device
    *   @param maintenance which is the maintenance state that will be set to the device
    *   @param pin_led which is the pin of the led that will be set to the device
    *   @param pin_button which is the pin of the button that will be set to the device
    *   @param pin_servo which is the pin of the servo that will be set to the device
    *   @pre an admin has logged successfully
    *   @post a new device will be added
    """

    def update_device_by_id(self, id_device, name, state, maintenance, pin_led, pin_button, pin_servo):
        self.__door_model.update_device_by_id(id_device, name, state, maintenance, pin_led, pin_button, pin_servo)

    """
    *   @brief Get all the devices to send them to the center
    *   @param id_center which is the id of the center we want the devices.
    *   @pre a center has logged successfully
    *   @return the necessary info for the center 
    """

    def get_devices_for_center(self, id_center):
        return self.__door_model.get_devices_for_center(id_center)

    """
    *   @brief Call a model method to get all the devices of the centre
    *   @param id_center which is the center of we want to know their devices
    *   @pre the center has to been registered in the system
    *   @return returns all the devices that arent in maintenance of the centre
    """

    def get_all_devices_by_id_center_to_web(self, id_center):
        datos = self.__door_model.get_all_doors_by_id_center_for_web(id_center)
        return datos
