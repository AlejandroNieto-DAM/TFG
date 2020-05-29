import threading
import socket
from base64 import b64encode
import base64
import time
from Protocol import Protocol


class ClientThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.address = ("192.168.1.143", 1233)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)
        self.thread_owner = ""
        self.protocol = Protocol(self)


    """
    *   @brief Call a protocol method to get the correct msg to try to get logged
    *   @param username which is the username of the admin who wants to sign in
    *   @param password which is the password of the admin who wants to sign in
    *   @pre the socket connection has to been successfully
    *   @return the response and in the web know if the user is well or not
    *   @post if the admin username and password are correct the admin will be logged
    """
    def sendLogin(self, username, password):
        self.thread_owner = username
        message = self.protocol.sendLogin(username, password)
        self.sendBySocket(message)
        fromServer = self.myreceive()
        return fromServer

    """
    *   @brief Send an output by the socket to the server
    *   @param output which is the msg that the user wants to send to the server
    *   @pre the connection socket has been successfully
    *   @post the output will be sent to the server 
    """
    def sendBySocket(self, output):
        self.sock.send(bytes(str(output) + "\r\n", 'UTF-8'))

    """
    *   @brief Call a protocol method that makes the protocol msg to get all devices and listen to the server for the msg
    *   @pre the user has been logged successfully
    """
    def getAllDevices(self):
        message = self.protocol.getAllDevices()
        self.sendBySocket(message)
        fromServer = self.myreceive()
        fromServer = self.protocol.processDevices(fromServer)
        return fromServer

    """
    *   @brief Call a protocol method for add a new device and sent the msg by the socket
    *   @param name which is the name of the new device
    *   @param state which is the default state of the new device
    *   @param maintenance which is the default state of maintenance of the device
    *   @pre the user has been logged succesfully
    *   @post a new device will be added
    """
    def addDevice(self, name, state, maintenance, pin_led, pin_button, pin_servo):
        output = self.protocol.addDevice(name, state, maintenance, pin_led, pin_button, pin_servo)
        self.sendBySocket(output)

    """
    *   @brief Call a protocol method to update with new values an existing device and sent the msg by the socket
    *   @param id which is the id of the device we want to update
    *   @param name which is the name that will be set to the device
    *   @param state which is the state that will be set to the device
    *   @param maintenance which is the maintenance state that will be set to the device
    *   @pre there is an existing device with this id
    *   @pre the admin has been logged successfully
    *   @post the selected device will be change his values by this
    """
    def updateDevice(self, id, name, state, maintenance, pin_led, pin_button, pin_servo):
        output = self.protocol.updateDevice(id, name, state, maintenance, pin_led, pin_button, pin_servo)
        self.sendBySocket(output)

    """
    *   @brief Call a protocol method to delte the selected device
    *   @param id which is the id of the device we want to delete
    *   @pre the admin has been logged successfully
    *   @pre there is an existing device with this id
    *   @post the device will be deleted  
    """
    def deleteDevice(self, id):
        output = self.protocol.deleteDevice(id)
        self.sendBySocket(output)

    """
    *   @brief Call a protocol method to get all the info of one device and sent the msg by the socket and listen to the server
    *   @param id which is the id of the device we want to know the info
    *   @pre the user has been logged successfully
    *   @pre there is an existing device with this id
    *   @return an object Device with the info received 
    """
    def getDevice(self, id):
        output = self.protocol.getDevice(id)
        self.sendBySocket(output)
        fromServer = self.myreceive()
        device = self.protocol.processDevice(fromServer)
        return device

    """
    *   @brief Call a protocol method to get all the users and sent the msg by the socket and listen to the server
    *   @pre the user has been logged successfully
    """
    def getAllUsers(self):
        message = self.protocol.getAllUsers()
        self.sendBySocket(message)
        fromServer = self.myreceive()
        fromServer = self.protocol.processUsers(fromServer)
        return fromServer

    """
    *   @brief Call a protocol method to add a new user and sent the msg by the socket
    *   @param dni which is the dni of the new user
    *   @param name which is the name of the new user
    *   @param surname which is the surname of the new user
    *   @param lastname which is the lastname of the new user
    *   @param password which is the password of the new user
    *   @param active which is the default state of the new user
    *   @pre the admin has been logged successfully
    *   @post a new user will be added 
    """
    def addUser(self, dni, name, surname, lastname, password, active):
        output = self.protocol.addUser(dni, name, surname, lastname, password, active)
        self.sendBySocket(output)

    """
    *   @brief Call a protocol method to update the user and sent the msg by the socket
    *   @param dni which is the dni that will be set to the user
    *   @param name which is the name that will be set to the user
    *   @param surname which is the surname that will be set to the user
    *   @param lastname which is the lastname that will be set to the user
    *   @param password which is the password that will be set to the user
    *   @param active which is the state that will be set to the user
    """
    def updateUser(self, id, name, surname, lastname, password, active):
        output = self.protocol.updateUser(id, name, surname, lastname, password, active)
        self.sendBySocket(output)

    """
    *   @brief Call a protocol method to delete the selected device and sent the msg by the socket
    *   @pre an admin has been logged successfully
    *   @post the selected user will be deleted
    """
    def deleteUser(self, id):
        output = self.protocol.deleteUser(id)
        self.sendBySocket(output)

    """
    *   @brief Call a protocol method to get all the info of a user, sent the msg to the server and listen for the response
    *   @param id which is the id of the user we want to get all the info
    *   @pre an admin has been logged successfully
    *   @pre there is an existing user with this id
    *   @return a User object with the info received   
    """
    def getUser(self, id):
        output = self.protocol.getUser(id)
        self.sendBySocket(output)
        fromServer = self.myreceive()
        user = self.protocol.processUser(fromServer)
        return user

    """
    *   @brief Call a protocol method to get all the admins and sent the msg by the socket and listen to the server
    *   @pre an admin has been logged successfully
    """
    def getAllAdmins(self):
        message = self.protocol.getAllAdmins()
        self.sendBySocket(message)
        fromServer = self.myreceive()
        fromServer = self.protocol.processUsers(fromServer)
        return fromServer

    """
    *   @brief Call a protocol method to add a new admin and sent the msg by the socket
    *   @param dni which is the dni of the new admin
    *   @param name which is the name of the new admin
    *   @param surname which is the surname of the new admin
    *   @param lastname which is the lastname of the new admin
    *   @param password which is the password of the new admin
    *   @param active which is the default state of the new admin
    *   @pre the admin has been logged successfully
    *   @post a new admin will be added 
    """
    def addAdmin(self, dni, name, surname, lastname, password, active):
        output = self.protocol.addAdmin(dni, name, surname, lastname, password, active)
        self.sendBySocket(output)

    """
    *   @brief Call a protocol method to get the photo of the device, sent the msg by the server and listen for the server until the img is full loaded
    *   @param id which is the id of the device we want the photo
    *   @pre an admin has been logged successfully
    *   @pre the device has a photo in the server
    *   @post the photo will be created to load in the correct html
    """
    def getPhoto(self, id):
        output = self.protocol.getPhoto(id)
        self.sendBySocket(output)

        image = []

        rawMsg = ""

        while not rawMsg.__contains__("FINIMAGE"):
            rawMsg = self.myreceive()
            if not rawMsg.__contains__("FINIMAGE"):
                msg = rawMsg.split("#")
                rawBase64 = msg[4][2: -1]
                data = base64.b64decode(rawBase64)
                image.append(data)

        f = open('Images/' + str(id) + '.jpg', 'wb')
        for row in image:
            f.write(row)

        f.close()

    """
    *   @brief Sent an image to the server to update the photo of a device
    *   @param id which is the id of the device we want to update the photo
    *   @pre an admin has been logged successfully
    *   @post the photo of the device will be updated
    """
    def updatePhoto(self, id):

        file = open("Images/" + id + ".jpg", "rb")
        byte = file.read(512)
        time.sleep(0.08)

        while byte:
            self.sendBySocket(self.protocol.sendPartPhoto(str(b64encode(byte))))
            byte = file.read(512)
            time.sleep(0.08)

        self.sendBySocket(self.protocol.finImage(id))

        file.close()

    """
    *   @brief Call a protocol method to logout and sent the msg by the socket
    *   @pre an admin has been logged successfully
    *   @post the admin will logout
    """
    def logout(self):
        output = self.protocol.logout()
        self.sendBySocket(output)

    """
    *   @brief Listen to the server until the msg received has #END
    *   @pre the socket connection has been successfully 
    *   @return the msg received
    """
    def myreceive(self):
        msg = ""
        while not msg.__contains__("#END"):
            chunk = self.sock.recv(1024)
            if chunk == '':
                print("conexión interrumpida")
            msg = msg + str(chunk)

        return msg
