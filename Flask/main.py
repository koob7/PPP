# Dołączanie modułu flask

from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
import sqlite3
from flask import Flask, session
from flask_session import Session

# Tworzenie obiektu aplikacji
app = Flask(__name__)
# Tworzenie obsługi sesji
sess = Session()
# Ścieżka do pliku bazy danych w sqlite
DATABASE = "database.db"


@app.route("/cd", methods=["GET", "POST"])
def create_db():
    # Połączenie sie z bazą danych
    conn = sqlite3.connect(DATABASE)
    # Stworzenie tabeli w bazie danych za pomocą sqlite3
    conn.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, admin boolean)"
    )
    conn.execute("CREATE TABLE books (title TEXT, author TEXT)")
    # Zakończenie połączenia z bazą danych
    conn.close()

    return index()


@app.route("/", methods=["GET", "POST"])
def index():
    con = sqlite3.connect(DATABASE)

    # Pobranie danych z tabeli
    cur = con.cursor()
    cur.execute("select * from books")
    users = cur.fetchall()

    if "user" in session:
        return (
            render_template("t4.html", userdata=session["user"])
            + "<a href='/users'> users </a>"
            + "<br><a href='/logout'> logout </a>"
        )
    else:
        return render_template("t1.html")


@app.route("/users", methods=["GET", "POST"])
def users():
    con = sqlite3.connect(DATABASE)

    # Pobranie danych z tabeli
    cur = con.cursor()
    cur.execute("select * from users")
    users = cur.fetchall()

    return render_template("t5.html", users=users) + "<br><a href='/'> home </a>"


@app.route("/login", methods=["GET", "POST"])
def login():
    con = sqlite3.connect(DATABASE)

    # Pobranie danych z tabeli
    cur = con.cursor()
    # cur.execute("select * from users")
    users = cur.fetchall()
    session["user"] = "username"
    return "Sesja została utworzona <br> <a href='/'> Dalej </a> "


@app.route("/add_book", methods=["POST"])
def add_book():
    author = request.form["author"]
    title = request.form["title"]

    # Dodanie użytkownika do bazy danych
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO books (author,title) VALUES (?,?)", (author, title))
    con.commit()
    con.close()

    return "Dodano książkę do bazy danych <br>" + index()


@app.route("/add_user", methods=["POST"])
def add_user():
    login = request.form["login"]
    password = request.form["password"]
    # Checkbox is only present in form data when checked
    admin = request.form.get("admin") == "on"

    # Dodanie użytkownika do bazy danych
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username,password,admin) VALUES (?,?,?)",
        (login, password, admin),
    )
    con.commit()
    con.close()

    return "Dodano użytkownika do bazy danych <br>" + users()


@app.route("/logout", methods=["GET"])
def logout():
    # Jeżeli sesja klienta istnieje - usunięcie sesji
    if "user" in session:
        session.pop("user")
    else:
        # Przekierowanie klienta do strony początkowej
        redirect(url_for("index"))

    return "Wylogowano <br>  <a href='/'> Powrót </a>"


# Uruchomienie aplikacji w trybie debug
app.secret_key = "super secret key"
app.config["SESSION_TYPE"] = "filesystem"
sess.init_app(app)
app.config.from_object(__name__)
app.debug = True
app.run()
