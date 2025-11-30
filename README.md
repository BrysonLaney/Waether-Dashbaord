Weather Dashboard - Cloud Database Application

This project is a cloud-integrated Weather Dashboard designed to demonstrate interaction between a Python application, an external weather API, and a cloud database. The system allows users to create a profile, save favorite locations, and retrieve real-time weather information while persisting all preferences using Google Firestore.

This project showcases full CRUD operations, external API integration, and a scalable data structure similar to those used in real software engineering environments.

Software Demo Video

https://youtu.be/2Npglss7xls

Cloud Database

This application uses Google Firestore, a NoSQL cloud document database. The data model was intentionally structured to demonstrate related collections and support cloud-based CRUD operations.

Data Model
Collection: users

Each user is stored as a document using a unique user ID. Example fields include:

{
  "name": "Bryson",
  "default_units": "metric",
  "created_at": "...",
  "updated_at": "..."
}

Subcollection: users/{user_id}/locations

Each user may have multiple saved locations. Example fields include:

{
  "city": "Boise",
  "country_code": "US",
  "nickname": "Home",
  "created_at": "...",
  "updated_at": "..."
}

CRUD Operations Implemented
Operation	Users	Locations
Create	Create a new user profile	Add a new saved location
Read	Retrieve stored user information	List all saved locations
Update	Change temperature units or name	Update the nickname of a location
Delete	—	Remove a saved location

This fully satisfies the requirement to insert, modify, delete, and retrieve data in a cloud database.

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


A menu will appear that allows you to create a profile, manage saved locations, and fetch weather data.

Useful Websites

The following resources were valuable during development:

https://firebase.google.com/docs/firestore/quickstart

https://firebase.google.com/docs/firestore/data-model

https://openweathermap.org/api

https://requests.readthedocs.io/en/latest/

https://stackoverflow.com

Future Work

Planned improvements and potential features:

Implement Firebase Authentication for secure user login

Add Firestore snapshot listeners for real-time database updates

Build a graphical interface using Tkinter, PyQt, or a Flask web UI

Add multi-day forecasts or historical weather data

Improve error handling and input validation

Store usage logs or weather retrieval history