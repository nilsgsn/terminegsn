from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"
ADMIN_PASSWORD = "geheim123"  # ⚠️ Hier dein Admin-Passwort setzen


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", termine=data["termine"])


@app.route("/eintragen", methods=["POST"])
def eintragen():
    name = request.form.get("name")
    slot_index = int(request.form.get("slot"))
    data = load_data()

    if data["termine"][slot_index]["name"] == "":
        data["termine"][slot_index]["name"] = name
        save_data(data)
    return redirect(url_for("index"))


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            # Zurücksetzen
            data = load_data()
            for slot in data["termine"]:
                slot["name"] = ""
            save_data(data)
            return render_template("admin.html", success=True)
        else:
            return render_template("admin.html", error="Falsches Passwort.")
    return render_template("admin.html")
