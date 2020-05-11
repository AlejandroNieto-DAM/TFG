from base64 import b64encode

from Controllers.User_Controller import User_Controller
from Controllers.Door_Controller import Door_Controller
from Controllers.Center_Controller import Center_Controller
from datetime import datetime



class Protocol:

    def __init__(self, server, client_thread):
        self.user_controller = User_Controller()
        self.door_controller = Door_Controller()
        self.center_controller = Center_Controller()
        self.thread_owner = ""
        self.server = server
        self.client_thread = client_thread

    def process(self, from_client):
        output = ""
        if str(from_client).__contains__("LOGIN"):
            from_client = self.splitString(from_client)
            #comprobacionLogin = self.user_controller.existUser(from_client[4], from_client[5])
            #comprobacionLogin = self.user_controller.existUser("45936238A", "1234")
            #print(comprobacionLogin)
            self.thread_owner = "45936238A"
            comprobacionLogin = True

            if comprobacionLogin:
                self.user_controller.setUserState(self.thread_owner, "1")

                allDoors = self.door_controller.getAllDoors(self.thread_owner)
                datos = self.compoundDoorsToSend(allDoors)

            else:
                datos = "PROTOCOLTFG#" + str(self.getDateTime()) + "SERVERTFG#LOGINERROR"

            output = datos


        elif str(from_client).__contains__("OPENDEVICE"):

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

            output = datos


        elif str(from_client).__contains__("CLOSEDEVICE"):

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

            output = datos

        elif str(from_client).__contains__("LOGOUT"):
            output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#1"

        return output

    def splitString(self, string_from_client):
        splitted_string = string_from_client.split("#")
        return splitted_string

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

    def setUserDisconnected(self):
        self.user_controller.setUserState(self.thread_owner, "0")

    def getDateTime(self):
        timestamp = 1545730073
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object

    def getImage(self, fromClient):

        from_client = fromClient.split("#")
        print(str(from_client[6]))
        file = open("C:\\Users\\Alejandro\\Downloads\\readFileBytes\\" + str(from_client[6]) + ".jpg", "rb")

        byte = file.read(512)

        while byte:
            self.client_thread.sendBySocket("PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#PHOTO#" + str(b64encode(byte)))
            #print(byte)
            byte = file.read(512)

        self.client_thread.sendBySocket("PROTOCOLTFG#" + str(self.getDateTime()) + "SERVERTFG#FINIMAGE#" + str(from_client[6]))

        file.close()
