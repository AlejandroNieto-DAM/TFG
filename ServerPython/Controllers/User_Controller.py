from Models.User_Model import User_Model


class User_Controller:
    def __init__(self):
        self.__user_model = User_Model()

    def getUserByNameAndPassword(self, name):
        datos = self.__user_model.getUserByLoginAndPassword(name)
        return datos

    def existUser(self, name, password):
        datos = self.__user_model.existUser(name, password)
        return datos

    def setUserState(self, id_student, state):
        self.__user_model.setUserState(id_student, state)

    def getUsersInSameCentre(self, id_student):
        students_in_same_center = self.__user_model.getUsersInSameCenter(id_student)
        return students_in_same_center