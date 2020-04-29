import socket
import threading
from ServerPython.venv.Server.ClientThread import ClientThread


class TFGServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        self.server_address = ('192.168.1.133', 1234)
        print('starting up on %s port %s' % self.server_address)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        self.clients_threads = []
        self.clients_threads.clear()

    def run(self):
        while True:
            # Wait for a connection
            print('waiting for a connection')
            (clientsocket, address) = self.sock.accept()
            # ahora se trata el socket cliente
            # en este caso, se trata de un servir multihilado
            ct = ClientThread(clientsocket, self)
            ct.start()
            self.clients_threads.append(ct)

    def alertOtherClients(self, thread_owner, output):

        for client in self.clients_threads:
            if client.protocol.thread_owner != thread_owner and client.protocol.thread_owner != "raspberry_client" and client.working == True:
                sock = client.getOutputStream()
                sock.send(bytes(str(output) + "\r\n", 'UTF-8'))

    def signalOpenDoorToRaspberry(self, idDoor):
        # Buscar en que hebra se encuentra la raspberry y mandarle la señal de abrir
        # Ponemos raspberry como hebra individual?
        a = 0

    def deleteThisThread(self, thread_owner):
        position = -1
        contador = 0
        for client in self.clients_threads:
            if client.protocol.thread_owner == thread_owner:
                position = contador
            contador += 1

        if position != -1:
            self.clients_threads.pop(position)

server = TFGServer()
server.start()
