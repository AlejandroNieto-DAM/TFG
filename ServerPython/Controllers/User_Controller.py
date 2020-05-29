from Models.User_Model import User_Model
from Models.Center_Model import Center_Model


class User_Controller:
    def __init__(self):
        self.__user_model = User_Model()
        self.__center_model = Center_Model()

    """
    *   @brief Call a model method to consult to the bd to know is the name and password given are registered
    *   @param id_student which is the id given to try to get logged
    *   @param password which is the password given to try to get logged
    *   @pre the socket connection has to been successful
    *   @return returns if the user is correct and exists
    """

    def existUser(self, name, password):
        datos = self.__user_model.existUser(name, password)
        return datos

    """
    *   @brief Call a model method to set to a specific student the state given
    *   @param id_student which is the id of the student we want to change his state
    *   @param state which is the new state of the user
    *   @pre the student has to been registered
    *   @post the student state will be changed
    """

    def setUserState(self, id_student, state):
        self.__user_model.setUserState(id_student, state)

    """
    *   @brief Call a model method to consult to db for the students in the same center that are connected
    *   @param id_student which is the id of the student we want to know his centre to know the other students
    *   @pre a center and a student of this center have been registed
    *   @return returns all the students in the same centre of the student given
    """

    def getUsersInSameCentre(self, id_student):
        students_in_same_center = self.__user_model.getUsersInSameCenter(id_student)
        return students_in_same_center

    def getAllUsersByIdCenter(self, id_center):
        return self.__user_model.getUsersByIdCenter(id_center)

    def getUserById(self, id_user):
        return self.__user_model.getUserById(id_user)

    def deleteUserById(self, id_user):
        self.__user_model.deleteUserById(id_user)

    def updateUserById(self, id_user, name, surname, lastname, password, active):
        self.__user_model.updateUserById(id_user, name, surname, lastname, password, active)

    def addUser(self, id_admin, id_user, name, surname, lastname, password, active):
        id_center = self.__center_model.getCenterByIdAdmin(id_admin)
        self.__user_model.addUser(id_center, id_admin, id_user, name, surname, lastname, password, active)