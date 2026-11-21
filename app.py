import os
import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "development-only-change-this")
DATABASE = os.path.join(app.root_path, "users.db")


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone_number TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)


init_db()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("About.html")


@app.route("/services")
def services():
    return render_template("Services.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone_number = request.form.get("phone_number", "").strip()
        password = request.form.get("password", "")
        agree_terms = request.form.get("agree_terms")

        if not all((full_name, email, phone_number, password, agree_terms)):
            error = "Please complete every field and agree to the Terms & Conditions and Privacy Policy."
        elif len(password) < 8:
            error = "Password must be at least 8 characters long."
        else:
            try:
                with get_db() as connection:
                    connection.execute(
                        "INSERT INTO users (full_name, email, phone_number, password_hash) VALUES (?, ?, ?, ?)",
                        (full_name, email, phone_number, generate_password_hash(password)),
                    )
                session["user_email"] = email
                session["user_name"] = full_name
                return redirect(url_for("home"))
            except sqlite3.IntegrityError:
                error = "An account with that email address already exists."

    return render_template("signup.html", error=error)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        with get_db() as connection:
            user = connection.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session["user_email"] = user["email"]
            session["user_name"] = user["full_name"]
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("dashboard"))

        error = "Invalid email address or password."

    return render_template("signin.html", error=error)


@app.route("/dashboard")
def dashboard():
    if not session.get("user_email"):
        return redirect(url_for("signin", next=request.path))
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
