import pymysql
import hashlib


class UserModel:

    """
    *   @brief Constructor
    """

    def __init__(self):
        self.__host = "localhost"
        self.__user = "root"
        self.__passwd = ""
        self.__db = "db1_tfg_v1"

    """
    *   @brief Consult to the bd to know is the name and password given are registered
    *   @param id_student which is the id given to try to get logged
    *   @param password which is the password given to try to get logged
    *   @pre the socket connection has to been successful
    *   @return returns if the user is correct and exists
    """

    def exist_user(self, id_student, password):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT * FROM student WHERE connected = 0 and id_student = '" + id_student + "' and password = '" + self.compute_MD5_hash(password) + "'")

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

    def set_user_state(self, id_student, state):
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

    def get_users_in_same_center(self, id_student):
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


    #Encrypts the password
    def compute_MD5_hash(self, my_string):
        m = hashlib.md5()
        m.update(my_string.encode('utf-8'))
        return m.hexdigest()

    """
    *   @brief Get all the users of a center
    *   @param id_center which is the id of the center we want to know the students
    *   @pre an admin has been logged successfully
    *   @return an array with all the students of the center
    """
    def get_users_by_id_center(self, id_center):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM student WHERE id_student IN (SELECT id_student FROM student_center WHERE id_center = '" + str(id_center) + "')")

        datos = []
        for row in cur.fetchall():
            datos.append(row)

        cur.close()
        conn.close()

        return datos

    """
    *   @brief Get all the info of a user by his id
    *   @param id_user which is the id of the user we want the info
    *   @pre an admin has logged successfully
    *   @return all the info of the selected user
    """

    def get_user_by_id(self, id_user):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT * FROM student WHERE id_student = '" + str(id_user) + "'")

        data = cur.fetchone()

        cur.close()
        conn.close()

        return data

    """
    *   @brief Delete a student by his id
    *   @param id_user which is the id of the student we want to delete
    *   @pre an admin has logged successfully
    *   @post the selected user will be deleted 
    """

    def delete_user_by_id(self, id_user):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("DELETE FROM student_center WHERE id_student = '" + str(id_user) + "'")
        cur.execute("DELETE FROM student WHERE id_student = '" + str(id_user) + "'")
        cur.close()
        conn.commit()
        conn.close()

    """
    *   @brief Updates a student of a center.
    *   @param id_user which is the dni of the student that will be updated
    *   @param name which is the name that will be set to the student
    *   @param surname which is the surname that will be set to the student
    *   @param lastname which is the lastname that will be set to the student
    *   @param password which is the password that will be set to the student
    *   @param active which is the state that will be set to the student (if can log or not)
    *   @pre an admin has logged successfully
    *   @post a new student will be updated
    """

    def update_user_by_id(self, id_user, name, surname, lastname, password, active):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE student SET  student_name = '" + name + "'," +
                    "student_surname1 = '" + surname + "'," +
                    "student_surname2 = '" + lastname + "'," +
                    "password = '" + self.compute_MD5_hash(password) + "'," +
                    "active = '" + active + "'"
                                            "WHERE id_student = '" + str(id_user) + "'")
        cur.close()
        conn.commit()
        conn.close()

    """
    *   @brief Adds a new user to the center that we get with the id.
    *   @param id_center is the center in which the user will be added
    *   @param id_admin which is the dni of the admin
    *   @param id_user which is the dni of the student that will be added
    *   @param name which is the name of the student
    *   @param surname which is the surname of the student
    *   @param lastname which is the lastname of the student
    *   @param password which is the password of the student
    *   @param active which is the state of the student (if can log or not)
    *   @pre an admin has logged successfully
    *   @post a new student will be added
    """

    def add_user(self, id_center, id_admin, id_user, name, surname, lastname, password, active):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO Student VALUES ('" + id_user + "', '" + name + "', '" + surname + "', '" + lastname + "', '" +
            self.compute_MD5_hash(password) + "', '" + str(0) + "', '" + active + "')")
        cur.execute("INSERT INTO register VALUES ('" + id_user + "', '" + id_admin + "')")
        cur.execute("INSERT INTO student_center VALUES ('" + str(id_center) + "', '" + id_user + "')")

        cur.close()
        conn.commit()
        conn.close()


