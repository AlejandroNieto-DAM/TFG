from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash
)
import time

from ClientThread import ClientThread


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
client_thread = ClientThread()
client_thread.start()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        potential_login = client_thread.sendLogin(username, password)

        if potential_login.__contains__("LOGINSUCCESFULLY"):
            return redirect(url_for('IndexUser'))

        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/add_device', methods=['POST'])
def add_device():
    if request.method == 'POST':
        name = request.form['name']
        state = request.form['state']
        maintenance = request.form['maintenance']
        client_thread.addDevice(name, state, maintenance)
        return redirect(url_for('Index'))

@app.route('/devices')
def Index():
    data = client_thread.getAllDevices()
    return render_template('index.html', devices=data)


@app.route('/editdevice/<id>', methods = ['POST', 'GET'])
def get_device(id):
    device = client_thread.getDevice(id)
    print(device)
    return render_template('edit-device.html', device = device)

@app.route('/updatedevice/<id>', methods=['POST'])
def update_device(id):
    if request.method == 'POST':
        name = request.form['name']
        state = request.form['state']
        maintenance = request.form['maintenance']

        client_thread.updateDevice(id, name, state, maintenance)
        flash('Contact Updated Successfully')
        return redirect(url_for('Index'))


@app.route('/deletedevice/<string:id>', methods = ['POST','GET'])
def delete_device(id):
    client_thread.deleteDevice(id)
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))


# USER

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        dni = request.form['id']
        name = request.form['name']
        surname = request.form['surname']
        lastname = request.form['lastname']
        password = request.form['password']
        active = request.form['active']
        client_thread.addUser(dni, name, surname, lastname, password, active)
        return redirect(url_for('IndexUser'))

@app.route('/users')
def IndexUser():
    data = client_thread.getAllUsers()
    return render_template('users.html', users=data)


@app.route('/edituser/<id>', methods = ['POST', 'GET'])
def get_user(id):
    user = client_thread.getUser(id)
    return render_template('edit-user.html', user = user)

@app.route('/updateuser/<id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        lastname = request.form['lastname']
        password = request.form['password']
        active = request.form['active']

        client_thread.updateUser(id, name, surname, lastname, password, active)
        flash('User Updated Successfully')
        return redirect(url_for('IndexUser'))


@app.route('/deleteuser/<string:id>', methods = ['POST','GET'])
def delete_user(id):
    client_thread.deleteUser(id)
    flash('User Removed Successfully')
    return redirect(url_for('IndexUser'))

if __name__ == '__main__':
    app.run(port=12348, debug=True)
