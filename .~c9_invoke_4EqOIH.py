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
# Your Account SID from twilio.com/console
account_sid = "ACb5d9be6303b400c0254a44656e990440"
# Your Auth Token from twilio.com/console
auth_token  = "f730e6d53fc966ab9e1bb8ef710eb9af"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

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
db = SQL("sqlite:///lifegaurding.db")



@app.route("/")
def index():
    return render_template('index.html')




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    global username
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = :username",
                          username=(request.form.get("email")).lower())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        if rows[0]["gaurd"] == "TRUE":
            session["gaurd"] = 1
        elif rows[0]["gaurd"] == "FALSE":
            session["gaurd"] = 0

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()


    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()
    global username
    if request.method == "POST":
        if request.form.get("email") == '':
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif request.form.get("password") == '':
            return apology("must provide password", 403)

        # Ensure password confirmation was submitted
        elif request.form.get("confirmation") == '':
            return apology("must provide password confirmation", 403)

        elif request.form.get("machine") == '':
            return apology("must provide machine code", 403)
        elif request.form.get("number") == '':
            return apology("must provide phone number", 403)


        # Ensure password was submitted
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)


        rows = db.execute(f"SELECT * FROM users WHERE email = {username}",
                          username=request.form.get("email"))


        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        tel = request.form.get("tel")
        address1 = request.form.get("address1")
        city = request.form.get("city")
        state = request.form.get("state")
        zipcode = request.form.get("zip")
        passhash = generate_password_hash(password)
        if len(rows) == 0:
            db.execute("INSERT INTO users (name, email, hash, phone) VALUES (?, ?, ?, ?)", name, email, passhash, tel)
            rows = db.execute(f"SELECT * FROM users WHERE email = {username}",
                          username=(request.form.get("email")))
            session["user_id"] = rows[0]["id"]
            session['guard'] = 0
            address = address1 + ", " + city + ", " + state
            faddress = address.replace(" ", "+")
            address2 = address1 + ", " + city + ", " + state + " " + zipcode + "USA"
            db.execute("INSERT INTO addresses (user_id, address) VALUES (?, ?)", session["user_id"], address2)

            return redirect("/")

        else:
            return apology("Username already in use", 403)


    else:
        return render_template("register.html")









@app.route("/new_pass", methods=["GET", "POST"])
@login_required
def new_pass():
    if request.method == "POST":
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        if password == confirmation:
            db.execute("UPDATE 'users' SET hash = ? WHERE id = ?", generate_password_hash(password), session['user_id'])
            return redirect('/')
        else:
            return apology('password must match confirmation')
    else:
        return render_template('new_pass.html')
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)



          
@app.route("/history")
@login_required
def history():
    if session['user_id'] == '':
        return apology("You do not have access", 400)
    gaurd = db.execute("SELECT gaurd FROM 'users' WHERE id = ?", session['user_id'])
    if gaurd[0]['gaurd'] == 'TRUE':
        return apology("You do not have access", 400)
    oldformat = date.today()
    datetimeobject = datetime.strptime(str(oldformat),'%Y-%m-%d')
    today = datetimeobject.strftime('%m/%d/%Y')
    all_old = db.execute("SELECT * FROM pending_session WHERE date < ? AND confirmed = 'TRUE'", today)
    for row in all_old:
        db.execute("INSERT INTO history (session_id, gaurd_id, user_id, time, address, date, length, payment) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row["session_id"], row["gaurd_id"], row['user_id'], row['time'], row['address'], row['date'], row['length'], row['payment'])
    db.execute("DELETE FROM pending_session WHERE date < ?", today)
    print(all_old)
    jobs = db.execute("SELECT * FROM 'history' JOIN 'users' ON history.gaurd_id=users.id WHERE user_id = ?", session["user_id"])
    print(jobs)
    return render_template("history.html", jobs=jobs)




@app.route("/medications", methods=["GET", "POST"])
@login_required
def medications():
    if request.method == "POST":
        med1 = {
            name = request.form.get('name1'),
            dosage = request.form.get('dose1')
            often = request.form.get('often1'),
            

        }
        if med1['often'] = 1:
            med1.update({
                stime = request.form.get('stime1')
                etime = request.form.get('etime1')
            })

        med2 = {
            name = request.form.get('name2'),
            dosage = request.form.get('dose2')
            often = request.form.get('often2'),
            

        }
        if med2['often'] = 1:
            med2.update({
                stime = request.form.get('stime2')
                etiime = request.form.get('etime2')
            })
    else:
        return render_template('medications.html')
