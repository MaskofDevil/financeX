import datetime
import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# manage.py
from manage import prompt, password_check, login_required, login_not_required, lookup, getDetails, usd

# Configure app
app = Flask(__name__)


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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///financeX.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_not_required
def index():
    """ Show landing page """

    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
@login_not_required
def login():
    """ Show login form """

    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("Must provide a Username", "alert-warning")
            return render_template("login.html")

        if not password:
            flash("Must provide Password", "alert-warning")
            return render_template("login.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1:
            flash("Invalid Username", "alert-warning")
            return render_template("login.html")

        if not check_password_hash(rows[0]["hash"], password):
            flash("Invalid Password", "alert-warning")
            return render_template("login.html")

        session["user_id"] = rows[0]["id"]
        flash("Successfully logged in!", "alert-success")
        return redirect("/loading")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
@login_not_required
def register():
    """ Show register form """

    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cpassword = request.form.get("confirm_password")

        if not username:
            flash("Must provide a Username", "alert-warning")
            return render_template("register.html")

        if not password:
            flash("Must provide a Password", "alert-warning")
            return render_template("register.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) == 1:
            flash("Username is taken", "alert-warning")
            return render_template("register.html")

        if not password_check(password):
            flash("Password doesn't satisfy parameters", "alert-warning")
            return render_template("register.html")

        if not password == cpassword:
            flash("Passwords doesn't match", "alert-warning")
            return render_template("register.html")

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                   username, generate_password_hash(password))

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        flash("Successfully registered!", "alert-success")
        return redirect("/loading")

    else:
        return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    session.clear()
    flash("Successfully logged out!", "alert-success")
    return redirect("/")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change password"""

    if request.method == "POST":

        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        cpassword = request.form.get("confirm_password")

        if not old_password:
            flash("Must provide old password", "alert-warning")
            return render_template("change.html")

        if not new_password:
            flash("Must provide a new password", "alert-warning")
            return render_template("change.html")

        if old_password == new_password:
            flash("New password is same as old password", "alert-warning")
            return render_template("change.html")

        if not new_password == cpassword:
            flash("Passwords doesn't match", "alert-warning")
            return render_template("change.html")

        if not password_check(new_password):
            flash("Password doesn't satisfy parameters", "alert-warning")
            return render_template("change.html")

        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   generate_password_hash(new_password), session["user_id"])
        session.clear()
        flash("Password changed! Login", "alert-success")
        return redirect("/")

    else:
        return render_template("change.html")


@app.route("/history")
@login_required
def history():
    """ Show history of transactions """

    rows = db.execute(
        "SELECT symbol, shares, time FROM history WHERE user_id = ? ORDER BY time DESC", session["user_id"])
    return render_template("history.html", rows=rows)


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    """ Show homepage containing search bar and user owned shares """

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if symbol:
            return redirect(f'/home/{symbol}')

        sell = request.form.get("sell")
        if sell:
            shares = request.form.get("shares")

            share = db.execute(
                "SELECT shares FROM transactions WHERE symbol = ?", sell)
            share = share[0]["shares"]

            if int(shares) > share:
                return prompt("too many shares")

            look = lookup(sell)

            cost = int(shares) * look["price"]

            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                       cost, session["user_id"])

            db.execute("UPDATE transactions SET shares = ? WHERE user_id = ? AND symbol = ?",
                       share - int(shares), session["user_id"], sell)

            db.execute("INSERT INTO history (user_id, symbol, shares, price, time) VALUES(?, ?, ?, ?, ?)",
                       session["user_id"], sell, -int(shares), look["price"], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            if (share - int(shares)) == 0:
                db.execute(
                    "DELETE FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], sell)

            return redirect("/loading")

        return redirect("/loading")

    else:
        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])

        rows = db.execute(
            "SELECT * FROM transactions WHERE user_id = ?", session["user_id"])

        totalDiff = 0
        for r in rows:
            look = lookup(r["symbol"])
            if look == None:
                return prompt("API unreachable")
            r["diff"] = int(look["price"] - r["price"])
            totalDiff += r["diff"] * r["shares"]

        return render_template("home.html", rows=rows, cash=cash[0]["cash"], totalDiff=totalDiff)


@app.route("/loading")
@login_required
def loading():
    """ Display loading screen """
    
    return render_template("loading.html")


@app.route("/home/<symbol>", methods=["GET", "POST"])
@login_required
def details(symbol):
    """ Stock details based on symbol """

    if request.method == "POST":
        look = lookup(symbol)
        shares = request.form.get("shares")
        cost = int(shares) * look["price"]
        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])

        if cash[0]["cash"] >= cost:
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?",
                       cost, session["user_id"])

            rows = db.execute(
                "SELECT shares FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)

            if len(rows) == 1:
                db.execute("UPDATE transactions SET shares = shares + ?, price = ? WHERE user_id = ? AND symbol = ?",
                           shares, look["price"], session["user_id"], symbol)

                db.execute("INSERT INTO history (user_id, symbol, shares, price, time) VALUES(?, ?, ?, ?, ?)",
                           session["user_id"], symbol, shares, look["price"], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            else:
                db.execute("INSERT INTO transactions (user_id, symbol, shares, name, price) VALUES(?, ?, ?, ?, ?)",
                           session["user_id"], look["symbol"], shares, look["name"], look["price"])

                db.execute("INSERT INTO history (user_id, symbol, shares, price, time) VALUES(?, ?, ?, ?, ?)",
                           session["user_id"], symbol, shares, look["price"], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            flash("Transaction successful", "alert-success")
            return redirect("/loading")

        else:
            flash("You don't have enough money", "alert-warning")
            return redirect("/loading")
    else:
        look = lookup(symbol)
        info = getDetails(symbol)

        if look and info:
            return render_template("details.html", look=look, info=info)

        else:
            flash("No such symbol", "alert-warning")
            return prompt("Invalid Symbol")


def errorhandler(e):
    """Handle error"""

    if not isinstance(e, HTTPException):
        e = InternalServerError()
    flash(e.name, "alert-failure")
    return prompt(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
