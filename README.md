Weather Dashboard - Cloud Database Application

This project is a cloud-integrated Weather Dashboard designed to demonstrate interaction between a Python application, an external weather API, and a cloud database. The system allows users to create a profile, save favorite locations, and retrieve real-time weather information while persisting all preferences using Google Firestore.

Software Demo Video

https://youtu.be/2Npglss7xls

Cloud Database

This application uses Google Firestore, a NoSQL cloud document database. The data model was intentionally structured to demonstrate related collections and support cloud-based CRUD operations.


Development Environment
Tools and Technologies

Python 3.10+

Google Firebase / Firestore

Visual Studio Code

OpenWeatherMap API

Python Libraries Used

firebase-admin — Firestore integration

requests — API communication

datetime — Timestamps and formatting


Install required libraries:

pip install firebase-admin requests


Running the Program

Follow these steps to run the Weather Dashboard:

1. Configure Firebase

Create a Firebase project

Enable Firestore

Generate a Service Account Key (JSON)

Save it as serviceAccountKey.json in the project directory

2. Configure the Weather API

Set your OpenWeatherMap API key as an environment variable.

Windows PowerShell:

setx OPENWEATHER_API_KEY "your_api_key_here"


Mac/Linux:

export OPENWEATHER_API_KEY="your_api_key_here"

3. Start the Application
python weather_dashboard.py

4. navigate to the webpage
http://127.0.0.1:5000/


Useful Websites

The following resources were valuable during development:

https://firebase.google.com/docs/firestore/quickstart

https://firebase.google.com/docs/firestore/data-model

https://openweathermap.org/api

https://requests.readthedocs.io/en/latest/

https://stackoverflow.com


Future Work:

Add Firestore snapshot listeners for real-time database updates

Build a graphical interface using Tkinter, PyQt, or a Flask web UI

Add multi-day forecasts or historical weather data
