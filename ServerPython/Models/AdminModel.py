import pymysql
import hashlib


class AdminModel:
    def __init__(self):
        self.__host = "localhost"
        self.__user = "root"
        self.__passwd = ""
        self.__db = "db1_tfg_v1"

    """
    *   @brief Adds a new admin to the center that we get with the id.
    *   @param id_admin which is the dni of the admin that will be admin
    *   @param name which is the name of the admin
    *   @param surname which is the surname of the admin
    *   @param lastname which is the lastname of the admin
    *   @param password which is the password of the admin
    *   @param active which is the state of the admin (if can log or not)
    *   @pre an admin has logged successfully
    *   @post a new admin will be added
    """

    def add_admin(self, id_center, id_user, name, surname, lastname, password, active):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO Admin VALUES ('" + id_user + "', '" + name + "', '" + surname + "', '" + lastname + "', '" +
            self.compute_MD5_hash(password) + "', '" + str(0) + "', '" + active + "')")

        cur.execute("INSERT INTO admin_center VALUES ('" + str(id_center) + "', '" + id_user + "')")

        cur.close()
        conn.commit()
        conn.close()

    """
    *   @brief Get all the admins of a center
    *   @param id_center which is the id of the center we want to know the admins
    *   @pre an admin has been logged successfully
    *   @return an array with all the admins of the center
    """

    def get_users_by_id_center(self, id_center):
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

    """
    *   @brief Set to a specific admin the state given
    *   @param id_admin which is the id of the admin we want to change his state
    *   @param state which is the new state of the admin
    *   @pre the admin has to been registered
    *   @post the admin state will be changed
    """

    def set_connected(self, id_admin, state):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE admin SET connected = " + state + " WHERE id_admin = '" + id_admin + "'")

        cur.close()
        conn.commit()
        conn.close()

    """
    *   @brief Consult to the bd to know is the name and password given are registered
    *   @param id which is the id given to try to get logged
    *   @param password which is the password given to try to get logged
    *   @pre the socket connection has to been successful
    *   @return returns if the user is correct and exists
    """

    def could_login(self, id, password):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE connected = 0 and active = 1 and id_admin = '" + id + "' and password = '" + self.compute_MD5_hash(
                password) + "'")

        exist = False

        if cur.fetchone() is not None:
            exist = True

        cur.close()
        conn.close()

        return exist

    #Encrypts the password
    def compute_MD5_hash(self, my_string):
        m = hashlib.md5()
        m.update(my_string.encode('utf-8'))
        return m.hexdigest()
