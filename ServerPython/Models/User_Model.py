import pymysql
import hashlib


class User_Model:

    def __init__(self):
        self.__host = "localhost"
        self.__user = "root"
        self.__passwd = "root"
        self.__db = "db_tfg_v1"

    """
    *   @brief Consult to the bd to know is the name and password given are registered
    *   @param id_student which is the id given to try to get logged
    *   @param password which is the password given to try to get logged
    *   @pre the socket connection has to been successful
    *   @return returns if the user is correct and exists
    """
    def existUser(self, id_student, password):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT * FROM student WHERE connected = 0 and id_student = '" + id_student + "' and password = '" + self.computeMD5hash(password) + "'")

        exist = False

        if cur.fetchone() is not None:
            exist = True

        cur.close()
        conn.close()

        return exist

    """
    *   @brief Set to a specific student the state given
    *   @param id_student which is the id of the student we want to change his state
    *   @param state which is the new state of the user
    *   @pre the student has to been registered
    *   @post the student state will be changed
    """
    def setUserState(self, id_student, state):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE student SET connected = " + state + " WHERE id_student = '" + id_student + "'")

        cur.close()
        conn.commit()
        conn.close()

    """
    *   @brief Consult to db for the students in the same center that are connected
    *   @param id_student which is the id of the student we want to know his centre to know the other students
    *   @pre a center and a student of this center have been registed
    *   @return returns all the students in the same centre of the student given
    """
    def getUsersInSameCenter(self, id_student):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT id_student " +
                    "FROM student " +
                    "WHERE connected = 1 and id_student IN (SELECT id_student " +
                                                            "FROM student_center " +
                                                            "WHERE id_center = (SELECT id_center " +
                                                                                "FROM student_center " +
                                                                                "WHERE student_center.id_student = '"+ id_student + "'));")

        students_in_same_center = []

        for row in cur.fetchall():
            students_in_same_center.append(row)

        cur.close()
        conn.close()

        return students_in_same_center

    def computeMD5hash(self, my_string):
        m = hashlib.md5()
        m.update(my_string.encode('utf-8'))
        return m.hexdigest()


