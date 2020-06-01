from Models.UserModel import UserModel
from Models.CenterModel import CenterModel


class UserController:
    def __init__(self):
        self.__user_model = UserModel()
        self.__center_model = CenterModel()

    """
    *   @brief Call a model method to consult to the bd to know is the name and password given are registered
    *   @param id_student which is the id given to try to get logged
    *   @param password which is the password given to try to get logged
    *   @pre the socket connection has to been successful
    *   @return returns if the user is correct and exists
    """

    def exist_user(self, name, password):
        data = self.__user_model.exist_user(name, password)
        return data

    """
    *   @brief Call a model method to set to a specific student the state given
    *   @param id_student which is the id of the student we want to change his state
    *   @param state which is the new state of the user
    *   @pre the student has to been registered
    *   @post the student state will be changed
    """

    def set_user_state(self, id_student, state):
        self.__user_model.set_user_state(id_student, state)

    """
    *   @brief Call a model method to consult to db for the students in the same center that are connected
    *   @param id_student which is the id of the student we want to know his centre to know the other students
    *   @pre a center and a student of this center have been registed
    *   @return returns all the students in the same centre of the student given
    """

    def get_users_in_same_centre(self, id_student):
        students_in_same_center = self.__user_model.get_users_in_same_center(id_student)
        return students_in_same_center

    def get_all_users_by_id_center(self, id_center):
        return self.__user_model.get_users_by_id_center(id_center)

    def get_user_by_id(self, id_user):
        return self.__user_model.get_user_by_id(id_user)

    def delete_user_by_id(self, id_user):
        self.__user_model.delete_user_by_id(id_user)

    def update_user_by_id(self, id_user, name, surname, lastname, password, active):
        self.__user_model.update_user_by_id(id_user, name, surname, lastname, password, active)

    def add_user(self, id_admin, id_user, name, surname, lastname, password, active):
        id_center = self.__center_model.get_center_by_id_admin(id_admin)
        self.__user_model.add_user(id_center, id_admin, id_user, name, surname, lastname, password, active)
