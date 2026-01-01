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
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, admin boolean)"
    )
    conn.execute("CREATE TABLE IF NOT EXISTS books (title TEXT, author TEXT)")

    # Tworzenie domyślnych użytkowników
    conn.execute(
        "INSERT INTO users (username, password, admin) VALUES (?, ?, ?)",
        ("user", "user", 0),
    )
    conn.execute(
        "INSERT INTO users (username, password, admin) VALUES (?, ?, ?)",
        ("admin", "admin", 1),
    )
    conn.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        ("The Odyssey", "Homer"),
    )
    conn.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        ("Narnia", "C.S. Lewis"),
    )
    conn.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        ("Hamlet", "William Shakespeare"),
    )
    # Zakończenie połączenia z bazą danych
    conn.commit()
    conn.close()

    return index()


@app.route("/", methods=["GET", "POST"])
def index():
    con = sqlite3.connect(DATABASE)

    # Pobranie danych z tabeli
    cur = con.cursor()
    cur.execute("select * from books")
    books = cur.fetchall()
    con.close()

    if "user" in session:
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        # Sprawdzenie czy użytkownik ma uprawnienia admina
        cur.execute("SELECT admin FROM users WHERE username = ?", (session["user"],))
        user_data = cur.fetchone()
        con.close()

        if user_data and user_data[0]:
            return (
                render_template("t2.html", books=books, userdata=session["user"])
                + "<a href='/users'> users </a>"
                + "<br><a href='/logout'> logout </a>"
            )
        else:
            return (
                render_template("t2.html", books=books, userdata=session["user"])
                + "<br><a href='/logout'> logout </a>"
            )
    else:
        return render_template("t1.html")


@app.route("/users", methods=["GET", "POST"])
def users():

    # Sprawdzenie czy użytkownik jest zalogowany
    if "user" not in session:
        return "Access denied. Please <a href='/'> login </a> to view users."

    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    # Sprawdzenie czy użytkownik ma uprawnienia admina
    cur.execute("SELECT admin FROM users WHERE username = ?", (session["user"],))
    user_data = cur.fetchone()

    # Jeżeli użytkownik nie istnieje lub nie jest adminem
    if not user_data or not user_data[0]:
        con.close()
        return "Access denied. Admin privileges required. <br><a href='/'> home </a>"

    # Pobranie danych z tabeli użytkowników
    cur.execute("select * from users")
    users = cur.fetchall()
    con.close()

    return render_template("t3.html", users=users) + "<br><a href='/'> home </a>"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["login"]
        password = request.form["password"]

        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        # Check if user exists with matching password
        cur.execute(
            "SELECT username FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        user = cur.fetchone()
        con.close()

        if user:
            session["user"] = user[0]
            return redirect(url_for("index"))
        else:
            return "Invalid credentials. Please try again. " + index()

    return redirect(url_for("index"))


@app.route("/add_book", methods=["POST"])
def add_book():
    author = request.form["author"]
    title = request.form["title"]

    # Dodanie użytkownika do bazy danych
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    # Sprawdzenie czy użytkownik już istnieje
    cur.execute("SELECT title FROM books WHERE title = ?", (title,))
    existing_book = cur.fetchone()

    if existing_book:
        con.close()
        return "!Book already exists.!" + index()

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

    # Sprawdzenie czy użytkownik już istnieje
    cur.execute("SELECT username FROM users WHERE username = ?", (login,))
    existing_user = cur.fetchone()

    if existing_user:
        con.close()
        return "!User already exists.!" + users()

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

    return redirect(url_for("index"))


@app.route("/user/<user_identifier>", methods=["GET"])
def user(user_identifier):
    # Sprawdzenie czy użytkownik jest zalogowany
    if "user" not in session:
        return "Access denied. Please <a href='/'> login </a>"
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    # Sprawdzenie czy zalogowany użytkownik ma uprawnienia admina
    cur.execute("SELECT admin FROM users WHERE username = ?", (session["user"],))
    user_data = cur.fetchone()

    # Jeżeli użytkownik nie jest adminem
    if not user_data or not user_data[0]:
        con.close()
        return (
            "Access denied. Admin privileges required. <br><a href='/users'> back </a>"
        )

    # Pobranie danych wybranego użytkownika po ID lub loginie
    if user_identifier.isdigit():
        cur.execute(
            "SELECT id, username, password, admin FROM users WHERE id = ?",
            (user_identifier,),
        )
    else:
        cur.execute(
            "SELECT id, username, password, admin FROM users WHERE username = ?",
            (user_identifier,),
        )

    selected_user = cur.fetchone()
    con.close()

    if not selected_user:
        return "User not found. <br><a href='/users'> back </a>"

    return render_template("t4.html", selected_user=selected_user)


# Uruchomienie aplikacji w trybie debug
app.secret_key = "super secret key"
app.config["SESSION_TYPE"] = "filesystem"
sess.init_app(app)
app.config.from_object(__name__)
app.debug = True
app.run()
