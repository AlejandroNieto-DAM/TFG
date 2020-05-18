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


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
client_thread = ClientThread()
client_thread.start()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        if client_thread.sendLogin(username, password).__contains__("LOGINSUCCESFULLY"):
            session['user_id'] = 1
            return redirect(url_for('profile'))

        # user = [x for x in users if x.username == username][0]
        # if user and user.password == password:
        #    session['user_id'] = user.id
        #    return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')


def redirect_to_profile():
    session['user_id'] = 1
    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

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
    if data != None:
        return render_template('index.html', devices=data)
    else:
        data = client_thread.getAllDevices()
        return render_template('index.html', devices=data)

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    device = client_thread.getDevice(id)
    return render_template('edit-contact.html', device = device)

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        name = request.form['name']
        state = request.form['state']
        maintenance = request.form['maintenance']

        client_thread.updateDevice(id, name, state, maintenance)
        flash('Contact Updated Successfully')
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    client_thread.deleteDevice(id)
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=12348, debug=True)
