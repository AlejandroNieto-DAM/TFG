import pymysql


class DeviceModel:

    """
    *   @brief Constructor
    """

    def __init__(self):
        self.__host = "localhost"
        self.__user = "root"
        self.__passwd = ""
        self.__db = "db1_tfg_v1"

    """
    *   @brief Get all the devices of the centre in which the student is registered
    *   @param id_student which is the student of we want to know the center to give him the devices
    *   @pre the user and the center have to been registered in the system
    *   @return returns all the devices that arent in maintenance
    """

    def get_all_devices(self, id_student):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT id_device, device_name, device_state, device_maintenance " +
                    "FROM device " +
                    "WHERE device_maintenance = 0 and device.id_device IN (SELECT device_center.id_device " +
                    "FROM device_center, student_center " +
                    "WHERE student_center.id_center = device_center.id_center and student_center.id_student = '" + id_student + "')")

        datos = []

        for row in cur.fetchall():
            datos.append(row)

        cur.close()
        conn.close()

        return datos

    """
    *   @brief Get all the devices of the centre
    *   @param id_center which is the center of we want to know their devices
    *   @pre the center has to been registered in the system
    *   @return returns all the devices that arent in maintenance of the centre
    """

    def get_all_devices_by_center_id(self, id_center):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute(
            "SELECT id_device, device_name, device_state, device_maintenance" +
            " FROM device WHERE id_device IN (SELECT id_device FROM device_center WHERE id_center = '" + str(
                id_center) + "')")

        datos = []

        for row in cur.fetchall():
            datos.append(row)

        cur.close()
        conn.close()

        return datos

    """
    *   @brief Give the status of a specific device
    *   @param id_device which is the id of the device we want to know his status
    *   @pre a center has to been registered and has devices.
    *   @return returns the status of the specific device
    """

    def devices_status(self, id_device):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT device_state FROM device WHERE id_device = '" + str(id_device) + "'")

        couldBeOpened = False

        for row in cur.fetchone():
            if row == 0:
                couldBeOpened = True

        cur.close()
        conn.close()

        return couldBeOpened

    """
    *   @brief Set the status of a specific device to open
    *   @param id_device which is the id of the device we want to open
    *   @pre the selected device has to be not in maintenance
    *   @post the status of the device will be changed
    """

    def open_device(self, id_device):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE device SET device_state = '1' WHERE id_device = '" + str(id_device) + "'")

        cur.close()
        conn.commit()
        conn.close()

    """
    *   @brief Set the status of a specific device to close
    *   @param id_device which is the id of the device we want to close
    *   @pre the selected device has to be not in maintenance
    *   @post the status of the device will be changed
    """

    def close_device(self, id_device):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE device SET device_state = '0' WHERE id_device = '" + str(id_device) + "'")

        cur.close()
        conn.commit()
        conn.close()

    """
    *   @brief Get all the info of a device by his id
    *   @param id_device which is the id of the device we want the info
    *   @pre an admin has logged successfully
    *   @return all the info of the selected device
    """
    def get_device_by_id(self, id_device):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT * FROM device WHERE id_device = '" + str(id_device) + "'")

        data = cur.fetchone()

        cur.close()
        conn.close()

        return data

    """
    *   @brief Delete a device by his id
    *   @param id_device which is the id of the device we want to delete
    *   @pre an admin has logged successfully
    *   @post the selected device will be deleted 
    """

    def delete_device_by_id(self, id_device):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("DELETE FROM device WHERE id_device = '" + str(id_device) + "'")
        cur.execute("DELETE FROM device_center WHERE id_device = '" + str(id_device) + "'")
        cur.close()
        conn.commit()
        conn.close()

    """
    *   @brief Updates a device of a center.
    *   @param id_device which is the id of the device that will be updated
    *   @param name which is the name that will be set to the device
    *   @param state which is the state that will be set to the device
    *   @param maintenance which is the maintenance state that will be set to the device
    *   @param pin_led which is the pin of the led that will be set to the device
    *   @param pin_button which is the pin of the button that will be set to the device
    *   @param pin_servo which is the pin of the servo that will be set to the device
    *   @pre an admin has logged successfully
    *   @post a new device will be updated
    """

    def update_device_by_id(self, id_device, name, state, maintenance, pin_led, pin_button, pin_servo):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("UPDATE device SET  device_name = '" + name + "'," +
                    "device_state = '" + state + "'," +
                    "device_maintenance = '" + maintenance + "'," +
                    "pin_led = '" + pin_led + "'," +
                    "pin_button = '" + pin_button + "'," +
                    "pin_servo = '" + pin_servo + "'" +
                    "WHERE id_device = '" + str(id_device) + "'")
        cur.close()
        conn.commit()
        conn.close()

    """
    *   @brief Adds a new device to the center that we get with the id.
    *   @param id_center is the center in which the device will be added
    *   @param id_device which is the id of the device that will be added
    *   @param name which is the name that will be set to the device
    *   @param state which is the state that will be set to the device
    *   @param maintenance which is the maintenance state that will be set to the device
    *   @param pin_led which is the pin of the led that will be set to the device
    *   @param pin_button which is the pin of the button that will be set to the device
    *   @param pin_servo which is the pin of the servo that will be set to the device
    *   @pre an admin has logged successfully
    *   @post a new device will be added
    """

    def add_device(self, id_center, name, state, maintenance, pin_led, pin_button, pin_servo):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute("SELECT Max(id_device) FROM Device")

        max_id = int(cur.fetchone()[0]) + 1

        cur.execute("INSERT INTO Device VALUES ('" + str(
            max_id) + "', '" + name + "', '" + state + "', '" + maintenance + "', '" + pin_led + "', '" + pin_button + "', '" + pin_servo + "')")
        cur.execute("INSERT INTO device_center VALUES ('" + str(id_center) + "', '" + str(max_id) + "')")

        cur.close()
        conn.commit()
        conn.close()

    """
    *   @brief Get all the devices to send them to the center
    *   @param id_center which is the id of the center we want the devices.
    *   @pre a center has logged successfully
    *   @return the necessary info for the center 
    """

    def get_devices_for_center(self, id_center):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()

        sql = "SELECT id_device, pin_led, pin_button, pin_servo, device_state" + " FROM device WHERE device_maintenance = 0 and id_device IN " + "(SELECT id_device FROM device_center WHERE id_center = " + str(
            int(id_center)) + ")"
        cur.execute(sql)

        datos = []

        for row in cur.fetchall():
            datos.append(row)

        cur.close()
        conn.close()

        return datos

    """
    *   @brief Get all the devices to send them to the web
    *   @param id_center which is the id of the center we want the devices.
    *   @pre an admin has logged successfully
    *   @return the necessary info for the web 
    """

    def get_all_doors_by_id_center_for_web(self, id_center):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()
        cur.execute(
            "SELECT * " +
            " FROM device WHERE id_device IN (SELECT id_device FROM device_center WHERE id_center = '" + str(
                id_center) + "')")

        datos = []

        for row in cur.fetchall():
            datos.append(row)

        cur.close()
        conn.close()

        return datos

    def interaction(self, id_student, id_device, fecha, hora):
        conn = pymysql.connect(self.__host, self.__user, self.__passwd, self.__db)
        cur = conn.cursor()

        cur.execute("INSERT INTO interaction VALUES ('" + str(id_student) + "', '" + str(id_device)
                    + "', '" + str(fecha) + "', '" + str(hora) + "')")

        cur.close()
        conn.commit()
        conn.close()
