import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-secret-in-production")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@localhost:3306/clinfo",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)

    invoices = db.relationship("Invoice", backref="user", lazy=True)
    stocks = db.relationship("StockItem", backref="user", lazy=True)
    debts = db.relationship("Debt", backref="user", lazy=True)


class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    invoice_no = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Неплатена")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class StockItem(db.Model):
    __tablename__ = "stock_items"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Numeric(12, 2), nullable=False)
    unit = db.Column(db.String(30), nullable=False, default="бр.")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Debt(db.Model):
    __tablename__ = "debts"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    state = db.Column(db.String(50), nullable=False, default="Дължима")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect(url_for("dashboard"))

        flash("Невалидно име или парола.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    user = User.query.get_or_404(user_id)

    invoices = Invoice.query.filter_by(user_id=user_id).order_by(Invoice.date.desc()).all()
    stocks = StockItem.query.filter_by(user_id=user_id).order_by(StockItem.item_name.asc()).all()
    debts = Debt.query.filter_by(user_id=user_id).order_by(Debt.due_date.asc().nulls_last()).all()

    total_invoices = sum(float(item.amount) for item in invoices)
    total_debts = sum(float(item.amount) for item in debts)

    return render_template(
        "dashboard.html",
        user=user,
        invoices=invoices,
        stocks=stocks,
        debts=debts,
        total_invoices=total_invoices,
        total_debts=total_debts,
    )


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Базата е инициализирана.")


@app.cli.command("create-user")
def create_user():
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    full_name = input("Full name: ").strip()

    if User.query.filter_by(username=username).first():
        print("Потребител с това име вече съществува.")
        return

    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        full_name=full_name or username,
    )
    db.session.add(user)
    db.session.commit()
    print("Потребителят е създаден.")


if __name__ == "__main__":
    app.run(debug=True)
