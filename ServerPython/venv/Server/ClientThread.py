import threading
from base64 import b64encode

from ServerPython.venv.Server.Protocol import Protocol


class ClientThread(threading.Thread):

    def __init__(self, client_socket, server):
        threading.Thread.__init__(self)
        self.server = server
        self.socket = client_socket
        self.protocol = Protocol(self.server)
        self.working = True



    def run(self):
        while self.working:
            try:

                chunk = self.socket.recv(1024)
                fromClient = str(chunk)
                print(fromClient)
                output = self.processInput(fromClient)
                self.sendBySocket(output)
                self.sendImage()


            except ConnectionAbortedError:
                print("Conexion cerrada")
                self.server.deleteThisThread(self.protocol.thread_owner)
                self.working = False

    def processInput(self, fromClient):
        if fromClient.__contains__("PROTOCOL"):
            output = self.protocol.process(fromClient)
            return output

    def sendBySocket(self, output):
        print(output)
        self.socket.send(bytes(str(output) + "\r\n", 'UTF-8'))

    def getOutputStream(self):
        return self.socket

    def sendImage(self):
        file = open("C:\\Users\\Alejandro\\Downloads\\readFileBytes\\monkeySelfie.jpg", "rb")

        byte = file.read(512)

        while byte:
            self.sendBySocket("PHOTO#"+ str(b64encode(byte)))
            print(byte)
            byte = file.read(512)

        self.sendBySocket("FINIMAGE#YEY")

        file.close()









