from datetime import datetime
from Device import Device


class Protocol:

    def __init__(self, mainThread):
        self.mainThread = mainThread

    def sendLogin(self, login, password):
        output = "PROTOCOLTFG#" + str(
            self.getDateTime()) + "#CLIENT#MOTORS#LOGINCENTER#" + login + "#" + password + "#END"
        return output

    """
    *   @return returns the current time in a specific format (AAAA/MM/DD HH:mm:ss)
    """

    def getDateTime(self):
        timestamp = 1545730073
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object

    """
    *   @brief Makes the correct msg protocol to advert the users that one device will be opened
    *   @param id_device which is the id of the device we will open
    *   @pre we received an action of a user or some people are touching the door
    *   @post the device will be opened
    """

    def sendTryOpening(self, id_device):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CENTER#TRYOPENINGDEVICE#" + id_device + "#END"
        return output

    """
    *   @brief Makes the correct msg protocol to advert the users that one device will be closed
    *   @param id_device which is the id of the device we will closed
    *   @pre we received an action of a user or some people are touching the door
    *   @post the device will be closed
    """

    def sendTryClosing(self, id_device):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CENTER#TRYCLOSINGDEVICE#" + id_device + "#END"
        return output

    """
    *   @brief Makes the correct msg protocol to advert the users that one device has been opened
    *   @param id_device which is the id of the device opened
    *   @pre we received an action of a user or some people are touching the door
    *   @post the device has been opened
    """

    def sendOpenDevice(self, id_device):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CENTER#OPENEDDEVICE#" + id_device + "#END"
        return output

    """
    *   @brief Makes the correct msg protocol to advert the users that one device has been closed
    *   @param id_device which is the id of the device closed
    *   @pre we received an action of a user or some people are touching the door
    *   @post the device has been closed
    """

    def sendCloseDevice(self, id_device):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CENTER#CLOSEDDEVICE#" + id_device + "#END"
        return output

    """
    *   @brief Makes the correct msg protocol to get again all the devices
    *   @pre one admin has updated a device
    *   @post the devices will be updated
    """

    def updateDb(self):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CLIENT#CENTER#GETUPDATEDDB#END"
        return output

    """
    *   @brief Process a string received by the server to get all the devices
    *   @param fromServer which is the protocol msg that has the info of all devices
    *   @return return all the devices processed
    *   @post the devices will be created
    """

    def processDevices(self, fromServer):
        devices = []
        fromServer = fromServer[fromServer.index("DEVICE") + 7: -5]
        fromServer = fromServer.split("#")

        indexD = 1
        id = ""
        pin_led = ""
        pin_button = ""
        pin_servo = ""
        state = ""

        for row in fromServer:
            if indexD == 1:
                id = row

            if indexD == 2:
                pin_led = row

            if indexD == 3:
                pin_button = row

            if indexD == 4:
                pin_servo = row

            if indexD == 5:
                state = row

            if row == "DEVICE" or row == "END":
                print("Is mainthread null? --> ", self.mainThread)
                aux = Device(id, pin_led, pin_button, pin_servo, state, self.mainThread)
                aux.startListenToButton()
                devices.append(aux)
                indexD = 0
            indexD += 1

        return devices
