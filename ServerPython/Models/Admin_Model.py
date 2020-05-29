import pymysql
import hashlib

class Admin_Model:
    def __init__(self):
        self.__host = "localhost"
        self.__user = "root"
        self.__passwd = ""
        self.__db = "db1_tfg_v1"

    def addAdmin(self, id_center, id_user, name, surname, lastname, password, active):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO Admin VALUES ('" + id_user + "', '" + name + "', '" + surname + "', '" + lastname + "', '" + password + "', '" + str(0) + "', '" + active + "')")
        cur.execute("INSERT INTO admin_center VALUES ('" + str(id_center) + "', '" + id_user + "')")

        cur.close()
        conn.commit()
        conn.close()

    def getUsersByIdCenter(self, id_center):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE id_admin IN (SELECT id_admin FROM admin_center WHERE id_center = '" + str(
                id_center) + "')")

        datos = []
        for row in cur.fetchall():
            datos.append(row)

        cur.close()
        conn.close()

        return datos

    def setConnected(self, id_admin, state):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE admin SET connected = " + state + " WHERE id_admin = '" + id_admin + "'")

        cur.close()
        conn.commit()
        conn.close()

    def couldLogin(self, id, password):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE connected = 0 and active = 1 and id_admin = '" + id + "' and password = '" + self.computeMD5hash(password) + "'")

        exist = False

        if cur.fetchone() is not None:
            exist = True

        cur.close()
        conn.close()

        return exist

    def computeMD5hash(self, my_string):
        m = hashlib.md5()
        m.update(my_string.encode('utf-8'))
        return m.hexdigest()
