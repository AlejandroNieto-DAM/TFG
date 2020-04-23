import pymysql

class Door_Model:
    def __init__(self):
        self.host = "localhost"
        self.port = "3306"
        self.user = "root"
        self.passwd = ""
        self.db = "tfg"

    def getAllDoors(self):
        conn = pymysql.connect('localhost', 'root', '', 'tfg')
        cur = conn.cursor()
        cur.execute("SELECT * FROM door WHERE maintenance = 0")

        datos = []

        for row in cur.fetchall():
            datos.append(row)

        cur.close()
        conn.close()

        return datos

    def doorStatus(self, idDoor):
        conn = pymysql.connect('localhost', 'root', '', 'tfg')
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
        conn = pymysql.connect('localhost', 'root', '', 'tfg')
        cur = conn.cursor()
        cur.execute("UPDATE door SET state = 1 WHERE id = '" + str(idDoor) + "'")

        cur.close()
        conn.commit()
        conn.close()

    def closeDoor(self, idDoor):
        conn = pymysql.connect('localhost', 'root', '', 'tfg')
        cur = conn.cursor()
        cur.execute("UPDATE door SET state = 0 WHERE id = '" + str(idDoor) + "'")

        cur.close()
        conn.commit()
        conn.close()

    def doorInMaintenance(self, idDoor):
        conn = pymysql.connect('localhost', 'root', '', 'tfg')
        cur = conn.cursor()
        cur.execute("UPDATE door SET maintenance = 1 WHERE id = '" + str(idDoor) + "'")

        cur.close()
        conn.commit()
        conn.close()

    def doorNotInMaintenance(self, idDoor):
        conn = pymysql.connect('localhost', 'root', '', 'tfg')
        cur = conn.cursor()
        cur.execute("UPDATE door SET maintenance = 0 WHERE id = '" + str(idDoor) + "'")

        cur.close()
        conn.commit()
        conn.close()
