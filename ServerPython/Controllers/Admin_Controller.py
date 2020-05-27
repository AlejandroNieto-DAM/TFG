from Models.Admin_Model import Admin_Model
from Models.Center_Model import Center_Model

class Admin_Controller:
    def __init__(self):
        self.__admin_model = Admin_Model()
        self.__center_model = Center_Model()

    def addAdmin(self, id_admin, id_user, name, surname, lastname, password, active):
        id_center = self.__center_model.getCenterByIdAdmin(id_admin)
        self.__admin_model.addAdmin(id_center, id_user, name, surname, lastname, password, active)

    def getAllAdminsByIdCenter(self, id_center):
        return self.__admin_model.getUsersByIdCenter(id_center)


    def setConnected(self, id_admin, state):
        self.__admin_model.setConnected(id_admin, state)

    def couldLogin(self, id, password):
        return self.__admin_model.couldLogin(id, password)