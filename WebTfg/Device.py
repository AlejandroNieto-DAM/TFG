
class Device:
    def __init__(self, id, name, state, maintenante):
        self.id = id
        self.name = name
        self.state = state
        self.maintenance = maintenante
        self.image = []

    def set_image(self, image):
        self.image = image