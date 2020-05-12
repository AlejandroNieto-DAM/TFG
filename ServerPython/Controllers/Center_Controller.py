from Models.Center_Model import Center_Model

class Center_Controller:
    def __init__(self):
        self.__center_model = Center_Model()

    def getCenterByIdStudent(self, id_student):
        id_center = self.__center_model.getCenterByIdStudent(id_student)
        return id_center

    def getCenterStatus(self, id_center):
        status = self.__center_model.getCenterStatus(id_center)
        return status

    def setActive(self, id_center, state):
        self.__center_model.setActive(id_center, state)