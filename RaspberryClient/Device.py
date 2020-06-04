import threading
import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685


class Device:
    def __init__(self, id, pin_led, pin_button, pin_servo, state, mainThread):
        self.id = id
        self.pin_led = int(pin_led)
        self.pin_button = int(pin_button, base=10)
        self.pin_servo = int(pin_servo)
        self.state = state
        self.buttonThread = None
        self.mainThread = mainThread
        self.pwm = Adafruit_PCA9685.PCA9685()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(18, GPIO.OUT)

    #Thread that listen for the button (open, close door)
    def listenButton(self):
        while True:
            input_state = GPIO.input(27)
            if input_state == 1:
                if self.state == str("0"):
                    self.state = "1"
                    print("OPENED " + self.state)
                    self.mainThread.sendOpenDevice(self.id)
            else:
                if self.state == str("1"):
                    self.state = "0"
                    print("CLOSED")
                    self.mainThread.sendCloseDevice(self.id)

    #Starts to listen the button thread
    def startListenToButton(self):
        self.buttonThread = threading.Thread(target=self.listenButton)
        self.buttonThread.start()

    #Open the door
    def open(self):
        self.mainThread.sendTryOpening(self.id)
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        time.sleep(1)
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        time.sleep(1)
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        self.pwm.set_pwm_freq(60)
        self.pwm.set_pwm(self.pin_servo, 0, 600)
        self.mainThread.sendOpenDevice(self.id)
        time.sleep(1)

    #Close the door
    def close(self):
        self.mainThread.sendTryClosing(self.id)
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        time.sleep(1)
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        time.sleep(1)
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        self.pwm.set_pwm_freq(60)
        self.pwm.set_pwm(self.pin_servo, 0, 150)
        self.mainThread.sendCloseDevice(self.id)
        time.sleep(1)
