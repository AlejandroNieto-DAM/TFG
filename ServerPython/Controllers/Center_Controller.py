from Models.Center_Model import Center_Model


class Center_Controller:
    def __init__(self):
        self.__center_model = Center_Model()

    """
    *   @brief Call a model method to get the center of the student
    *   @param id_student which is the id of the student of what we want to know his centre
    *   @pre the student has to be registered in the system
    *   @return the id of the center of the student will be given
    """

    def getCenterByIdStudent(self, id_student):
        id_center = self.__center_model.getCenterByIdStudent(id_student)
        return id_center

    """
    *   @brief Call a model method for the status of the id of the centre we want
    *   @param id_center which is the id of the centre we want to know his status
    *   @pre the center has to be registered in the system
    *   @return the status of the specific center
    """

    def getCenterStatus(self, id_center):
        status = self.__center_model.getCenterStatus(id_center)
        return status

    """
    *   @brief Call a model method to change the status of the centre (connected | disconnected)
    *   @param id_center which is the center of we want to change his state
    *   @param state which is the new state of the centre
    *   @pre the center has to been registered
    *   @post the state of the specific center will be changed
    """

    def setActive(self, id_center, state):
        self.__center_model.setActive(id_center, state)

    def getCenterByIdAdmin(self, id_admin):
        data = self.__center_model.getCenterByIdAdmin(id_admin)
        return data
