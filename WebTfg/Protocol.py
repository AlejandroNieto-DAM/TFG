from datetime import datetime
from Classes.Device import Device
from Classes.User import User


class Protocol:

    def __init__(self, clientThread):
        self.clientThread = clientThread

    def getDateTime(self):
        timestamp = 1545730073
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object

    def sendLogin(self, username,  password):
        message = "PROTOCOLTFG#" + str(self.getDateTime()) + "#LOGINWEB" + "#" + username + "#" + password + "#END"
        return message


    def getAllDevices(self):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETDEVICES#" + self.clientThread.thread_owner + "#END"
        return output

    def processDoors(self, fromServer):
        print("ProcessDoors ", fromServer)
        fromServer = fromServer[fromServer.index("DEVICE") + 7: -5]
        fromServer = fromServer.split("#")

        devices = []
        index = 1
        id = ""
        name = ""
        state = ""
        maintenance = ""

        for row in fromServer:
            if index == 1:
                id = row

            if index == 2:
                name = row

            if index == 3:
                state = row


            if index == 4:
                maintenance = row

            if row == "DEVICE" or row == "END":
                aux = Device(id, name, state, maintenance)
                #print(id, name, state, maintenance)
                devices.append(aux)
                index = 0

            index += 1

        return devices

    def addDevice(self, name, state, maintenance):
        output = "PROTOCOLTFG#" + str(
            self.getDateTime()) + "#WEB#ADDDEVICE#" + self.clientThread.thread_owner + "#" + name + "#" + state + "#" + maintenance + "#END"
        return output

    def updateDevice(self, id, name, state, maintenance):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#UPDATEDEVICE#" + self.clientThread.thread_owner + "#" + id + "#" + name + "#" + state + "#" + maintenance + "#END"
        return output

    def deleteDevice(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#DELETEDEVICE#" + self.clientThread.thread_owner + "#" + id + "#END"
        return output

    def getDevice(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETDEVICE#" + self.clientThread.thread_owner + "#" + str(id) + "#END"
        return output

    def processDevice(self, fromServer):
        fromServer = fromServer.split("#")
        device = Device(fromServer[4], fromServer[5], fromServer[6], fromServer[7])
        return device

    def getAllUsers(self):
        message = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETUSERS#" + self.clientThread.thread_owner + "#END"
        return message

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

    def addUser(self, dni, name, surname, lastname, password, active):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#ADDUSER#" + self.clientThread.thread_owner + "#" + dni + "#" + name + "#" + surname + "#" + lastname + "#" + password + "#" + active + "#END"
        return output

    def updateUser(self, id, name, surname, lastname, password, active):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#UPDATEUSER#" + self.clientThread.thread_owner + "#" + id + "#" + name + "#" + surname + "#" + lastname + "#" + password + "#" + active + "#END"
        return output

    def deleteUser(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#DELETEUSER#" + self.clientThread.thread_owner + "#" + id + "#END"
        return output

    def getUser(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETUSER#" + self.clientThread.thread_owner + "#" + str(id) + "#END"
        return output

    def processUser(self, fromServer):
        fromServer = fromServer.split("#")
        user = User(fromServer[4], fromServer[5], fromServer[6], fromServer[7], fromServer[8], fromServer[9], fromServer[10])
        return user

    def getAllAdmins(self):
        message = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETADMINS#" + self.clientThread.thread_owner + "#END"
        return message

    def addAdmin(self, dni, name, surname, lastname, password, active):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#ADDADMIN#" + self.clientThread.thread_owner + "#" + dni + "#" + name + "#" + surname + "#" + lastname + "#" + password + "#" + active + "#END"
        return output

    def getPhoto(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CLIENT#WEB#" + self.clientThread.thread_owner + "#GETPHOTO#" + id + "#END";
        return output


    def sendPartPhoto(self, bytesPhoto):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#UPLOADPHOTO#" + bytesPhoto + "#END"
        return output

    def finImage(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#FINUPLOADPHOTO#" + id + "#END"
        return output

    def logout(self):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CLIENT#WEB#LOGOUT#" + self.clientThread.thread_owner + "#END"
        return output