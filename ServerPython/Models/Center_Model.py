import pymysql

class Center_Model:
    def __init__(self):
        self.__host = "localhost"
        self.__user = "root"
        self.__passwd = "root"
        self.__db = "db_tfg_v1"

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