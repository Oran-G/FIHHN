import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from helpers import apology, login_required, lookup, is_valid_number
from datetime import datetime
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
# import MySQLdb
import mysql.connector
# client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
global userame
username = ''

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# db = MySQLdb.connect(passwd="moonpie",db="thangs").cursor()
# db = SQL("sqlite:///keys.db")
mydb = mysql.connector.connect(
  host="31.170.167.102",
  user="u997324830_dkUVG",
  password="+W;Ca:6fR;2",
  database='u997324830_z5GnK'
)
db = mydb.cursor()

# main home page
@app.route("/")
def index():
    print(db.execute('INSERT INTO users (Email) VALUES ("test@test.co")'))
    return render_template('index.html', message=None)



# login to existing account
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    global username
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        info = {
            'email': request.form.get('email'),
            'password': request.form.get('password'),
        }
        # Ensure username was submitted
        if not info['email'] or not info['password']:
            return error('login.html', params={info}, message='Information is incomplete')

        # Query database for username
        rows = db.execute("SELECT RowID, name, tel, machine, email, hash, med1, med2 FROM users WHERE email = :username",
                          username=(request.form.get("email")).lower())
        print(rows[0].keys())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            del info['password']
            return error('login.html', params={info}, message='Passwords do not match')

        # Remember which user has logged in
        
        session["user_id"] = rows[0]["rowid"]
        session['info'] = rows[0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", params={}, message=None)

# logout of current account
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()


    # Redirect user to login form
    return redirect("/")


# register a new account
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()
    global username
    if request.method == "POST":
        info = {
        'email': request.form.get("email"),
        'password': request.form.get("password"),
        'name': request.form.get("name"),
        'tel': request.form.get("tel"),
        'passhash': generate_password_hash(request.form.get("password")),
        'machine': request.form.get('machine'),
        }


        # Ensure password was submitted
        if info['password'] != request.form.get("confirmation"):
            del info['password']
            return error('register.html', params=info, message='Passwords do not match')


        rows = db.execute("SELECT * FROM users WHERE email = :username",
                          username=request.form.get("email"))

       
        if len(rows) == 0:
            max_med = int(db.execute('SELECT RowID FROM medications WHERE RowID = (SELECT MAX(RowID) FROM medications)')[0]['rowid'])
            for i in range(2):
                db.execute(f'INSERT INTO medications (slot) VALUES ({i+1})')
            print(type(max_med))
            print(info)
            db.execute("INSERT INTO users (email, hash, name, tel, machine, med1, med2) VALUES (?, ?, ?, ?, ?, ?, ?)", info['email'], info['passhash'], info['name'], info['tel'], info['machine'], max_med+1, max_med+2)
            return redirect("/")
        else:
            del info['email']
            del info['password']
            return error('register.html', params=info, message='Username already in use')


    else:
        return render_template("register.html", params={}, message=None)


# change password
@app.route("/new_pass", methods=["GET", "POST"])
@login_required
def new_pass():
    if request.method == "POST":
        password = request.form.get('password')
        confirmation =  request.form.get('confirmation')
        if password == confirmation:
            db.execute("UPDATE 'users' SET hash = ? WHERE id = ?", generate_password_hash(password), session['user_id'])
            return redirect('/')
        else:
            return error('new_pass.html', params={}, message='password must match confirmation')
    else:
        return render_template('new_pass.html', params={}, message=None)
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)



# submit medication 1 information
@app.route("/medications", methods=["GET", "POST"])
@login_required

