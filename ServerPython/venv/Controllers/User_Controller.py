from ServerPython.venv.Models.User_Model import User_Model


class User_Controller:
    def __init__(self):
        self.__user_model = User_Model()

    def getUserByNameAndPassword(self, name):
        datos = self.__user_model.getUserByLoginAndPassword(name)
        return datos

    def existUser(self, name, password):
        datos = self.__user_model.existUser(name, password)
        return datos
