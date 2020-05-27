
class Device:
    def __init__(self, id, name, state, maintenante, pin_led, pin_button, pin_servo):
        self.id = id
        self.name = name
        self.state = state
        self.maintenance = maintenante
        self.pin_led = pin_led
        self.pin_button = pin_button
        self.pin_servo = pin_servo
