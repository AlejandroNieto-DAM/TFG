import threading
import socket
from Classes.Device import Device
from Classes.User import User
from datetime import datetime
from base64 import b64encode
import base64
import time
from Protocol import Protocol


class ClientThread(threading.Thread):
    def __init__(self):
        print("Constructor")
        threading.Thread.__init__(self)
        self.address = ("192.168.1.128", 1233)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)
        self.thread_owner = ""
        self.protocol = Protocol(self)



    def sendLogin(self, username, password):
        self.thread_owner = username
        message = self.protocol.sendLogin(username, password)
        self.sendBySocket(message)
        fromServer = self.myreceive()
        return fromServer

    def sendBySocket(self, output):
        self.sock.send(bytes(str(output) + "\r\n", 'UTF-8'))

    def getAllDevices(self):
        message = self.protocol.getAllDevices()
        self.sendBySocket(message)
        fromServer = self.myreceive()
        fromServer = self.protocol.processDoors(fromServer)
        return fromServer

    def addDevice(self, name, state, maintenance):
        output = self.protocol.addDevice(name, state, maintenance)
        self.sendBySocket(output)

    def updateDevice(self, id, name, state, maintenance):
        output = self.protocol.updateDevice(id, name, state, maintenance)
        self.sendBySocket(output)

    def deleteDevice(self, id):
        output = self.protocol.deleteDevice(id)
        self.sendBySocket(output)

    def getDevice(self, id):
        output = self.protocol.getDevice(id)
        self.sendBySocket(output)
        fromServer = self.myreceive()
        device = self.protocol.processDevice(fromServer)
        return device

    def getAllUsers(self):
        message = self.protocol.getAllUsers()
        self.sendBySocket(message)
        fromServer = self.myreceive()
        fromServer = self.protocol.processUsers(fromServer)
        return fromServer


    def addUser(self, dni, name, surname, lastname, password, active):
        output = self.protocol.addUser(dni, name, surname, lastname, password, active)
        self.sendBySocket(output)

    def updateUser(self, id, name, surname, lastname, password, active):
        output = self.protocol.updateUser(id, name, surname, lastname, password, active)
        self.sendBySocket(output)

    def deleteUser(self, id):
        output = self.protocol.deleteUser(id)
        self.sendBySocket(output)

    def getUser(self, id):
        output = self.protocol.getUser(id)
        self.sendBySocket(output)
        fromServer = self.myreceive()
        user = self.protocol.processUser(fromServer)
        return user

    def getAllAdmins(self):
        message = self.protocol.getAllAdmins()
        self.sendBySocket(message)
        fromServer = self.myreceive()
        fromServer = self.protocol.processUsers(fromServer)
        return fromServer

    def addAdmin(self, dni, name, surname, lastname, password, active):
        output = self.protocol.addAdmin(dni, name, surname, lastname, password, active)
        self.sendBySocket(output)

    def getPhoto(self, id):
        output = self.protocol.getPhoto(id)
        self.sendBySocket(output)

        image = []

        rawMsg = ""

        while not rawMsg.__contains__("FINIMAGE"):
            rawMsg = self.myreceive()
            if not rawMsg.__contains__("FINIMAGE"):
                msg = rawMsg.split("#")
                rawBase64 = msg[4][2: -1]
                data = base64.b64decode(rawBase64)
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
            self.sendBySocket(self.protocol.sendPartPhoto(str(b64encode(byte))))
            byte = file.read(512)
            time.sleep(0.08)

        self.sendBySocket(self.protocol.finImage(id))

        file.close()

    def logout(self):
        output = self.protocol.logout()
        self.sendBySocket(output)

    def myreceive(self):
        msg = ""
        while not msg.__contains__("#END"):
            chunk = self.sock.recv(1024)
            if chunk == '':
                print("conexión interrumpida")
            msg = msg + str(chunk)

        return msg
