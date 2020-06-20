from datetime import datetime
from Classes.Device import Device
from Classes.User import User


class Protocol:

    #Constructor
    def __init__(self, clientThread):
        self.clientThread = clientThread

    """
    *   @brief get the current time
    *   @return the current time
    """
    def getDateTime(self):
        timestamp = 1545730073
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object

    """
     * @brief Make the protocol to try to get logged into the application
     * @param login which is the login of the person who wants to get logged
     * @param password which is the password of the user who wants to get logged
     * @return Returns the protocol to try to get logged
    """
    def sendLogin(self, username,  password):
        message = "PROTOCOLTFG#" + str(self.getDateTime()) + "#LOGINWEB" + "#" + username + "#" + password + "#END"
        return message

    """
    *   @brief Make the protocol to try to get all the devices
    *   @pre The admin has been logged successfully
    *   @return returns the correct string protocol
    """
    def getAllDevices(self):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETDEVICES#" + self.clientThread.thread_owner + "#END"
        return output

    """
    *   @brief Procces the string with the devices received by the server
    *   @param fromServer which is the msg received by the server with all the devices
    *   @pre the admin has been logged successfully
    *   @return an array with all the devices
    """
    def processDevices(self, fromServer):
        print("ProcessDoors ", fromServer)
        fromServer = fromServer[fromServer.index("DEVICE") + 7: -5]
        fromServer = fromServer.split("#")

        devices = []
        index = 1
        id = ""
        name = ""
        state = ""
        maintenance = ""
        pin_led = ""
        pin_button = ""
        pin_servo = ""

        for row in fromServer:
            if index == 1:
                id = row

            if index == 2:
                name = row

            if index == 3:
                state = row


            if index == 4:
                maintenance = row

            if index == 5:
                pin_led = row

            if index == 6:
                pin_button = row

            if index == 7:
                pin_servo = row

            if row == "DEVICE" or row == "END":
                aux = Device(id, name, state, maintenance, pin_led, pin_button, pin_servo)
                devices.append(aux)
                index = 0

            index += 1

        return devices

    """
    *   @brief Make the correct protocol msg to add a new device
    *   @param name wich is the name for the new device
    *   @param state wich is the default state for the new device
    *   @param name wich is the state of maintenance for the new device
    *   @pre the admin has been logged successfully
    *   @return de correct msg to send to the server
    *   @post the new device will be added to the center
    """
    def addDevice(self, name, state, maintenance, pin_led, pin_button, pin_servo):
        output = "PROTOCOLTFG#" + str(
            self.getDateTime()) + "#WEB#ADDDEVICE#" + self.clientThread.thread_owner + "#" + name + "#" + state + "#" + maintenance + "#" + pin_led + "#" + pin_button + "#" + pin_servo + "#END"
        return output

    """
    *   @brief Make the correct protocol msg to update the values of a device
    *   @param id which is the id of the device we will update
    *   @param name which is the name that will be set to the device
    *   @param state which is the state that will be set to the device
    *   @param maintenance which is the maintenance state that will be set to the device
    *   @pre the admin has to been logged successfully
    *   @return the correct protocol msg
    *   @post the device will be change his values for this.
    """
    def updateDevice(self, id, name, state, maintenance, pin_led, pin_button, pin_servo):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#UPDATEDEVICE#" + self.clientThread.thread_owner + "#" + id + "#" + name + "#" + state + "#" + maintenance + "#" + pin_led + "#" + pin_button + "#" + pin_servo + "#END"
        return output

    """
    *   @brief Make the correct protocol msg to delete a device
    *   @param id which is the id of the device we want to delete
    *   @pre the admin has been logged successfully
    *   @return the correct protocol message to delete a device
    *   @post the device selected will be deleted
    """
    def deleteDevice(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#DELETEDEVICE#" + self.clientThread.thread_owner + "#" + id + "#END"
        return output

    """
    *   @brief Makes the correct protocol msg to get all the info of a device
    *   @param id which is the id of the device we want to know the info
    *   @pre the user has been logged successfully
    *   @return the correct msg to get all the info of the device
    """
    def getDevice(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETDEVICE#" + self.clientThread.thread_owner + "#" + str(id) + "#END"
        return output

    """
    *   @brief Proccess the msg received by the server with all the info of a device
    *   @param fromServer which is the string received by the server with all the info of the device
    *   @pre the admin has been logged successfully
    *   @return the object device with his info
    """
    def processDevice(self, fromServer):
        fromServer = fromServer.split("#")
        print("Mira el id --> ", fromServer[4])
        print("Mira el id --> ", fromServer[5])

        print("Mira el id --> ", fromServer[6])

        print("Mira el id --> ", fromServer[7])

        print("Mira el id --> ", fromServer[8])
        print("Mira el id --> ", fromServer[9])

        print("Mira el id --> ", fromServer[10])

        device = Device(fromServer[4], fromServer[5], fromServer[6], fromServer[7], fromServer[8], fromServer[9], fromServer[10])
        return device

    """
    *   @brief Make the protocol to try to get all the students
    *   @pre The admin has been logged successfully
    *   @return returns the correct string protocol
    """
    def getAllUsers(self):
        message = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETUSERS#" + self.clientThread.thread_owner + "#END"
        return message

    """
    *   @brief Procces the string with the users(admin|students) received by the server
    *   @param fromServer which is the msg received by the server with all the users
    *   @pre the admin has been logged successfully
    *   @return an array with all the users(students or admins)
    """
    def processUsers(self, fromServer):
        fromServer = fromServer[fromServer.index("USER") + 5: -5]
        fromServer = fromServer.split("#")

        users = []
        index = 1
        id = ""
        name = ""
        surname = ""
        lastname = ""
        password = ""
        connected = ""
        active = ""


        for row in fromServer:
            if index == 1:
                id = row

            if index == 2:
                name = row

            if index == 3:
                surname = row

            if index == 4:
                lastname = row

            if index == 5:
                password = row

            if index == 6:
                connected = row

            if index == 7:
                active = row

            if row == "USER" or row == "END":
                aux = User(id, name, surname, lastname, password, connected, active)
                print(id, name, surname, lastname, password, connected, active)
                users.append(aux)
                index = 0

            index += 1

        return users

    """
    *   @brief Make the correct protocol msg to add a new student
    *   @param name which is the name of the new student
    *   @param dni which is the dni of the new student
    *   @param surname which is the surname of the new student
    *   @param lastname which is the lastname of the student
    *   @param password which will be the password for the student
    *   @param active which will be the state of the student
    *   @pre the admin has been logged successfully
    *   @return the correct msg to send to the server
    *   @post the new student will be added to the center
    """
    def addUser(self, dni, name, surname, lastname, password, active):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#ADDUSER#" + self.clientThread.thread_owner + "#" + dni + "#" + name + "#" + surname + "#" + lastname + "#" + password + "#" + active + "#END"
        return output

    """
    *   @brief Make the correct protocol msg to update the values of a student
    *   @param id which is the dni of the student we will update
    *   @param name which is the name that will be set to the student
    *   @param surname which is the surname of the new student
    *   @param lastname which is the lastname of the student
    *   @param password which will be the password for the student
    *   @param active which will be the state of the student
    *   @pre the admin has to been logged successfully
    *   @return the correct protocol msg
    *   @post the student will be change his values for this.
    """
    def updateUser(self, id, name, surname, lastname, password, active):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#UPDATEUSER#" + self.clientThread.thread_owner + "#" + id + "#" + name + "#" + surname + "#" + lastname + "#" + password + "#" + active + "#END"
        return output

    """
    *   @brief Make the correct protocol msg to delete a student
    *   @param id which is the dni of the student we want to delete
    *   @pre the admin has been logged successfully
    *   @return the correct protocol message to delete a student
    *   @post the student selected will be deleted
    """
    def deleteUser(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#DELETEUSER#" + self.clientThread.thread_owner + "#" + id + "#END"
        return output

    """
    *   @brief Makes the correct protocol msg to get all the info of a student
    *   @param id which is the id of the student we want to know the info
    *   @pre the user has been logged successfully
    *   @return the correct msg to get all the info of the student
    """
    def getUser(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETUSER#" + self.clientThread.thread_owner + "#" + str(id) + "#END"
        return output

    """
    *   @brief Proccess the msg received by the server with all the info of a user (student|admin)
    *   @param fromServer which is the string received by the server with all the info of the user
    *   @pre the admin has been logged successfully
    *   @return the object user with his info
    """
    def processUser(self, fromServer):
        fromServer = fromServer.split("#")
        user = User(fromServer[4], fromServer[5], fromServer[6], fromServer[7], fromServer[8], fromServer[9], fromServer[10])
        return user

    """
    *   @brief Make the protocol to try to get all the admins
    *   @pre The admin has been logged successfully
    *   @return returns the correct string protocol
    """
    def getAllAdmins(self):
        message = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETADMINS#" + self.clientThread.thread_owner + "#END"
        return message

    """
    *   @brief Make the correct protocol msg to add a new admin
    *   @param name which is the name of the new admin
    *   @param dni which is the dni of the new admin
    *   @param surname which is the surname of the new admin
    *   @param lastname which is the lastname of the admin
    *   @param password which will be the password for the admin
    *   @param active which will be the state of the admin
    *   @pre the admin has been logged successfully
    *   @return the correct msg to send to the server
    *   @post the new admin will be added to the center
    """
    def addAdmin(self, dni, name, surname, lastname, password, active):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#ADDADMIN#" + self.clientThread.thread_owner + "#" + dni + "#" + name + "#" + surname + "#" + lastname + "#" + password + "#" + active + "#END"
        return output

    """
    *   @brief Make the correct protocol msg to try to get the photo of the device selected
    *   @param id which is the id of the device we want the photo
    *   @pre the admin has been logged successfully
    *   @return the correct msg to send to the server
    """
    def getPhoto(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CLIENT#WEB#" + self.clientThread.thread_owner + "#GETPHOTO#" + id + "#END";
        return output


    """
    *   @brief Make the correct protocol to send 512 bytes of a photo to the server
    *   @param bytesPhoto which is the string of 512 bytes encoded by base64 of the photo
    *   @pre the admin has been logged successfully
    *   @return the correct msg to send to the server
    """
    def sendPartPhoto(self, bytesPhoto):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#UPLOADPHOTO#" + bytesPhoto + "#END"
        return output

    """
    *   @brief Make the correct protocol to indicate to the server that the photo is finished
    *   @param id which is the id of the device we want to associate the new photo
    *   @pre the admin has been logged successfully
    *   @return the correct msg to send to the server
    *   @post the photo sent to the server will be the new of the selected device
    """
    def finImage(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#FINUPLOADPHOTO#" + id + "#END"
        return output

    """
    *   @brief Make the protocol to get logout into the application
    *   @pre The user has to been logged previously
    *   @return Returns the protocol to get logout
    """
    def logout(self):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CLIENT#WEB#LOGOUT#" + self.clientThread.thread_owner + "#END"
        return output