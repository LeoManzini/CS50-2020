import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    stocks = db.execute("SELECT symbol, shares FROM portfolio WHERE id = :id ORDER BY symbol DESC", id = user_id)

    total = 0

    for stock in stocks:
        name = price = lookup(stock["symbol"])["name"]
        stock.update({ "name": name })
        price = lookup(stock["symbol"])["price"]
        stock.update({ "price": usd(price) })
        value = price * stock["shares"]
        stock.update({ "value": usd(value) })
        total = total + value

    row = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
    cash = row[0]["cash"]
    total = total + cash

    return render_template("index.html", stocks=stocks, cash=usd(cash), value=usd(total))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        quote = lookup(symbol)
        user_id = session["user_id"]

        if not symbol:
            return apology("missing symbol", 400)
        elif not shares:
            return apology("missing shares", 400)
        elif not quote:
            return apology("invalid symbol", 400)
        elif shares <= 0:
            return apology("number of shares must be a positive integer", 400)

        row = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = user_id)
        cash = row[0]["cash"]
        price = quote["price"]
        total = price * shares

        if cash < total:
            return apology("can't afford", 400)

        db.execute("INSERT INTO history (id, symbol, shares, price) VALUES (:id, :symbol, :shares, :price)",
            id = user_id,
            symbol = symbol,
            shares = shares,
            price = format(total, '.2f'))

        cash = cash - total
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=cash, user_id=user_id)

        portfolios = db.execute("SELECT shares FROM portfolio WHERE id = :id AND symbol = :symbol",
                        id = user_id,
                        symbol = symbol)

        # In case user already does have shares for purchased stock
        if len(portfolios) == 1:
            shares = portfolios[0]["shares"] + shares
            db.execute("UPDATE portfolio SET shares = :shares WHERE id = :id AND symbol = :symbol", shares = shares, id = user_id, symbol = symbol)
        else:
            db.execute("INSERT INTO portfolio (id, symbol, shares) VALUES (:id, :symbol, :shares)", id = user_id, symbol = symbol, shares = shares)

        flash("Bought!")
        return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]

    transactions = db.execute("SELECT date, symbol, shares, price FROM history WHERE id = :id ORDER BY date DESC", id=user_id)

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        symbol = request.form.get("symbol").upper()
        quote = lookup(symbol)

        if quote == None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == 'POST':

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not confirmation:
            return apology("must provide equal password", 400)

        elif request.form.get("password") != confirmation:
            return apology("passwords don't match", 400)

        row = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=username, hash=password)

        if not row:
            return apology("username taken", 400)

        session["user_id"] = row
        flash("Registered!")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        quote = lookup(symbol)

        if not symbol:
            return apology("must provide symbol", 400)
        elif shares <= 0:
            return apology("number of shares must be a positive integer", 400)
        if quote == None:
            return apology("invalid symbol", 400)

        stock = db.execute("SELECT SUM(shares) as total_shares FROM portfolio WHERE id = :id AND symbol = :symbol GROUP BY symbol", id=session["user_id"], symbol=symbol)

        if len(stock) != 1 or stock[0]["total_shares"] <= 0 or stock[0]["total_shares"] < shares:
            return apology("not enough shares", 400)

        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        cash = rows[0]["cash"]
        price = quote["price"] * shares

        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price=price, user_id=session["user_id"])
        db.execute("INSERT INTO portfolio (id, symbol, shares) VALUES(:id, :symbol, :shares)", id=session["user_id"], symbol=symbol, shares=-shares)

        flash("Sold!")
        return redirect("/")

    else:
        stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM portfolio WHERE id = :id GROUP BY symbol HAVING total_shares > 0", id=session["user_id"])
        return render_template("sell.html", stocks=stocks)

@app.route("/funds", methods=["GET", "POST"])
@login_required
def wallet():
    """Add more funds."""

    if request.method == "POST":

        user_id = session["user_id"]
        funds = request.form.get("funds")
        if not funds:
            return apology("specify the amount of money", 400)

        db.execute("UPDATE users SET cash = cash + :funds WHERE id = :user_id", user_id=user_id, funds=funds)

        flash("Funds add!")
        return redirect("/")

    else:
        return render_template("funds.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
