import socket
import threading
from Server.ClientThread import ClientThread
from Controllers.User_Controller import User_Controller
from Controllers.Device_Controller import Door_Controller
from Controllers.Center_Controller import Center_Controller
from Controllers.Admin_Controller import Admin_Controller


class TFGServer(threading.Thread):

    """
    *   @brief  Constructor. Initialize the server socket on the specific port and address
    """
    def __init__(self):
        threading.Thread.__init__(self)
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        self.server_address = ('192.168.1.143', 1234)
        print('starting up on %s port %s' % self.server_address)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        self.clients_threads = []
        self.center_threads = []
        self.web_threads = []
        self.clients_threads.clear()
        self.center_threads.clear()
        self.web_threads.clear()
        self.user_controller = User_Controller()
        self.door_controller = Door_Controller()
        self.center_controller = Center_Controller()
        self.admin_controller = Admin_Controller()

    """
    *   @brief Wait for a connection to the server and when there is one accepts the connection and ads the new connection to the clients_threads
    """
    def run(self):
        while True:
            # Wait for a connection
            print('waiting for a connection')
            (clientsocket, address) = self.sock.accept()
            # ahora se trata el socket cliente
            # en este caso, se trata de un servir multihilado
            ct = ClientThread(clientsocket, self, self.user_controller, self.door_controller, self.center_controller, self.admin_controller)
            ct.start()


    """
    *   @brief Send an alert to the clients in the array of students in same centre less the thread owner to let then know there was an action to one of the devices.
    *   @param thread_owner is the owner of the thread that send the action to one of the devices
    *   @param students_in_same_centre is the users in the same centre of the user who did the action that are connected to the application
    *   @param output is the msg to send to the users
    *   @pre one user has to do an action over one device
    *   @post the users that are in students_in_same_centre will be alerted by one msg by socket
    """
    def alertOtherClients(self, students_in_same_centre, output):

        for student in students_in_same_centre:
            for client in self.clients_threads:
                print(student, " -- ", client.protocol.thread_owner)
                if student == client.protocol.thread_owner:
                    client.sendBySocket(output)

    """
        *   @brief Send the signal to the thread of the center in which one user has operate over a device.
        *   @param id_center is the id of the center in which the device has been operated
        *   @param output is the message that will be sent to the center
        *   @pre one user has to do an action over one device
        *   @post the msg will be sent and the specific device will do an action
    """
    def sendSignalToThisCenter(self, id_center, output):
        print("output que envio -> " + output)
        for center in self.center_threads:
            if center.protocol.thread_owner == id_center:
                center.sendBySocket(output)

    """
        *   @brief Delete the thread of the specific owner when is disconnected
        *   @param thread_owner is the id of the user that has been disconected
        *   @pre one user has to logout
        *   @post the thread will be deleted
    """
    def deleteThisThread(self, thread_owner):
        position = -1
        contador = 0
        for client in self.clients_threads:
            if client.getThreadOwner() == thread_owner:
                position = contador
            contador += 1

        if position != -1:
            self.clients_threads.pop(position)

        position = -1
        contador = 0
        for client in self.center_threads:
            if client.getThreadOwner() == thread_owner:
                position = contador
            contador += 1

        if position != -1:
            self.center_threads.pop(position)

        position = -1
        contador = 0
        for client in self.web_threads:
            if client.getThreadOwner() == thread_owner:
                position = contador
            contador += 1

        if position != -1:
            self.web_threads.pop(position)



    def addCenter(self, thread):
        self.center_threads.append(thread)

    def addAdmin(self, thread):
        self.web_threads.append(thread)


    def addUser(self, thread):
        self.clients_threads.append(thread)


server = TFGServer()
server.start()
