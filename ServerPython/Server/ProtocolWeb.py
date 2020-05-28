import base64
from datetime import datetime
import time
from base64 import b64encode


class ProtocolWeb:

    def __init__(self, server, client_thread, user_controller, device_controller, center_controller, admin_controller):
        self.user_controller = user_controller
        self.door_controller = device_controller
        self.center_controller = center_controller
        self.admin_controller = admin_controller
        self.thread_owner = ""
        self.server = server
        self.client_thread = client_thread
        self.decoded = []

    def process(self, from_client):

        output = ""

        if str(from_client).__contains__("LOGIN"):
            print("UserAdmin")
            from_client = self.splitString(from_client)

            comprobacionLogin = None

            if not from_client[3] == "":
                self.thread_owner = from_client[3]
                if self.admin_controller.couldLogin(from_client[3], from_client[4]):
                    comprobacionLogin = True
                    self.admin_controller.setConnected(self.thread_owner, "1")
            else:
                comprobacionLogin = False



            if comprobacionLogin:
                # TODO Poner admin conectado
                datos = "LOGINSUCCESFULLY#END"
            else:
                datos = "OSTIALOGINERROr#END"

            output = datos

        elif str(from_client).__contains__("LOGOUT"):
            output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#1"

        elif str(from_client).__contains__("WEB#GETDEVICES"):
            if self.thread_owner != "":
                id_center = self.center_controller.getCenterByIdAdmin(self.thread_owner)
                output = self.makeDoorsToSend(self.door_controller.getAllDoorsByIdCenterToWeb(id_center))

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
                self.door_controller.updateDeviceById(from_client[5], from_client[6], from_client[7], from_client[8], from_client[9], from_client[10], from_client[11])

        elif str(from_client).__contains__("WEB#ADDDEVICE"):
            if self.thread_owner != "":
                from_client = self.splitString(from_client)
                self.door_controller.addDevice(self.thread_owner, from_client[5], from_client[6], from_client[7], from_client[8], from_client[9], from_client[10])

        # USER
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
                self.user_controller.updateUserById(from_client[5], from_client[6], from_client[7], from_client[8],
                                                    from_client[9], from_client[10])

        elif str(from_client).__contains__("WEB#ADDUSER"):
            if self.thread_owner != "":
                from_client = self.splitString(from_client)
                self.user_controller.addUser(self.thread_owner, from_client[5], from_client[6], from_client[7],
                                             from_client[8], from_client[9], from_client[10])

        # ADMIN
        elif str(from_client).__contains__("WEB#ADDADMIN"):
            if self.thread_owner != "":
                from_client = self.splitString(from_client)
                self.admin_controller.addAdmin(self.thread_owner, from_client[5], from_client[6], from_client[7],
                                               from_client[8], from_client[9], from_client[10])

        elif str(from_client).__contains__("WEB#GETADMINS"):
            if self.thread_owner != "":
                id_center = self.center_controller.getCenterByIdAdmin(self.thread_owner)
                output = self.makeUsersToSend(self.admin_controller.getAllAdminsByIdCenter(id_center))

        elif str(from_client).__contains__("WEB#UPLOADPHOTO"):
            from_client = self.splitString(from_client)
            rawBase64 = from_client[4][2: -1]
            data = base64.b64decode(rawBase64)
            self.decoded.append(data)

        elif str(from_client).__contains__("WEB#FINUPLOADPHOTO"):
            from_client = self.splitString(from_client)
            f = open(
                '/Users/alejandronietoalarcon/Desktop/TFG/TFG/ServerPython/deviceImages/' + from_client[4] + '.jpg',
                'wb')
            for row in self.decoded:
                f.write(row)
            f.close()

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
        return final_string_to_send

    def makeUserToSend(self, data):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVER" + "#USER"
        for row in data:
            output += "#" + str(row)

        output += "#END"

        return output

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
        return final_string_to_send

    """
    *   @return returns the current time in a specific format (AAAA/MM/DD HH:mm:ss)
    """

    def getDateTime(self):
        timestamp = 1545730073
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object

    def makeDoorToSend(self, data):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVER" + "#DEVICE"
        for row in data:
            output += "#" + str(row)

        output += "#END"

        return output

    """
        *   @brief Sends the specific image of the device that the user wants
        *   @param fromClient which is the msg received by the client
        *   @pre the msg have the specific word GETPHOTO
        *   @post the image will be sent to the user
        """

    def getImage(self, fromClient):

        from_client = fromClient.split("#")

        try:
            file = open(
                "/Users/alejandronietoalarcon/Desktop/TFG/TFG/ServerPython/deviceImages/" + str(from_client[6]) + ".jpg", "rb")
        except FileNotFoundError as e:
            file = open(
                "/Users/alejandronietoalarcon/Desktop/TFG/TFG/ServerPython/deviceImages/1.jpg", "rb")

        byte = file.read(512)
        time.sleep(0.08)

        while byte:
            self.client_thread.sendBySocket(
                "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#PHOTO#" + str(b64encode(byte)) + "#END")
            byte = file.read(512)
            time.sleep(0.08)

        self.client_thread.sendBySocket(
            "PROTOCOLTFG#" + str(self.getDateTime()) + "SERVERTFG#FINIMAGE#" + str(from_client[6]) + "#END")

        file.close()

    """
    *   @brief Set the user of this thread disconnected when he does the logout
    *   @pre The client has to been logged successful
    *   @post the user will be disconnected
    """
    def setDisconnected(self):
        self.admin_controller.setConnected(self.thread_owner, "0")
