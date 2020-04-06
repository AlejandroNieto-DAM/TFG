from threading import Thread
from Protocol import Protocol


class ClientThread(Thread):

    def __init__(self, client_socket):
        self.socket = client_socket
        self.protocol = Protocol()

    def start(self):
        while True:
            try:

                chunk = self.socket.recv(1024)
                fromClient = str(chunk)
                print(fromClient)
                output = self.processInput(fromClient)
                self.socket.send(bytes(str(output) + "\r\n", 'UTF-8'))
                print("Enviao")

            except ConnectionAbortedError:
                print("Conexion cerrada")

    def processInput(self, fromClient):
        if fromClient.__contains__("PROTOCOL"):
            output = self.protocol.process(fromClient)
            return output





