import threading
import socket
from Device import Device
from User import User
from datetime import datetime
from base64 import b64encode
import base64
import time





class ClientThread(threading.Thread):
    def __init__(self):
        print("Constructor")
        threading.Thread.__init__(self)
        self.address = ("192.168.1.128", 1233)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)
        self.thread_owner = ""

    def getDateTime(self):
        timestamp = 1545730073
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object

    def sendLogin(self, username, password):
        self.thread_owner = username
        message = "PROTOCOLTFG#" + str(self.getDateTime()) + "#LOGINWEB" + "#" + username + "#" + password + "#END"
        self.sendBySocket(message)

        fromServer = self.myreceive()
        print(fromServer)
        return fromServer

    def sendBySocket(self, output):
        self.sock.send(bytes(str(output) + "\r\n", 'UTF-8'))

    def getAllDevices(self):
        message = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETDEVICES#" + self.thread_owner + "#END"
        self.sendBySocket(message)
        fromServer = self.myreceive()
        fromServer = self.processDoors(fromServer)



        return fromServer

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
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#ADDDEVICE#" + self.thread_owner + "#" + name + "#" + state + "#" + maintenance + "#END"
        self.sendBySocket(output)

    def updateDevice(self, id, name, state, maintenance):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#UPDATEDEVICE#" + self.thread_owner + "#" + id + "#" + name + "#" + state + "#" + maintenance + "#END"
        self.sendBySocket(output)

    def deleteDevice(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#DELETEDEVICE#" + self.thread_owner + "#" + id + "#END"
        self.sendBySocket(output)

    def getDevice(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETDEVICE#" + self.thread_owner + "#" + str(id) + "#END"
        self.sendBySocket(output)
        fromServer = self.myreceive()
        device = self.processDevice(fromServer)
        return device

    def processDevice(self, fromServer):
        fromServer = fromServer.split("#")
        device = Device(fromServer[4], fromServer[5], fromServer[6], fromServer[7])
        return device

    #USER
    def getAllUsers(self):
        message = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETUSERS#" + self.thread_owner + "#END"
        self.sendBySocket(message)
        fromServer = self.myreceive()
        fromServer = self.processUsers(fromServer)
        return fromServer

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
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#ADDUSER#" + self.thread_owner + "#" + dni + "#" + name + "#" + surname + "#" + lastname + "#" + password + "#" + active + "#END"
        self.sendBySocket(output)

    def updateUser(self, id, name, surname, lastname, password, active):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#UPDATEUSER#" + self.thread_owner + "#" + id + "#" + name + "#" + surname + "#" + lastname + "#" + password + "#" + active + "#END"
        self.sendBySocket(output)

    def deleteUser(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#DELETEUSER#" + self.thread_owner + "#" + id + "#END"
        self.sendBySocket(output)

    def getUser(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETUSER#" + self.thread_owner + "#" + str(id) + "#END"
        self.sendBySocket(output)
        fromServer = self.myreceive()
        user = self.processUser(fromServer)
        return user

    def processUser(self, fromServer):
        fromServer = fromServer.split("#")
        user = User(fromServer[4], fromServer[5], fromServer[6], fromServer[7], fromServer[8], fromServer[9], fromServer[10])
        return user

    # USER
    def getAllAdmins(self):
        message = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETADMINS#" + self.thread_owner + "#END"
        self.sendBySocket(message)
        fromServer = self.myreceive()
        fromServer = self.processUsers(fromServer)
        return fromServer

    def addAdmin(self, dni, name, surname, lastname, password, active):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#ADDADMIN#" + self.thread_owner + "#" + dni + "#" + name + "#" + surname + "#" + lastname + "#" + password + "#" + active + "#END"
        self.sendBySocket(output)

    def getPhoto(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CLIENT#WEB#" + self.thread_owner + "#GETPHOTO#" + id + "#END";
        self.sendBySocket(output)

        image = []
        print("yey")

        rawMsg = ""

        while not rawMsg.__contains__("FINIMAGE"):
            rawMsg = self.myreceive()
            if not rawMsg.__contains__("FINIMAGE"):
                #print("MSG --> " + rawMsg)
                msg = rawMsg.split("#")
                rawBase64 = msg[4][2: -1]
                data = base64.b64decode(rawBase64)
                #print("Sin -->" + str(data))
                #print("Con--> " + str(data)[2:-1])
                image.append(data)

        f = open('Images/' + str(id) + '.jpg', 'wb')
        for row in image:
            f.write(row)

        f.close()

    def updatePhoto(self, id):

        file = open("Images/" + id + ".jpg", "rb")
        byte = file.read(512)
        time.sleep(0.08)

        while byte:
            #print("bytes --> " + str(byte))
            self.sendBySocket(
                "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#UPLOADPHOTO#" + str(b64encode(byte)) + "#END")
            byte = file.read(512)
            time.sleep(0.08)

        self.sendBySocket(
            "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#FINUPLOADPHOTO#" + id + "#END")

        file.close()

    def myreceive(self):
        msg = ""
        while not msg.__contains__("#END"):
            chunk = self.sock.recv(1024)
            if chunk == '':
                print("conexión interrumpida")
            msg = msg + str(chunk)

        return msg
