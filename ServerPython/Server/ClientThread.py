import threading
from base64 import b64encode

from Server.Protocol import Protocol


class ClientThread(threading.Thread):

    def __init__(self, client_socket, server):
        threading.Thread.__init__(self)
        self.server = server
        self.socket = client_socket
        self.protocol = Protocol(self.server, self)
        self.working = True



    def run(self):
        while self.working:
            try:

                chunk = self.socket.recv(1024)
                fromClient = str(chunk)
                print(fromClient)
                output = self.processInput(fromClient)
                self.sendBySocket(output)

            except ConnectionAbortedError:
                print("Conexion cerrada")
                self.protocol.setUserDisconnected()
                self.server.deleteThisThread(self.protocol.thread_owner)
                self.working = False



    def processInput(self, fromClient):
        if fromClient.__contains__("GETPHOTO"):
            self.getImage(fromClient)
        elif fromClient.__contains__("LOGOUT"):
            self.protocol.setUserDisconnected()
        else:
            output = self.protocol.process(fromClient)
            return output


    def sendBySocket(self, output):
        print(output)
        self.socket.send(bytes(str(output) + "\r\n", 'UTF-8'))

    def getOutputStream(self):
        return self.socket

    def getImage(self, fromClient):
        self.protocol.getImage(fromClient)

    def getThreadOwner(self):
        return self.protocol.thread_owner









