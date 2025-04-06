import streamlit as st
import json
import os

# ==== Einstellungen ====
DATA_FILE = "data.json"
ADMIN_PASSWORD = "geheim123"  # Ändere das Passwort hier!

# ==== Daten laden / speichern ====
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"termine": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ==== Initialisierung ====
def initialize():
    if not os.path.exists(DATA_FILE):
        data = {
            "termine": [
                {"zeit": "10:00 - 10:30", "name": ""},
                {"zeit": "10:30 - 11:00", "name": ""},
                {"zeit": "11:00 - 11:30", "name": ""},
                {"zeit": "11:30 - 12:00", "name": ""},
                {"zeit": "12:00 - 12:30", "name": ""}
            ]
        }
        save_data(data)

initialize()

# ==== Oberfläche ====
st.set_page_config(page_title="Terminliste", layout="centered")
st.title("Beratungstermine Frau Jeyapala")

tab1, tab2 = st.tabs(["➕ Termin eintragen", "🔐 Adminbereich"])

# === Tab 1: Termin eintragen ===
with tab1:
    data = load_data()
    freie_slots = [t["zeit"] for t in data["termine"] if t["name"] == ""]

    if freie_slots:
        name = st.text_input("Dein Name")
        slot = st.selectbox("Wähle einen freien Termin", freie_slots)

        if st.button("Eintragen"):
            if not name.strip():
                st.warning("Bitte gib deinen Namen ein.")
            else:
                for t in data["termine"]:
                    if t["zeit"] == slot and t["name"] == "":
                        t["name"] = name
                        save_data(data)
                        st.success(f"Du wurdest für {slot} eingetragen!")
                        st.rerun()
    else:
        st.info("Alle Termine sind bereits vergeben.")

    st.subheader("📋 Aktuelle Einträge")
    for t in data["termine"]:
        status = t["name"] if t["name"] else "🟢 Frei"
        st.write(f"**{t['zeit']}**: {status}")

# === Tab 2: Adminbereich ===
with tab2:
    st.write("⚠️ Hier kannst du die Liste zurücksetzen. Passwort erforderlich.")
    pw = st.text_input("Admin-Passwort", type="password")
    if st.button("Liste zurücksetzen"):
        if pw == ADMIN_PASSWORD:
            for t in data["termine"]:
                t["name"] = ""
            save_data(data)
            st.success("Alle Termine wurden zurückgesetzt.")
            st.experimental_rerun()
        else:
            st.error("Falsches Passwort!")
# Ganz unten auf der Seite
# Hinweis ganz unten
st.markdown("<hr>", unsafe_allow_html=True)  # Trennlinie für besseren Look

# Ganz unten auf der Seite
st.markdown(
    """
    <style>
        .footer {
            display: flex;
            justify-content: center;
            align-items: center;
            padding-top: 20px;
        }
        .footer img {
            max-height: 100px;
        }
    </style>
    <div class="footer">
        <img src="images/school_logo.png" alt="Logo der Schule">
    </div>
    """,
    unsafe_allow_html=True
)
