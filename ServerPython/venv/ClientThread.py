from threading import Thread
from Protocol import Protocol


class ClientThread(Thread):

    def __init__(self, client_socket, server):
        self.server = server
        self.socket = client_socket
        self.protocol = Protocol(self.server)
        self.working = True

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
                self.working = False
                self.join()

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set()
        self.join(self, timeout)

    def processInput(self, fromClient):
        if fromClient.__contains__("PROTOCOL"):
            output = self.protocol.process(fromClient)
            return output

    def sendBySocket(self, output):
        self.socket.send(bytes(str(output) + "\r\n", 'UTF-8'))

    def sendAlertDoorWillBeOpened(self):
        self.sendBySocket("QUE SE ABRE UNA PUERTA")






