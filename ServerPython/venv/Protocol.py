from User_Controller import User_Controller

class Protocol:

    def __init__(self):
        self.user_controller = User_Controller()

    def process(self, fromClient):
        if str(fromClient).__contains__("LOGIN"):
            datos = self.user_controller.getUserByNameAndPassword("nieto", "1234")
            return datos
