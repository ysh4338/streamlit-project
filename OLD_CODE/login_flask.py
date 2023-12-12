from flask import Flask, escape, redirect, request, session, url_for
import redis
from flask_session import Session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'cloudwave'

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
app.config['SESSION_REDIS'] = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    password='qwer1234',
    decode_responses=True)
server_session = Session(app)



@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


# set the secret key.  keep this really secret:
app.secret_key = b'\xe2\x92*\x1b\x96F\xf2\xafh^\xfd\xcf\xde\xb4f\xbd\x0b\xdf\xa1@#\xd4\xb1\x9c'


if __name__ == '__main__':
    app.run()