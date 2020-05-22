from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash,
)

import os
import base64

import time
from ClientThread import ClientThread

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
app.config["IMAGE_UPLOADS"] = "Images"
threads = []

"""
*   @brief return a thread by a name
*   @param owner which is the name of the owner of that thread
*   @pre there is an existing thread
*   @return the correct thread of the owner
"""
def getMyThread(owner):
    for thread in threads:
        if thread.thread_owner == owner:
            return thread


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        client_thread = ClientThread()
        client_thread.start()
        threads.append(client_thread)

        session['username'] = username

        potential_login = client_thread.sendLogin(username, password)

        if potential_login.__contains__("LOGINSUCCESFULLY"):
            return redirect(url_for('IndexAdmin'))
        else :
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    getMyThread(session['username']).logout()
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add_device', methods=['POST'])
def add_device():
    if request.method == 'POST':
        name = request.form['name']
        state = request.form['state']
        maintenance = request.form['maintenance']
        getMyThread(session['username']).addDevice(name, state, maintenance)
        return redirect(url_for('Index'))

@app.route('/devices')
def Index():
    data = getMyThread(session['username']).getAllDevices()
    return render_template('index.html', devices=data)


@app.route('/editdevice/<id>', methods = ['POST', 'GET'])
def get_device(id):
    device = getMyThread(session['username']).getDevice(id)
    getMyThread(session['username']).getPhoto(id)

    with open("Images/2.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    final = str(encoded_string)
    final.encode("utf-8")

    return render_template('edit-device.html', device = device, image = final)

@app.route('/updatedevice/<id>', methods=['POST'])
def update_device(id):
    if request.method == 'POST':
        if request.files:
            uploadIma = request.files["uploadImage"]
            uploadIma.save(os.path.join(app.config["IMAGE_UPLOADS"], str(id) + ".jpg"))
            getMyThread(session['username']).updatePhoto(id)


        name = request.form['name']
        state = request.form['state']
        maintenance = request.form['maintenance']

        getMyThread(session['username']).updateDevice(id, name, state, maintenance)
        flash('Contact Updated Successfully')
        return redirect(url_for('Index'))


@app.route('/deletedevice/<string:id>', methods = ['POST','GET'])
def delete_device(id):
    getMyThread(session['username']).deleteDevice(id)
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        dni = request.form['id']
        name = request.form['name']
        surname = request.form['surname']
        lastname = request.form['lastname']
        password = request.form['password']
        active = request.form['active']
        getMyThread(session['username']).addUser(dni, name, surname, lastname, password, active)
        return redirect(url_for('IndexUser'))

@app.route('/users')
def IndexUser():
    data = getMyThread(session['username']).getAllUsers()
    return render_template('users.html', users=data)

@app.route('/edituser/<id>', methods = ['POST', 'GET'])
def get_user(id):
    user = getMyThread(session['username']).getUser(id)
    return render_template('edit-user.html', user = user)

@app.route('/updateuser/<id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        lastname = request.form['lastname']
        password = request.form['password']
        active = request.form['active']

        getMyThread(session['username']).updateUser(id, name, surname, lastname, password, active)
        flash('User Updated Successfully')
        return redirect(url_for('IndexUser'))

@app.route('/deleteuser/<string:id>', methods = ['POST','GET'])
def delete_user(id):
    getMyThread(session['username']).deleteUser(id)
    flash('User Removed Successfully')
    return redirect(url_for('IndexUser'))

@app.route('/add_admin', methods=['POST'])
def add_admin():
    if request.method == 'POST':
        dni = request.form['id']
        name = request.form['name']
        surname = request.form['surname']
        lastname = request.form['lastname']
        password = request.form['password']
        active = request.form['active']
        getMyThread(session['username']).addAdmin(dni, name, surname, lastname, password, active)
        return redirect(url_for('IndexAdmin'))

@app.route('/admins')
def IndexAdmin():
    data = getMyThread(session['username']).getAllAdmins()
    return render_template('admins.html', users=data)

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
