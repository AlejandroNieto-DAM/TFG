import threading
import socket
from Protocol import Protocol


class ClientThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.socket_address = "192.168.1.107"
        self.socket_port = 1237
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.socket_address, self.socket_port))
        self.devices = []
        self.id_center = "100"
        self.password = "1234"
        self.protocol = None

    #Body of the thread (listen to the server for messages)
    def run(self):
        self.protocol = Protocol(self)
        self.sendBySocket(self.protocol.sendLogin(self.id_center, self.password))

        while True:
            chunk = self.socket.recv(1024)
            fromClient = str(chunk)
            print("recibo -->", fromClient)
            self.proccessMsg(fromClient)

    #Sends a message by the socket to the server
    def sendBySocket(self, output):
        print("Mando -->", output)
        self.socket.send(bytes(str(output) + "\r\n", 'UTF-8'))

    """
    *   @brief Makes the correct msg protocol to advert the users that one device will be opened
    *   @param id_device which is the id of the device we will open
    *   @pre we received an action of a user or some people are touching the door
    *   @post the device will be opened
    """

    def sendTryOpening(self, id_device):
        protocolMsg = self.protocol.sendTryOpening(id_device)
        print("Try opening --> ",protocolMsg)
        self.sendBySocket(self.protocol.sendTryOpening(id_device))

    """
    *   @brief Makes the correct msg protocol to advert the users that one device will be closed
    *   @param id_device which is the id of the device we will closed
    *   @pre we received an action of a user or some people are touching the door
    *   @post the device will be closed
    """

    def sendTryClosing(self, id_device):
        self.sendBySocket(self.protocol.sendTryClosing(id_device))

    """
    *   @brief Makes the correct msg protocol to advert the users that one device has been opened
    *   @param id_device which is the id of the device opened
    *   @pre we received an action of a user or some people are touching the door
    *   @post the device has been opened
    """

    def sendOpenDevice(self, id_device):
        self.sendBySocket(self.protocol.sendOpenDevice(id_device))

    """
    *   @brief Makes the correct msg protocol to advert the users that one device has been closed
    *   @param id_device which is the id of the device closed
    *   @pre we received an action of a user or some people are touching the door
    *   @post the device has been closed
    """

    def sendCloseDevice(self, id_device):
        self.sendBySocket(self.protocol.sendCloseDevice(id_device))

    """
    *   @brief Process the msgs received by the server
    *   @param fromServer which is the msg received by the server
    *   @pre the socket connection has been successfully
    *   @return depending of the msg this will generate a response
    *   @post an action will be executed
    """

    def proccessMsg(self, fromServer):
        if fromServer.__contains__("TOTAL"):
            self.devices = self.protocol.processDevices(fromServer)
            for d in self.devices:
                print("Un device --->", d.id)
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
