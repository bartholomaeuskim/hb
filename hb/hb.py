import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and ovverride config from an environment variable
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'hb.db'),
    SECRET_KEY = 'development key',
))
app.config.from_envvar('HB_SETTINGS', silent=True)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/shipping')
def shipping():
    return render_template('shipping.html')

@app.route('/stock')
def stock():
    return render_template('stock.html')

@app.route('/eds')
def eds():
    return render_template('eds.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db = get_db()
        cur = db.execute('select count(*) from users where id="'+request.form['username']+'" and password="'+request.form['password']+'"')
        exists = cur.fetchone()
        if not exists[0]:
            error = "Invalid ID or password"
        else:
            session['logged_in'] = True
            cur = db.execute('select admin_permission from users where id="'+request.form['username']+'"')
            admin_per = cur.fetchone()
            if admin_per[0]:
                flash('You were logged as an admin')
                session['admin'] = True
            else:
                flash('You were logged in')
                session['admin'] = False
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
