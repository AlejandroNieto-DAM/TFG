from base64 import b64encode

from Controllers.User_Controller import User_Controller
from Controllers.Device_Controller import Door_Controller
from Controllers.Center_Controller import Center_Controller
from datetime import datetime


class Protocol:
    """
    *   @brief Constructor
    """
    def __init__(self, server, client_thread):
        self.user_controller = User_Controller()
        self.door_controller = Door_Controller()
        self.center_controller = Center_Controller()
        self.thread_owner = ""
        self.server = server
        self.client_thread = client_thread

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
                    datos = self.compoundDoorsToSend(allDevices)

            else:
                print("UserNormal")
                # comprobacionLogin = self.user_controller.existUser(from_client[4], from_client[5])
                comprobacionCenterActive = self.center_controller.getCenterStatus(
                self.center_controller.getCenterByIdStudent(self.thread_owner))

                if comprobacionCenterActive:
                    self.thread_owner = "45936238A"
                    if comprobacionLogin:
                        self.user_controller.setUserState(self.thread_owner, "1")

                if comprobacionLogin:
                    allDoors = self.door_controller.getAllDoors(self.thread_owner)
                    datos = self.compoundDoorsToSend(allDoors)
                else:
                    datos = "PROTOCOLTFG#" + str(self.getDateTime()) + "SERVERTFG#LOGINERROR"

            output = datos


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
    *   @brief Compounds the device of the centre in which the client is to send them to his app
    *   @param doors_data which is the array of device that we get in the database
    *   @pre the user has to been logged successful
    *   @post the correct message of the protocol will be generated
    *   @return returns the message that will be sent to the user
    """
    def compoundDoorsToSend(self, doors_data):
        final_string_to_send = "PROTOCOLTFG#" + str(self.getDateTime()) + "SERVERTFG#START#"
        door_count = 0;
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
        file = open("C:\\Users\\Alejandro\\Downloads\\readFileBytes\\" + str(from_client[6]) + ".jpg", "rb")

        byte = file.read(512)

        while byte:
            self.client_thread.sendBySocket("PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#PHOTO#" + str(b64encode(byte)))
            byte = file.read(512)

        self.client_thread.sendBySocket(
            "PROTOCOLTFG#" + str(self.getDateTime()) + "SERVERTFG#FINIMAGE#" + str(from_client[6]))

        file.close()
