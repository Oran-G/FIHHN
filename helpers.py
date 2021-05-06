import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Your Account Sid and Auth Token from twilio.com/user/account
# Store them in the environment variables:
# "TWILIO_ACCOUNT_SID" and "TWILIO_AUTH_TOKEN"
account_sid = "ACb5d9be6303b400c0254a44656e990440"
# Your Auth Token from twilio.com/console
auth_token  = "f730e6d53fc966ab9e1bb8ef710eb9af"
client1 = Client(account_sid, auth_token)

def is_valid_number(number):
    try:
        response = client1.lookups.phone_numbers(number).fetch(type="carrier")
        return True
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        else:
            raise e
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):

        #Escape special characters.

       #https://github.com/jacebrowning/memegen#special-characters

        for old, new in [("-", "-"), (" ", " "), ("_", "_"), ("?", "?"),
                         ("%", "%"), ("#", "#"), ("/", "/"), ("\"", "\"")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=message, message=None), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


