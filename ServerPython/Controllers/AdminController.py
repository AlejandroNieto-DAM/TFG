from Models.AdminModel import AdminModel
from Models.CenterModel import CenterModel


class AdminController:
    def __init__(self):
        self.__admin_model = AdminModel()
        self.__center_model = CenterModel()

    """
    *   @brief Adds a new admin to the center that we get with the id.
    *   @param id_admin which is the dni of the admin that will be admin
    *   @param name which is the name of the admin
    *   @param surname which is the surname of the admin
    *   @param lastname which is the lastname of the admin
    *   @param password which is the password of the admin
    *   @param active which is the state of the admin (if can log or not)
    *   @pre an admin has logged successfully
    *   @post a new admin will be added
    """

    def add_admin(self, id_admin, id_user, name, surname, lastname, password, active):
        id_center = self.__center_model.get_center_by_id_admin(id_admin)
        self.__admin_model.add_admin(id_center, id_user, name, surname, lastname, password, active)

    """
    *   @brief Get all the admins of a center
    *   @param id_center which is the id of the center we want to know the admins
    *   @pre an admin has been logged successfully
    *   @return an array with all the admins of the center
    """

    def get_all_admins_by_id_center(self, id_center):
        return self.__admin_model.get_users_by_id_center(id_center)

    """
    *   @brief Set to a specific admin the state given
    *   @param id_admin which is the id of the admin we want to change his state
    *   @param state which is the new state of the admin
    *   @pre the admin has to been registered
    *   @post the admin state will be changed
    """

    def set_connected(self, id_admin, state):
        self.__admin_model.set_connected(id_admin, state)

    """
    *   @brief Consult to the bd to know is the name and password given are registered
    *   @param id which is the id given to try to get logged
    *   @param password which is the password given to try to get logged
    *   @pre the socket connection has to been successful
    *   @return returns if the user is correct and exists
    """

    def could_login(self, id, password):
        return self.__admin_model.could_login(id, password)
