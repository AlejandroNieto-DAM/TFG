import base64
from base64 import b64encode

from datetime import datetime
import time

from Server.ProtocolF import ProtocolF


class Protocol(ProtocolF):

    """
    *   @brief Constructor
    """

    def __init__(self, server, client_thread, user_controller, device_controller, center_controller, admin_controller):
        ProtocolF.__init__(self, server, client_thread, user_controller,
                           device_controller, center_controller, admin_controller)

    """
    *   @brief Process the msg received by the client
    *   @param from_client which is the msg received by the client
    *   @pre we have to receive a msg from the client
    *   @post an answer will be generated to for the client if its needed 
    """

    def process(self, from_client):
        output = ""

        if str(from_client).__contains__("LOGIN"):

            from_client = self.splitString(from_client)

            comprobacionLogin = False

            #datos = ""

            print("UserNormal")
            comprobacionLogin = self.user_controller.existUser(from_client[4], from_client[5])
            #self.thread_owner = "45936238A"
            self.thread_owner = from_client[4]
            comprobacionCenterActive = self.center_controller.get_center_status(
                self.center_controller.get_center_by_id_student(self.thread_owner))

            if comprobacionCenterActive:
                if comprobacionLogin:
                    self.user_controller.set_user_state(self.thread_owner, "1")

            if comprobacionLogin:
                allDoors = self.door_controller.get_all_devices(self.thread_owner)
                datos = self.makeDoorsToSend(allDoors)
            else:
                datos = "PROTOCOLTFG#" + str(self.getDateTime()) + "SERVERTFG#ERROR#LOGIN"

            output = datos

        elif str(from_client).__contains__("#OPENDEVICE#"):
            self.open_device(from_client)

        elif str(from_client).__contains__("CLOSEDEVICE"):
            self.close_device(from_client)

        elif str(from_client).__contains__("LOGOUT"):
            output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#1"

        else:
            print("No he entrao")

        return output

    """
    *   @brief Makes all the checks to know if the device in which has operated could be active or not and if its true the device will be opened
    *   @param from_client which is the message received from the client
    *   @pre an user wants to operate to one of the devices
    *   @post if all the checks to the device are well the action will take place
    *   @return returns an answer to the client if the action was good or not
    """

    def open_device(self, from_client):
        from_client = self.splitString(from_client)
        couldBeOpened = self.door_controller.device_status(from_client[6])

        if couldBeOpened:

            id_center = self.center_controller.get_center_by_id_student(self.thread_owner)
            signal = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVER#OPENDEVICE#" + from_client[6] + "#END"
            self.server.sendSignalToThisCenter(str(id_center), signal)

            datetime = from_client[1].split(" ")

            self.door_controller.interaction(self.thread_owner, from_client[6], datetime[0], datetime[1][:-3])

        else:
            datos = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVER#ERROR#CANTOPEN#END"
            self.client_thread.sendBySocket(datos)

    """
    *   @brief Makes all the checks to know if the device in which has operated could be active or not and if its true the device will be closed
    *   @param from_client which is the message received from the client
    *   @pre an user wants to operate to one of the devices
    *   @post if all the checks to the device are well the action will take place
    *   @return returns an answer to the client if the action was good or not
    """

    def close_device(self, from_client):

        from_client = self.splitString(from_client)
        couldBeOpened = self.door_controller.device_status(from_client[6])

        if couldBeOpened == False:
            id_center = self.center_controller.get_center_by_id_student(self.thread_owner)
            signal = "PROTOCOLTFG#FECHA#SERVER#CLOSEDEVICE#" + from_client[6] + "#END"
            self.server.sendSignalToThisCenter(str(id_center), signal)
            # datos = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#CLOSINGDEVICE#" + from_client[6] + "#END"

            datetime = from_client[1].split(" ")
            self.door_controller.interaction(self.thread_owner, from_client[6], datetime[0], datetime[1][:-3])

        else:
            datos = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVER#ERROR#CANTCLOSE#END"
            self.client_thread.sendBySocket(datos)


    """
    *   @brief Makes a string with all the devices of the centre in which the client is to send them to his app
    *   @param doors_data which is the array of device that we get in the database
    *   @pre the user has to been logged successful
    *   @post the correct message of the protocol will be generated
    *   @return returns the message that will be sent to the user
    """

    def makeDoorsToSend(self, doors_data):
        final_string_to_send = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#START#"
        door_count = 0
        sub_info_door = ""
        for door in doors_data:
            sub_info_door += "DEVICE#"
            for data in door:
                sub_info_door += str(data) + "#"
            door_count += 1

        final_string_to_send += "TOTAL#" + str(door_count) + "#" + sub_info_door + "END"
        return final_string_to_send

    """
    *   @brief Set the user of this thread disconnected when he does the logout
    *   @pre The client has to been logged successful
    *   @post the user will be disconnected
    """

    def setDisconnected(self):
        self.user_controller.set_user_state(self.thread_owner, "0")


    """
    *   @brief Sends the specific image of the device that the user wants
    *   @param fromClient which is the msg received by the client
    *   @pre the msg have the specific word GETPHOTO
    *   @post the image will be sent to the user
    """

    def getImage(self, fromClient):

        from_client = fromClient.split("#")
        file = open(
            "/Users/alejandronietoalarcon/Desktop/VOLVER/TFG/ServerPython/deviceImages/" + str(from_client[6]) + ".jpg",
            "rb")
        byte = file.read(512)
        #time.sleep(0.15)

        while byte:
            self.client_thread.sendBySocket(
                "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#PHOTO#" + str(b64encode(byte)) + "#END")
            byte = file.read(512)
            #time.sleep(0.15)

        self.client_thread.sendBySocket(
            "PROTOCOLTFG#" + str(self.getDateTime()) + "SERVERTFG#FINIMAGE#" + str(from_client[6]) + "#END")

        file.close()



