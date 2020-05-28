import threading
import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685


class Device:
	def __init__(self, id, pin_led, pin_button, pin_servo, state, mainThread):
		self.id = id
		self.pin_led =  pin_led
		self.pin_button = int(pin_button, base=10)
		self.pin_servo = int(pin_servo)
		self.state = state
		self.mainThread = mainThread
		self.pwm = Adafruit_PCA9685.PCA9685()
		self.pwm.set_pwm_freq(60)

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def listenButton(self):
		while True:
			input_state = GPIO.input(self.pin_button)
			if input_state == False:
				if self.state == 0:
					self.state = 1
					print("OPENED")
					self.mainThread.sendOpenDevice(self.id)
			else:
				if self.state == 1:
					self.state = 0
					print("CLOSED")
					self.mainThread.sendCloseDevice(self.id)

	def startListenToButton(self):
		listen = threading.Thread(target=self.listenButton)
		listen.start()


	def open(self):
		self.mainThread.sendOpenDevice(self.id)
		self.pwm.set_pwm(self.pin_servo, 0, 600)
		time.sleep(1)

	def close(self):
		self.mainThread.sendCloseDevice(self.id)
		self.pwm.set_pwm(self.pin_servo, 0, 150)
		time.sleep(1)

