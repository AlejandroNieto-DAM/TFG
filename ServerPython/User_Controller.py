import User_Model


class User_Controller:
    def __init__(self):
        self.user_model = User_Model()

    def getUserByNameAndPassword(self, name, password):
        datos = self.user_model.getUserByLoginAndPassword(name, password)
        return datos