def medications():
    if request.method == "POST":
        print('hi')
    
        med1 = {
            'name': request.form.get('name1'),
            'dosage': request.form.get('dosage1'),
            'amount': request.form.get('pills1')
        
        }
        # if med1['often'] == 1:
        if True:
            med1.update({
                'stime': (int(request.form.get('stime1')[:2]) * 60) + int(request.form.get('stime1')[3:]),
                'etime': (int(request.form.get('etime1')[:2]) * 60) + int(request.form.get('etime1')[3:]),
            })
        # db.execute(f"UPDATE 'medications' SET name={med1['name']}, start_time={med1['stime']}, end_time={med1['etime']}, dosage={med1['dosage']}, amount={med1['amount']}, user_id={session['user_id']} WHERE RowID={session['info']['med1']}")
        print(db.execute('select * from medications'))
        print(med1)
        print(type(med1['etime']))
        
        db.execute("UPDATE medications SET  name=? WHERE RowID=?", med1['name'], session['info']['med1'])
        db.execute(f"UPDATE medications SET  start_time={med1['stime']} WHERE RowID={session['info']['med1']}")
        db.execute(f"UPDATE medications SET  end_time={med1['etime']} WHERE RowID={session['info']['med1']}")
        db.execute(f"UPDATE medications SET dosage={med1['dosage']} WHERE RowID={session['info']['med1']}")
        db.execute(f"UPDATE medications SET amount={med1['amount']} WHERE RowID={session['info']['med1']}")
        db.execute(f"UPDATE medications SET user_id={session['user_id']} WHERE RowID={session['info']['med1']}")
        return redirect('/')

        
    else:
        return render_template('medication.html', params={}, message=None)


# submit medication 2 information
@app.route('/medication2', methods=["POST"])
@login_required
def medication2():
    med2 = {
        'name': request.form.get('name2'),
        'dosage': request.form.get('dosage2'),
        'amount': request.form.get('pills2')
    
    }

    # print(request.form.get('name1'))
    # print(med2)
    # print(request.form.get('stime2'))
    # if med1['often'] == 1:
    if True:
        med2.update({
            'stime': (int(request.form.get('stime2')[:2]) * 60) + int(request.form.get('stime2')[3:]),
            'etime': (int(request.form.get('etime2')[:2]) * 60) + int(request.form.get('etime2')[3:]),
        })
    # db.execute(f"UPDATE 'medications' SET name={med1['name']}, start_time={med1['stime']}, end_time={med1['etime']}, dosage={med1['dosage']}, amount={med1['amount']}, user_id={session['user_id']} WHERE RowID={session['info']['med1']}")
    # print(db.execute('select * from medications'))
    # print(med2)
    # print(type(med2['etime']))
    
    db.execute("UPDATE medications SET  name=? WHERE RowID=?", med2['name'], session['info']['med2'])
    db.execute(f"UPDATE medications SET  start_time={med2['stime']} WHERE RowID={session['info']['med2']}")
    db.execute(f"UPDATE medications SET  end_time={med2['etime']} WHERE RowID={session['info']['med2']}")
    db.execute(f"UPDATE medications SET dosage={med2['dosage']} WHERE RowID={session['info']['med2']}")
    db.execute(f"UPDATE medications SET amount={med2['amount']} WHERE RowID={session['info']['med2']}")
    db.execute(f"UPDATE medications SET user_id={session['user_id']} WHERE RowID={session['info']['med2']}")
    return redirect('/')

import time
from math import floor
# show the status of medications for the day
@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    meds = db.execute(f"select * from medications WHERE user_id={session['user_id']}")
    print(meds)
    current_time = time.strftime("%H:%M:%S", time.localtime())
    current_minutes = (int(current_time[:2]) * 60) + int(current_time[3:5])
    print(current_minutes)
    messages = []
    for med in meds:
        
        if int(med['taken']) == 0:
            if int(med['start_time']) <= current_minutes and int(med['end_time']) >= current_minutes:   
                s = f"You will be notified in {int(med['end_time']) - current_minutes - 30} Minutes to take {med['name']}" if int(med['alerted']) != 1 else f"You were notifed to take {med['name']}"     
                s1 = f"You have {int(med['end_time']) - current_minutes} minutes left to take {med['name']}.\n{s}" 
            else:
                s1 = f"You did not take {med['name']}! Please do in the future"
        else:
            s1 = f"Great Job! You took {med['name']} at {floor(int(med['time_taken']) / 60)}:{int(med['time_taken']) % 60}"
        messages.append(s1)
        print(messages)
    return render_template('dash.html', params=messages, message=None)


# redirect to our website
@app.route("/dispense", methods=["GET", "POST"])
# @login_required
def dispense():
    return redirect('http://sites.google.com/frisch.org/fihhn/home')


def error(path, params, message=None):
    return render_template(path, params=params, message=message)
