import pymysql
import hashlib


class User_Model:

    def __init__(self):
        self.__host = "localhost"
        self.__user = "root"
        self.__passwd = "root"
        self.__db = "db_tfg_v1"

    def getUserByLoginAndPassword(self, name):
      """ conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE login = '" + name + "'")

        datos = []

        for row in cur.fetchone():
            datos.append(row)

        cur.close()
        conn.close()

        return datos"""

    def existUser(self, name, password):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT * FROM student WHERE connected = 0 and id_student = '" + name + "' and password = '" + self.computeMD5hash(password) + "'")

        exist = False

        if cur.fetchone() != None:
            exist = True

        cur.close()
        conn.close()

        return exist

    def setUserState(self, id_student, state):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE student SET connected = " + state + " WHERE id_student = '" + id_student + "'")

        cur.close()
        conn.commit()
        conn.close()

    def getUsersInSameCenter(self, id_student):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT id_student FROM student WHERE connected = 1 and id_student IN (SELECT id_student FROM student_center WHERE id_center = (SELECT id_center FROM student_center WHERE student_center.id_student = '"+ id_student + "'));")

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

