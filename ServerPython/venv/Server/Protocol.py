from ServerPython.venv.Controllers.User_Controller import User_Controller
from ServerPython.venv.Controllers.Door_Controller import Door_Controller

class Protocol:

    def __init__(self, server):
        self.user_controller = User_Controller()
        self.door_controller = Door_Controller()
        self.thread_owner = ""
        self.server = server

    def process(self, from_client):
        output = ""
        if str(from_client).__contains__("LOGIN"):
            from_client = self.splitString(from_client)
            comprobacionLogin = self.user_controller.existUser(from_client[4], from_client[5])
            #comprobacionLogin = self.user_controller.existUser("nieto", "1234")
            self.thread_owner = from_client[4]
            #print(comprobacionLogin)


            if comprobacionLogin == True:
                allDoors = self.door_controller.getAllDoors()
                #TODO Poner bonita la info de las puertas en el metodo
                datos = self.compoundDoorsToSend(allDoors)

            else:
                datos = "PROTOCOLTFG#LOGINERROR"

            output = datos


        elif str(from_client).__contains__("OPENDOOR"):
            #print(from_client)
            from_client = self.splitString(from_client)
            #print(from_client[4])
            couldBeOpened = self.door_controller.doorStatus(from_client[4])
            #print(couldBeOpened)
            if couldBeOpened == True:
                alert = "PROTOCOLTFG#OPENINGDOOR#" + from_client[4] +  "#END"
                self.server.alertOtherClients(self.thread_owner, alert)
                self.door_controller.openDoor(from_client[4])
                datos = "PROTOCOLTFG#OPENINGDOOR#" + from_client[4] +  "#END"

            else:
                datos = "No se pudo abrir la puerta"

            output = datos


        elif str(from_client).__contains__("CLOSEDOOR"):
            #print(from_client)
            from_client = self.splitString(from_client)
            #print(from_client[4])
            couldBeOpened = self.door_controller.doorStatus(from_client[4])
            #print(couldBeOpened)
            if couldBeOpened == False:
                alert = "PROTOCOLTFG#CLOSINGDOOR#" + from_client[4] + "#END"
                self.server.alertOtherClients(self.thread_owner, alert)
                self.door_controller.closeDoor(from_client[4])
                datos = "PROTOCOLTFG#CLOSINGDOOR#" + from_client[4] + "#END"

            else:
                datos = "No se pudo cerrar la puerta"

            output = datos

        elif str(from_client).__contains__("LOGOUT"):
            output = "1"


        return output

    def splitString(self, string_from_client):
        splitted_string = string_from_client.split("#")
        return splitted_string

    def compoundDoorsToSend(self, doors_data):
        final_string_to_send = "PROTOCOLTFG#START#"
        door_count = 0;
        sub_info_door = ""
        for door in doors_data:
            sub_info_door += "DOOR#"
            for data in door:
                sub_info_door += str(data) + "#"
            door_count += 1

        final_string_to_send += "TOTAL#" + str(door_count) + "#" + sub_info_door + "END"
        print(final_string_to_send)
        return final_string_to_send



