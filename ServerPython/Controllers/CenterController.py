from Models.CenterModel import CenterModel


class CenterController:
    def __init__(self):
        self.__center_model = CenterModel()

    """
    *   @brief Call a model method to get the center of the student
    *   @param id_student which is the id of the student of what we want to know his centre
    *   @pre the student has to be registered in the system
    *   @return the id of the center of the student will be given
    """

    def get_center_by_id_student(self, id_student):
        id_center = self.__center_model.get_center_by_id_student(id_student)
        return id_center

    """
    *   @brief Call a model method for the status of the id of the centre we want
    *   @param id_center which is the id of the centre we want to know his status
    *   @pre the center has to be registered in the system
    *   @return the status of the specific center
    """

    def get_center_status(self, id_center):
        status = self.__center_model.get_center_status(id_center)
        return status

    """
    *   @brief Call a model method to change the status of the centre (connected | disconnected)
    *   @param id_center which is the center of we want to change his state
    *   @param state which is the new state of the centre
    *   @pre the center has to been registered
    *   @post the state of the specific center will be changed
    """

    def set_active(self, id_center, state):
        self.__center_model.set_active(id_center, state)

    """
    *   @brief Consult to BD for the centre in which is the admin of the id given
    *   @param id_admin which is the id of the admin of what we want to know his centre
    *   @pre the admin has to be registered in the system
    *   @return the id of the center of the admin will be given
    """

    def get_center_by_id_admin(self, id_admin):
        data = self.__center_model.get_center_by_id_admin(id_admin)
        return data
