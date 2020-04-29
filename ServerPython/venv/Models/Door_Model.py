import pymysql

class Door_Model:
    def __init__(self):
        self.__host = "localhost"
        self.__user = "root"
        self.__passwd = ""
        self.__db = "tfg"

    def getAllDoors(self):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT * FROM door WHERE maintenance = 0")

        datos = []

        for row in cur.fetchall():
            datos.append(row)

        cur.close()
        conn.close()

        return datos

    def doorStatus(self, idDoor):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT state FROM door WHERE id = '" + str(idDoor) + "'")

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
        cur.execute("UPDATE door SET state = 1 WHERE id = '" + str(idDoor) + "'")

        cur.close()
        conn.commit()
        conn.close()

    def closeDoor(self, idDoor):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE door SET state = 0 WHERE id = '" + str(idDoor) + "'")

        cur.close()
        conn.commit()
        conn.close()

    def doorInMaintenance(self, idDoor):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE door SET maintenance = 1 WHERE id = '" + str(idDoor) + "'")

        cur.close()
        conn.commit()
        conn.close()

    def doorNotInMaintenance(self, idDoor):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE door SET maintenance = 0 WHERE id = '" + str(idDoor) + "'")

        cur.close()
        conn.commit()
        conn.close()
