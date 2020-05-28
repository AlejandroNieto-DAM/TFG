import threading
import socket
from Device import Device

class ClientThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.socket_address = "192.168.1.143"
		self.socket_port = 1234
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.socket_address, self.socket_port))
		self.devices = []

	def run(self):
		output = "PROTOCOLTFG#" + "FECHA" + "#CLIENT#MOTORS#LOGINCENTER#100#1234#END"
		self.sendBySocket(output)

		while True:
			chunk = self.socket.recv(1024)
			fromClient = str(chunk)
			print("DEl server", fromClient)
			self.proccessMsg(fromClient)


	def sendBySocket(self, output):
		print("LO que mando -->", output)
		self.socket.send(bytes(str(output) + "\r\n", 'UTF-8'))

	def sendOpenDevice(self, id_device):
		output = "PROTOCOLTFG#FECHA#CENTER#OPENEDDEVICE#" + id_device + "#END"
		self.sendBySocket(output)

	def sendCloseDevice(self, id_device):
		output = "PROTOCOLTFG#FECHA#CENTER#CLOSEDDEVICE#" + id_device + "#END"
		self.sendBySocket(output)

	def proccessMsg(self, fromServer):
		if fromServer.__contains__("TOTAL"):
			fromServer = fromServer[fromServer.index("DEVICE") +7: -5]
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
					indexD = 0
				indexD  += 1
		elif fromServer.__contains__("OPENDEVICE"):
			for device in self.devices:
				if device.id == "2":
					device.open()

		elif fromServer.__contains__("CLOSEDEVICE"):
			for device in self.devices:
				if device.id == "2":
					device.close()
if __name__ == '__main__':
	servo = ClientThread()
	servo.start()
