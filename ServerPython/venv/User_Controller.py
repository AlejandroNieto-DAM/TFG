from User_Model import User_Model


class User_Controller:
    def __init__(self):
        self.user_model = User_Model()

    def getUserByNameAndPassword(self, name):
        datos = self.user_model.getUserByLoginAndPassword(name)
        return datos

    def existUser(self, name, password):
        datos = self.user_model.existUser(name, password)
        return datos
