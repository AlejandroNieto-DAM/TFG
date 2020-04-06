import socket
from ClientThread import ClientThread

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.1.132', 1234)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    (clientsocket, address) = sock.accept()
    # ahora se trata el socket cliente
    # en este caso, se trata de un servir multihilado
    ct = ClientThread(clientsocket)
    ct.start()
