import base64
from base64 import b64encode

from datetime import datetime
import time


class Protocol:
    """
    *   @brief Constructor
    """
    def __init__(self, server, client_thread, user_controller, device_controller, center_controller, admin_controller):
        self.user_controller = user_controller
        self.door_controller = device_controller
        self.center_controller = center_controller
        self.admin_controller = admin_controller
        self.thread_owner = ""
        self.server = server
        self.client_thread = client_thread
        self.decoded = []

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

            comprobacionLogin = True

            datos = ""

            if str(from_client).__contains__("LOGINCENTER"):
                print("UserCenter")

                self.thread_owner = "100"

                if self.center_controller.getCenterStatus("100") == 1:
                    comprobacionLogin = True

                if comprobacionLogin:
                    self.center_controller.setActive(self.thread_owner, "1")
                    allDevices = self.door_controller.getAllDoorsByIdCenter("100")
                    datos = self.makeDoorsToSend(allDevices)

            elif str(from_client).__contains__("LOGINWEB"):
                print("UserAdmin")

                if not from_client[3] == "":
                    self.thread_owner = from_client[3]
                else:
                    comprobacionLogin = False

                # if self.center_controller.getCenterStatus("100") == 1:
                #    comprobacionLogin = True

                if comprobacionLogin:
                    # TODO Poner admin conectado
                    datos = "LOGINSUCCESFULLY#END"
                else :
                    datos = "OSTIALOGINERROr#END"

            else:
                print("UserNormal")
                # comprobacionLogin = self.user_controller.existUser(from_client[4], from_client[5])
                self.thread_owner = "45936238A"
                comprobacionCenterActive = self.center_controller.getCenterStatus(
                    self.center_controller.getCenterByIdStudent(self.thread_owner))

                if comprobacionCenterActive:
                    if comprobacionLogin:
                        self.user_controller.setUserState(self.thread_owner, "1")

                if comprobacionLogin:
                    allDoors = self.door_controller.getAllDoors(self.thread_owner)
                    datos = self.makeDoorsToSend(allDoors)
                else:
                    datos = "PROTOCOLTFG#" + str(self.getDateTime()) + "SERVERTFG#LOGINERROR"

            output = datos

        elif str(from_client).__contains__("WEB#GETDEVICES"):
            if self.thread_owner != "":
                id_center = self.center_controller.getCenterByIdAdmin(self.thread_owner)
                output = self.makeDoorsToSend(self.door_controller.getAllDoorsByIdCenter(id_center))

        elif str(from_client).__contains__("WEB#GETDEVICE"):
            if self.thread_owner != "":
                from_client = self.splitString(from_client)
                output = self.makeDoorToSend(self.door_controller.getDoorById(from_client[5]))

        elif str(from_client).__contains__("WEB#DELETEDEVICE"):
            if self.thread_owner != "":
                from_client = self.splitString(from_client)
                self.door_controller.deleteDeviceById(from_client[5])

        elif str(from_client).__contains__("WEB#UPDATEDEVICE"):
            if self.thread_owner != "":
                from_client = self.splitString(from_client)
                self.door_controller.updateDeviceById(from_client[5], from_client[6], from_client[7], from_client[8])

        elif str(from_client).__contains__("WEB#ADDDEVICE"):
            if self.thread_owner != "":
                from_client = self.splitString(from_client)
                self.door_controller.addDevice(self.thread_owner, from_client[5], from_client[6], from_client[7])

        #USER
        elif str(from_client).__contains__("WEB#GETUSERS"):
            if self.thread_owner != "":
                id_center = self.center_controller.getCenterByIdAdmin(self.thread_owner)
                output = self.makeUsersToSend(self.user_controller.getAllUsersByIdCenter(id_center))

        elif str(from_client).__contains__("WEB#GETUSER"):
            if self.thread_owner != "":
                from_client = self.splitString(from_client)
                output = self.makeUserToSend(self.user_controller.getUserById(from_client[5]))

        elif str(from_client).__contains__("WEB#DELETEUSER"):
            if self.thread_owner != "":
                from_client = self.splitString(from_client)
                self.user_controller.deleteUserById(from_client[5])

        elif str(from_client).__contains__("WEB#UPDATEUSER"):
            if self.thread_owner != "":
                from_client = self.splitString(from_client)
                self.user_controller.updateUserById(from_client[5], from_client[6], from_client[7], from_client[8], from_client[9], from_client[10])

        elif str(from_client).__contains__("WEB#ADDUSER"):
            if self.thread_owner != "":
                from_client = self.splitString(from_client)
                self.user_controller.addUser(self.thread_owner, from_client[5], from_client[6], from_client[7], from_client[8], from_client[9], from_client[10])

        #ADMIN
        elif str(from_client).__contains__("WEB#ADDADMIN"):
            if self.thread_owner != "":
                from_client = self.splitString(from_client)
                self.admin_controller.addAdmin(self.thread_owner, from_client[5], from_client[6], from_client[7], from_client[8], from_client[9], from_client[10])

        elif str(from_client).__contains__("WEB#GETADMINS"):
            if self.thread_owner != "":
                id_center = self.center_controller.getCenterByIdAdmin(self.thread_owner)
                output = self.makeUsersToSend(self.admin_controller.getAllAdminsByIdCenter(id_center))

        elif str(from_client).__contains__("WEB#UPLOADPHOTO"):
            from_client = self.splitString(from_client)
            rawBase64 = from_client[4][2: -1]
            print(rawBase64)
            data = base64.b64decode(rawBase64)
            self.decoded.append(data)

        elif str(from_client).__contains__("WEB#FINUPLOADPHOTO"):
            from_client = self.splitString(from_client)
            f = open('/Users/alejandronietoalarcon/Desktop/TFG/TFG/ServerPython/deviceImages/' + from_client[4] + '.jpg', 'wb')
            for row in self.decoded:
                f.write(row)
            f.close()

        elif str(from_client).__contains__("OPENDEVICE"):
            output = self.open_device(from_client)

        elif str(from_client).__contains__("CLOSEDEVICE"):
            output = self.close_device(from_client)

        elif str(from_client).__contains__("LOGOUT"):
            output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#1"

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
        couldBeOpened = self.door_controller.doorStatus(from_client[6])
        print(from_client[6])

        if couldBeOpened:
            alert = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#OPENINGDEVICE#" + from_client[6] + "#END"
            students_in_same_centre = self.user_controller.getUsersInSameCentre(self.thread_owner)
            id_center = self.center_controller.getCenterByIdStudent(self.thread_owner)
            self.server.alertOtherClients(self.thread_owner, students_in_same_centre, alert)
            self.server.sendSignalToThisCenter(id_center, "PROTOCOLOTOCENTER")
            self.door_controller.openDoor(from_client[6])
            datos = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#OPENINGDEVICE#" + from_client[6] + "#END"

            # TODO Introducir datos cuando se ha abierto en la tabla de interaction

        else:
            datos = "No se pudo abrir la puerta"

        return datos

    """
    *   @brief Makes all the checks to know if the device in which has operated could be active or not and if its true the device will be closed
    *   @param from_client which is the message received from the client
    *   @pre an user wants to operate to one of the devices
    *   @post if all the checks to the device are well the action will take place
    *   @return returns an answer to the client if the action was good or not
    """
    def close_device(self, from_client):

        from_client = self.splitString(from_client)
        couldBeOpened = self.door_controller.doorStatus(from_client[6])
        print(from_client[6])

        if couldBeOpened == False:
            alert = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#CLOSINGDEVICE#" + from_client[6] + "#END"
            students_in_same_centre = self.user_controller.getUsersInSameCentre(self.thread_owner)
            id_center = self.center_controller.getCenterByIdStudent(self.thread_owner)
            self.server.alertOtherClients(self.thread_owner, students_in_same_centre, alert)
            self.server.sendSignalToThisCenter(id_center, "PROTOCOLOTOCENTER")
            self.door_controller.closeDoor(from_client[6])
            datos = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#CLOSINGDEVICE#" + from_client[6] + "#END"

            # TODO Introducir datos cuando se ha abierto en la tabla de interaction

        else:
            datos = "No se pudo abrir la puerta"

        return datos

    """
    *   @brief Splits the string
    *   @param string_from_client which is the string we will split
    *   @return returns the string[] generated
    """
    def splitString(self, string_from_client):
        splitted_string = string_from_client.split("#")
        return splitted_string

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
        print(final_string_to_send)
        return final_string_to_send

    """
    *   @brief Set the user of this thread disconnected when he does the logout
    *   @pre The client has to been logged successful
    *   @post the user will be disconnected
    """
    def setUserDisconnected(self):
        self.user_controller.setUserState(self.thread_owner, "0")

    """
    *   @return returns the current time in a specific format (AAAA/MM/DD HH:mm:ss)
    """
    def getDateTime(self):
        timestamp = 1545730073
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object

    """
    *   @brief Sends the specific image of the device that the user wants
    *   @param fromClient which is the msg received by the client
    *   @pre the msg have the specific word GETPHOTO
    *   @post the image will be sent to the user
    """
    def getImage(self, fromClient):

        from_client = fromClient.split("#")
        print(str(from_client[6]))
        file = open("/Users/alejandronietoalarcon/Desktop/TFG/TFG/ServerPython/deviceImages/" + str(from_client[6]) + ".jpg", "rb")
        byte = file.read(512)
        time.sleep(0.08)

        while byte:
            print("bytes --> " + str(byte))
            self.client_thread.sendBySocket(
                "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#PHOTO#" + str(b64encode(byte)) + "#END")
            byte = file.read(512)
            time.sleep(0.08)

        self.client_thread.sendBySocket(
            "PROTOCOLTFG#" + str(self.getDateTime()) + "SERVERTFG#FINIMAGE#" + str(from_client[6]) + "#END")

        file.close()

    def makeDoorToSend(self, data):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVER" + "#DEVICE"
        for row in data:
            output += "#" + str(row)

        output += "#END"

        return output


    def makeUsersToSend(self, users_data):
        final_string_to_send = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#START#"
        user_count = 0
        sub_info_user = ""
        for user in users_data:
            sub_info_user += "USER#"
            for data in user:
                sub_info_user += str(data) + "#"
            user_count += 1

        final_string_to_send += "TOTAL#" + str(user_count) + "#" + sub_info_user + "END"
        print(final_string_to_send)
        return final_string_to_send

    def makeUserToSend(self, data):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVER" + "#USER"
        for row in data:
            output += "#" + str(row)

        output += "#END"

        return output