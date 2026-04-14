import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session, flash
import db
import config
import events
import users

con = sqlite3.connect('database.db', timeout=10)
app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)


@app.route("/")
def index():
    all_events = events.get_events()
    return render_template("index.html", events=all_events)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    events = users.get_events(user_id)

    return render_template("show_user.html", user=user, events=events)


@app.route("/find_event")
def find_event():
    query = request.args.get("query")
    if query:
        results = events.find_events(query)
    else:
        query = ""
        results = []
    return render_template("find_event.html", query=query, results=results)

@app.route("/event/<int:event_id>")
def page(event_id):
    event = events.get_event(event_id)
    if not event:
        abort(404)
    return render_template("show_event.html", event=event)


@app.route("/update_event/<int:event_id>", methods=["GET", "POST"])
def update_event(event_id):
    require_login()
    if request.method == "GET":
        event = events.get_event(event_id)
        if not event:
            abort(404)
        if event["user_id"] != session["user_id"]:
            abort(403)
        return render_template("edit_event.html", event=event)

    if request.method == "POST":
        event_id = request.form["event_id"]
        event = events.get_event(event_id)
        if not event:
            abort(404)
        if event["user_id"] != session["user_id"]:
            abort(403)
        title = request.form["title"]
        if not title or len(title) > 60:
            abort(403)
        description = request.form["description"]
        if not description or len(description) > 1500:
            abort(403)
        time = request.form["time"]
        date = request.form["date"]
        location = request.form["location"]
        if not location or len(location) > 100:
            abort(403)

        events.edit_event(event_id, title, description, date, time, location)

        return redirect("/event/" + str(event_id))

@app.route("/new_event")
def new_event():
    require_login()
    return render_template("new_event.html")

@app.route("/create_event", methods=["POST"])
def create_event():
    require_login()

    # Seuraavaksi syötekentät ja tarkistus ettei syötteet ole tyhjiä tai liian pitkiä
    title = request.form["title"]
    if not title or len(title) > 60:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1500:
        abort(403)
    time = request.form["time"]
    date = request.form["date"]
    location = request.form["location"]
    if not location or len(location) > 100:
        abort(403)
    user_id = session["user_id"]
    events.add_event(title, description, date, time, location, user_id)

    return redirect("/")
@app.route("/remove_event/<int:event_id>", methods=["GET", "POST"])
def remove_event(event_id):
    require_login()
    if "user_id" not in session:
        flash("Sinun täytyy olla kirjautuneena poistaaksesi tapahtumia.")
        return redirect("/login")
    event = events.get_event(event_id)
    if not event:
        abort(404)

    if event["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_event.html", event=event)

    if request.method == "POST":
        try:
            if "remove" in request.form:
                events.remove_event(event_id)
                flash("Tapahtuma on poistettu onnistuneesti.")
                return redirect("/")
            else:
                return redirect("/event/" + str(event_id))
        except Exception as e:
            # Tulosta virhe lokiin ja näytä käyttäjälle virheviesti
            print(f"Virhe tapahtuman poistamisessa: {e}")
            flash("Tapahtuman poistamisessa tapahtui virhe.")
            return redirect("/event/" + str(event_id))


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return render_template("registration_success.html", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

