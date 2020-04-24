import socket
from ClientThread import ClientThread

class TFGServer:
    def __init__(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        self.server_address = ('192.168.1.133', 1234)
        print('starting up on %s port %s' % self.server_address)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        self.clientsThreads = []


    def startServer(self):
        while True:
            # Wait for a connection
            print('waiting for a connection')
            (clientsocket, address) = self.sock.accept()
            # ahora se trata el socket cliente
            # en este caso, se trata de un servir multihilado
            ct = ClientThread(clientsocket, self)
            ct.start()
            self.clientsThreads.append(ct)


    def alertOtherClientsADoorWillBeOpened(self, thread_owner):
        for client in self.clientsThreads:
            if client.thread_owner != thread_owner and client.thread_owner != "raspberry_client" and client.working == True:
                client.sendAlertDoorWillBeOpened()

    def signalOpenDoorToRaspberry(self, idDoor):
        #Buscar en que hebra se encuentra la raspberry y mandarle la señal de abrir
        #Ponemos raspberry como hebra individual?
        a = 0



server = TFGServer()
server.startServer()