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

    """
    *   @brief Get all the users of a center
    *   @param id_center which is the id of the center we want to know the students
    *   @pre an admin has been logged successfully
    *   @return an array with all the students of the center
    """
    
    def get_all_users_by_id_center(self, id_center):
        return self.__user_model.get_users_by_id_center(id_center)

    """
    *   @brief Get all the info of a user by his id
    *   @param id_user which is the id of the user we want the info
    *   @pre an admin has logged successfully
    *   @return all the info of the selected user
    """

    def get_user_by_id(self, id_user):
        return self.__user_model.get_user_by_id(id_user)

    """
    *   @brief Delete a student by his id
    *   @param id_user which is the id of the student we want to delete
    *   @pre an admin has logged successfully
    *   @post the selected user will be deleted 
    """

    def delete_user_by_id(self, id_user):
        self.__user_model.delete_user_by_id(id_user)

    """
    *   @brief Updates a student of a center.
    *   @param id_user which is the dni of the student that will be updated
    *   @param name which is the name that will be set to the student
    *   @param surname which is the surname that will be set to the student
    *   @param lastname which is the lastname that will be set to the student
    *   @param password which is the password that will be set to the student
    *   @param active which is the state that will be set to the student (if can log or not)
    *   @pre an admin has logged successfully
    *   @post a new student will be updated
    """

    def update_user_by_id(self, id_user, name, surname, lastname, password, active):
        self.__user_model.update_user_by_id(id_user, name, surname, lastname, password, active)

    """
    *   @brief Adds a new user to the center that we get with the id.
    *   @param id_center is the center in which the user will be added
    *   @param id_admin which is the dni of the admin
    *   @param id_user which is the dni of the student that will be added
    *   @param name which is the name of the student
    *   @param surname which is the surname of the student
    *   @param lastname which is the lastname of the student
    *   @param password which is the password of the student
    *   @param active which is the state of the student (if can log or not)
    *   @pre an admin has logged successfully
    *   @post a new student will be added
    """

    def add_user(self, id_admin, id_user, name, surname, lastname, password, active):
        id_center = self.__center_model.get_center_by_id_admin(id_admin)
        self.__user_model.add_user(id_center, id_admin, id_user, name, surname, lastname, password, active)
