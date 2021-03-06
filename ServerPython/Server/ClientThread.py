import threading
from base64 import b64encode

from Server.Protocol import Protocol
from Server.ProtocolCenter import ProtocolCenter
from Server.ProtocolWeb import ProtocolWeb


class ClientThread(threading.Thread):
    """
    *   @brief Constructor. Is the thread of the socket client that generates the socket server.
    """

    def __init__(self, client_socket, server, user_controller, device_controller, center_controller, admin_controller):
        threading.Thread.__init__(self)
        self.server = server
        self.socket = client_socket

        self.user_controller = user_controller
        self.device_controller = device_controller
        self.center_controller = center_controller
        self.admin_controller = admin_controller

        self.user = ""

        self.protocol = None
        self.working = True

    """
    *   @brief Is the body of the thread. Infinite loop to stay always listening to the client. Read from the socket and generates an output to send a msg to the client.
    """

    def run(self):
        while self.working:
            try:

                chunk = self.socket.recv(1024)
                fromClient = str(chunk)
                print(fromClient)
                output = self.processInput(fromClient)
                self.sendBySocket(output)

            except Exception as err:
                print("Conexion cerrada")
                print(err)
                self.protocol.setDisconnected()
                self.server.deleteThisThread(self.getThreadOwner())
                self.working = False

    """
    *   @brief Process the msg received by the client.
    *   @param fromClient which is the msg received by the client
    *   @pre one client has to send a msg to the server
    *   @post depending what is write in the msg we will call one method
    *   @return Returns a msg if the msg that send the user needs a response
    """

    def processInput(self, fromClient):
        if fromClient.__contains__("GETPHOTO"):
            self.getImage(fromClient)
        elif fromClient.__contains__("LOGOUT"):
            self.protocol.setDisconnected()
        else:
            if fromClient.__contains__("LOGIN"):
                if fromClient.__contains__("LOGINWEB"):
                    self.protocol = ProtocolWeb(self.server, self, self.user_controller, self.device_controller,
                                                self.center_controller, self.admin_controller)
                    self.server.addAdmin(self)
                    self.user = "WEB"
                elif fromClient.__contains__("LOGINCENTER"):
                    self.protocol = ProtocolCenter(self.server, self, self.user_controller, self.device_controller,
                                                   self.center_controller, self.admin_controller)
                    self.server.addCenter(self)
                    self.user = "CENTER"

                elif fromClient.__contains__("LOGIN"):
                    self.protocol = Protocol(self.server, self, self.user_controller, self.device_controller,
                                             self.center_controller, self.admin_controller)
                    self.server.addUser(self)
                    self.user = "STUDENT"

                output = self.protocol.process(fromClient)

            else:

                output = self.protocol.process(fromClient)

            return output

    """
    *   @brief Send a msg to the client by the socket
    *   @param output which is the msg that will be sent
    """

    def sendBySocket(self, output):
        print(output)
        try:
            self.socket.send(bytes(str(output) + "\r\n", 'UTF-8'))
        except BrokenPipeError:
            print("broken pipe")

    """
    *   @return Returns the socket of the client
    """

    def getOutputStream(self):
        return self.socket

    """
    *   @brief Call for the method in the protocol to get the image of the device that the user wants.
    """

    def getImage(self, fromClient):
        self.protocol.getImage(fromClient)

    """
    *   @return Returns the id of the user of this thread
    """

    def getThreadOwner(self):
        return self.protocol.thread_owner
