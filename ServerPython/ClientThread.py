import socket
import sys
from threading import Thread


class ClientThread(Thread):

    def __init__(self, client_socket):
        self.socket = client_socket

    def start(self):
        amount_received = 0
        amount_expected = 1024

        chunks = []
        bytes_recd = 0
        contador = True
        while contador:
            chunk = self.socket.recv(1024)

            if chunk == b'':
                raise RuntimeError("socket connection broken")

            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
            contador = False

            print(chunks)
            final = str(chunks)

            if final.__contains__("yeyo"):
                self.socket.send(bytes("Demonio" + "\r\n", 'UTF-8'))
                print("Enviao")

            contador = True
