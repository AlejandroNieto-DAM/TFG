from datetime import datetime
from Device import Device


class Protocol:

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

    def sendTryOpening(self, id_device):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CENTER#TRYOPENINGDEVICE#" + id_device + "#END"
        return output

    def sendTryClosing(self, id_device):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CENTER#TRYCLOSINGDEVICE#" + id_device + "#END"
        return output

    def sendOpenDevice(self, id_device):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CENTER#OPENEDDEVICE#" + id_device + "#END"
        return output

    def sendCloseDevice(self, id_device):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CENTER#CLOSEDDEVICE#" + id_device + "#END"
        return output

    def updateDb(self):
        output = "PROTOCOLTFG#" + str(self.getDateTime()) + "#CLIENT#CENTER#GETUPDATEDDB#END"
        return output

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
                aux = Device(id, pin_led, pin_button, pin_servo, state, self)
                aux.startListenToButton()
                devices.append(aux)
                indexD = 0
            indexD += 1

        return devices
