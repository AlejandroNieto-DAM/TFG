import pymysql

class User_Model:

    def __init__(self):
        self.host = "localhost"
        self.port = "3306"
        self.user = "root"
        self.passwd = ""
        self.db = "tfg"

    def getUserByLoginAndPassword(self, name):
        conn = pymysql.connect('localhost', 'root', '', 'tfg')
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE login = '" + name + "'")

        datos = []

        for row in cur.fetchone():
            datos.append(row)

        cur.close()
        conn.close()

        return datos

    def existUser(self, name, password):
        conn = pymysql.connect('localhost', 'root', '', 'tfg')
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE login = '" + name + "' and password = '" + password + "'")

        exist = False

        if cur.fetchone() != None:
            exist = True

        cur.close()
        conn.close()

        return exist
