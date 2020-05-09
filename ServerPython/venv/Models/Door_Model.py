import pymysql

class Door_Model:
    def __init__(self):
        self.__host = "localhost"
        self.__user = "root"
        self.__passwd = "root"
        self.__db = "db_tfg_v1"

    def getAllDoors(self):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT * FROM device WHERE device.id_device IN (SELECT device_center.id_device FROM device_center, student_center WHERE student_center.id_center = device_center.id_center and student_center.id_student = '45936238A')")

        datos = []

        for row in cur.fetchall():
            datos.append(row)

        cur.close()
        conn.close()

        return datos

    def doorStatus(self, idDoor):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT device_state FROM device WHERE id_device = '" + str(idDoor) + "'")

        couldBeOpened = False

        for row in cur.fetchone():
            if row == 0:
                couldBeOpened = True

        cur.close()
        conn.close()

        return couldBeOpened

    def openDoor(self, idDoor):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE device SET device_state = 1 WHERE id_device = '" + str(idDoor) + "'")

        cur.close()
        conn.commit()
        conn.close()

    def closeDoor(self, idDoor):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE device SET device_state = 0 WHERE id_device = '" + str(idDoor) + "'")

        cur.close()
        conn.commit()
        conn.close()

    def doorInMaintenance(self, idDoor):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE device SET device_maintenance = 1 WHERE id_device = '" + str(idDoor) + "'")

        cur.close()
        conn.commit()
        conn.close()

    def doorNotInMaintenance(self, idDoor):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE device SET device_maintenance = 0 WHERE id_device = '" + str(idDoor) + "'")

        cur.close()
        conn.commit()
        conn.close()
