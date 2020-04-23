from User_Controller import User_Controller
from Door_Controller import Door_Controller

class Protocol:

    def __init__(self, server):
        self.user_controller = User_Controller()
        self.door_controller = Door_Controller()
        self.thread_owner = ""
        self.server = server

    def process(self, from_client):
        if str(from_client).__contains__("LOGIN"):
            from_client = self.splitString(from_client)
            comprobacionLogin = self.user_controller.getUserByNameAndPassword("nieto", "1234")
            self.thread_owner = "nieto"

            if True:
                allDoors = self.door_controller.getAllDoors()
                #TODO Poner bonita la info de las puertas en el metodo
                datos = self.compoundDoorsToSend(allDoors)

            else:
                datos = "Ohtia un erro"

            return datos

        elif str(from_client).__contains__("OPENDOOR"):

            couldBeOpened = self.door_controller.doorStatus(1)

            if couldBeOpened == True:
                self.server.alertOtherClientsADoorWillBeOpened(self.thread_owner)
                self.door_controller.openDoor(1)

            else:
                #TODO Mensaje de error
                errorMessage = "No se pudo abrir la puerta"

        #TODO MISMO METODO QUE EL DE ARRIBA PERO PARA CERRAR


    def splitString(self, string_from_client):
        splitted_string = string_from_client.split("#")
        return splitted_string

    def compoundDoorsToSend(self, doors_data):
        final_string_to_send = "aiai"
        return final_string_to_send