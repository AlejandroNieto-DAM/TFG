import threading
import socket
from Protocol import Protocol


class ClientThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.socket_address = "192.168.1.131"
        self.socket_port = 1233
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.socket_address, self.socket_port))
        self.devices = []
        self.id_center = "100"
        self.password = "1234"
        self.protocol = Protocol()

    def run(self):
        self.sendBySocket(self.protocol.sendLogin(self.id_center, self.password))

        while True:
            chunk = self.socket.recv(1024)
            fromClient = str(chunk)
            self.proccessMsg(fromClient)

    def sendBySocket(self, output):
        self.socket.send(bytes(str(output) + "\r\n", 'UTF-8'))

    def sendTryOpening(self, id_device):
        self.sendBySocket(self.protocol.sendTryOpening(id_device))

    def sendTryClosing(self, id_device):
        self.sendBySocket(self.protocol.sendTryClosing(id_device))

    def sendOpenDevice(self, id_device):
        self.sendBySocket(self.protocol.sendOpenDevice(id_device))

    def sendCloseDevice(self, id_device):
        self.sendBySocket(self.protocol.sendCloseDevice(id_device))

    def proccessMsg(self, fromServer):
        if fromServer.__contains__("TOTAL"):
            self.devices = self.protocol.processDevices(fromServer)

        elif fromServer.__contains__("OPENDEVICE"):

            splitted_string = fromServer.split("#")

            for device in self.devices:
                if device.id == splitted_string[4]:
                    device.open()

        elif fromServer.__contains__("CLOSEDEVICE"):

            splitted_string = fromServer.split("#")

            for device in self.devices:
                if device.id == splitted_string[4]:
                    device.close()

        elif fromServer.__contains__("DATABASEUPDATED"):
            self.devices.clear()
            self.sendBySocket(self.protocol.updateDb())


if __name__ == '__main__':
    servo = ClientThread()
    servo.start()
