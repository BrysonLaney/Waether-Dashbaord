import os
import datetime

import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash

import firebase_admin
from firebase_admin import credentials, firestore


# -----------------------------
# Flask & Firestore setup
# -----------------------------

app = Flask(__name__)
# In a real app, keep this secret and read from environment
app.secret_key = "change-this-secret-key"

def init_firestore():
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firestore()


# -----------------------------
# Firestore helper functions
# -----------------------------

def get_user(user_id: str):
    doc = db.collection("users").document(user_id).get()
    if doc.exists:
        return doc.to_dict()
    return None


def create_or_update_user(user_id: str, name: str, default_units: str = "metric"):
    now = datetime.datetime.utcnow().isoformat()
    db.collection("users").document(user_id).set(
        {
            "name": name,
            "default_units": default_units,
            "updated_at": now,
            "created_at": firestore.SERVER_TIMESTAMP,  # first write only
        },
        merge=True,
    )


def update_user_units(user_id: str, new_units: str):
    now = datetime.datetime.utcnow().isoformat()
    db.collection("users").document(user_id).update(
        {
            "default_units": new_units,
            "updated_at": now,
        }
    )


def list_locations(user_id: str):
    docs = (
        db.collection("users")
        .document(user_id)
        .collection("locations")
        .order_by("nickname")
        .stream()
    )
    locations = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        locations.append(data)
    return locations


def add_location(user_id: str, city: str, country_code: str, nickname: str):
    now = datetime.datetime.utcnow().isoformat()
    db.collection("users").document(user_id).collection("locations").add(
        {
            "city": city,
            "country_code": country_code,
            "nickname": nickname,
            "created_at": now,
            "updated_at": now,
        }
    )


def delete_location(user_id: str, loc_id: str):
    (
        db.collection("users")
        .document(user_id)
        .collection("locations")
        .document(loc_id)
        .delete()
    )


def get_location(user_id: str, loc_id: str):
    doc = (
        db.collection("users")
        .document(user_id)
        .collection("locations")
        .document(loc_id)
        .get()
    )
    if doc.exists:
        data = doc.to_dict()
        data["id"] = doc.id
        return data
    return None


# -----------------------------
# Weather API
# -----------------------------

def get_weather_for_city(city: str, country_code: str, units: str = "metric"):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {"error": "OPENWEATHER_API_KEY environment variable is not set."}

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": f"{city},{country_code}",
        "appid": api_key,
        "units": units,
    }

    try:
        resp = requests.get(base_url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        return {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temp": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "description": data.get("weather", [{}])[0].get("description"),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "units": units,
        }
    except requests.RequestException as e:
        return {"error": f"Error calling weather API: {e}"}


# -----------------------------
# Flask routes
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Landing page: ask for a user ID.
    If the user exists, log them in; otherwise allow creating a new profile.
    """
    if request.method == "POST":
        user_id = request.form.get("user_id", "").strip()
        name = request.form.get("name", "").strip()
        units = request.form.get("default_units", "metric")

        if not user_id:
            flash("Please enter a user ID.")
            return redirect(url_for("index"))

        user = get_user(user_id)
        if user is None:
            # Create a new user if no existing record
            if not name:
                name = user_id  # fallback
            create_or_update_user(user_id, name, units)
            flash("New user created.", "success")
        else:
            flash("Welcome back!", "success")

        session["user_id"] = user_id
        return redirect(url_for("dashboard"))

    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """
    Main dashboard view: show user info, locations, and optional weather data.
    """
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    user = get_user(user_id)
    if not user:
        flash("User not found. Please log in again.")
        session.pop("user_id", None)
        return redirect(url_for("index"))

    locations = list_locations(user_id)

    weather_data = None
    loc_id = request.args.get("loc")
    if loc_id:
        loc = get_location(user_id, loc_id)
        if loc:
            units = user.get("default_units", "metric")
            weather_data = get_weather_for_city(
                loc["city"], loc["country_code"], units
            )
            if "error" in weather_data:
                flash(weather_data["error"], "error")

    return render_template(
        "dashboard.html",
        user_id=user_id,
        user=user,
        locations=locations,
        weather=weather_data,
    )


@app.route("/set_units", methods=["POST"])
def set_units():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    new_units = request.form.get("default_units", "metric")
    if new_units not in ("metric", "imperial"):
        flash("Invalid units selection.", "error")
    else:
        update_user_units(user_id, new_units)
        flash(f"Default units updated to {new_units}.", "success")

    return redirect(url_for("dashboard"))


@app.route("/add_location", methods=["POST"])
def add_location_route():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    city = request.form.get("city", "").strip()
    country_code = request.form.get("country_code", "").strip().upper()
    nickname = request.form.get("nickname", "").strip()

    if not city or not country_code or not nickname:
        flash("City, country code, and nickname are required.", "error")
        return redirect(url_for("dashboard"))

    add_location(user_id, city, country_code, nickname)
    flash(f"Location '{nickname}' added.", "success")
    return redirect(url_for("dashboard"))


@app.route("/delete_location/<loc_id>", methods=["POST"])
def delete_location_route(loc_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    delete_location(user_id, loc_id)
    flash("Location deleted.", "success")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # For local development; in production you'd use a WSGI server
    app.run(debug=True)
