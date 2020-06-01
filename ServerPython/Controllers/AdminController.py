from Models.AdminModel import AdminModel
from Models.CenterModel import CenterModel


class AdminController:
    def __init__(self):
        self.__admin_model = AdminModel()
        self.__center_model = CenterModel()

    def add_admin(self, id_admin, id_user, name, surname, lastname, password, active):
        id_center = self.__center_model.get_center_by_id_admin(id_admin)
        self.__admin_model.add_admin(id_center, id_user, name, surname, lastname, password, active)

    def get_all_admins_by_id_center(self, id_center):
        return self.__admin_model.get_users_by_id_center(id_center)

    def set_connected(self, id_admin, state):
        self.__admin_model.set_connected(id_admin, state)

    def could_login(self, id, password):
        return self.__admin_model.could_login(id, password)
