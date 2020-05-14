import pymysql


class Center_Model:
    def __init__(self):
        self.__host = "localhost"
        self.__user = "root"
        self.__passwd = "root"
        self.__db = "db_tfg_v1"

    """
    *   @brief Consult to BD for the centre in which is the student of the id given
    *   @param id_student which is the id of the student of what we want to know his centre
    *   @pre the student has to be registered in the system
    *   @return the id of the center of the student will be given
    """

    def getCenterByIdStudent(self, id_student):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT id_center FROM student_center WHERE id_student = '" + id_student + "'")

        id_center = ""

        for row in cur.fetchone():
            id_center = row

        cur.close()
        conn.close()

        return id_center

    """
    *   @brief Consult to BD for the status of the id of the centre we want
    *   @param id_center which is the id of the centre we want to know his status
    *   @pre the center has to be registered in the system
    *   @return the status of the specific center
    """

    def getCenterStatus(self, id_center):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT active FROM center WHERE id_center = '" + str(id_center) + "'")

        active = ""

        for row in cur.fetchone():
            active = True

        cur.close()
        conn.close()

        return active

    """
    *   @brief update the DB to change the status of the centre (connected | disconnected)
    *   @param id_center which is the center of we want to change his state
    *   @param state which is the new state of the centre
    *   @pre the center has to been registered
    *   @post the state of the specific center will be changed
    """

    def setActive(self, id_center, state):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE center SET active = " + state + " WHERE id_center = '" + id_center + "'")

        cur.close()
        conn.commit()
        conn.close()
