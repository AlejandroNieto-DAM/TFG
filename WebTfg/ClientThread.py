import threading
import socket
from Device import Device
from datetime import datetime
#from App2 import redirect_to_profile


class ClientThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.address = ("192.168.1.136", 1233)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)
        self.thread_owner = ""

    def getDateTime(self):
        timestamp = 1545730073
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object

    def sendLogin(self, username, password):
        self.thread_owner = username
        message = "PROTOCOLTFG#LOGINWEB#" + str(self.getDateTime()) + "#" + username + "#" + password + "#END"
        self.sendBySocket(message)
        chunk = self.sock.recv(1024)
        fromServer = str(chunk)
        print(fromServer)
        return fromServer

    def sendBySocket(self, output):
        self.sock.send(bytes(str(output) + "\r\n", 'UTF-8'))

    def getAllDevices(self):
        message = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETDEVICES#" + "idAdmin" + "#END"
        self.sendBySocket(message)
        chunk = self.sock.recv(1024)
        fromServer = str(chunk)
        fromServer = self.processDoors(fromServer)
        return fromServer

    def processDoors(self, fromServer):

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
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#ADDDEVICE#" + "idADmin#" + name + "#" + state + "#" + maintenance + "#END"
        self.sendBySocket(output)

    def updateDevice(self, id, name, state, maintenance):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#UPDATEDEVICE#" + "idAdmin#" + id + "#" + name + "#" + state + "#" + maintenance + "#END"
        self.sendBySocket(output)

    def deleteDevice(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#DELETEDEVICE#" + "idAdmin#" + id + "#END"
        self.sendBySocket(output)

    def getDevice(self, id):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#WEB#GETDEVICE#" + "idAdmin#" + str(id) + "#END"
        self.sendBySocket(output)
        chunk = self.sock.recv(1024)
        fromServer = str(chunk)
        device = self.processDevice(fromServer)
        return device

    def processDevice(self, fromServer):
        fromServer = fromServer.split("#")
        device = Device(fromServer[4], fromServer[5], fromServer[6], fromServer[7])
        return device


ct = ClientThread()
ct.getDevice("1")


