from datetime import datetime


class ProtocolCenter:
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


    def process(self, from_client):
        output = ""



        if str(from_client).__contains__("LOGIN"):
            print("hemos entrado pero es el login", self.thread_owner)

            from_client = self.splitString(from_client)

            comprobacionLogin = True

            datos = ""

            print("UserCenter")

            self.thread_owner = "100"

            if self.center_controller.get_center_status("100") == 1:
                comprobacionLogin = True

            if comprobacionLogin:
                self.center_controller.set_active(self.thread_owner, "1")
                allDevices = self.door_controller.get_devices_for_center("100")
                datos = self.makeDoorsToSend(allDevices)

            output  = datos


        if str(from_client).find("CENTER#CLOSEDDEVICE") != -1:
            print("hemos entrado pero es el close", self.thread_owner)
            from_client = self.splitString(from_client)
            alert = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#CLOSINGDEVICE#" + from_client[4] + "#END"
            students_in_same_centre = self.user_controller.get_all_users_by_id_center(self.thread_owner)
            self.server.alertOtherClients(students_in_same_centre, alert)
            self.door_controller.close_device(from_client[4])
            print("Cerrao")

        if str(from_client).find("CENTER#OPENEDDEVICE") != -1:
            print("hemos entrado pero es el open", self.thread_owner)
            from_client = self.splitString(from_client)
            alert = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#OPENINGDEVICE#" + from_client[4] + "#END"
            students_in_same_centre = self.user_controller.get_all_users_by_id_center(self.thread_owner)
            self.server.alertOtherClients(students_in_same_centre, alert)
            self.door_controller.open_device(from_client[4])

        if str(from_client).find("LOGOUT") != -1:
            print("hemos entrado pero es el logout", self.thread_owner)
            output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#SERVERTFG#1"


        if str(from_client).find("CENTER#GETUPDATEDDB") != -1:
            print("hemos entrado", self.thread_owner)
            allDevices = self.door_controller.get_devices_for_center(self.thread_owner)
            datos = self.makeDoorsToSend(allDevices)
            output = datos



        return output

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
    *   @brief Splits the string
    *   @param string_from_client which is the string we will split
    *   @return returns the string[] generated
    """

    def splitString(self, string_from_client):
        splitted_string = string_from_client.split("#")
        return splitted_string


    """
    *   @return returns the current time in a specific format (AAAA/MM/DD HH:mm:ss)
    """
    def getDateTime(self):
        timestamp = 1545730073
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object

    """
    *   @brief Set the user of this thread disconnected when he does the logout
    *   @pre The client has to been logged successful
    *   @post the user will be disconnected
    """
    def setDisconnected(self):
        self.center_controller.set_active(self.thread_owner, "0")