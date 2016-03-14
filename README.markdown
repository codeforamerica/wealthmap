#Primer Peso 2

Primer Peso is a django project for the Puerto Rican government to allow local businesses to find and explore opportunities.

##Install Instructions

Requires Postgres and Django be installed.  This project is developed and tested with Python 3.5 and Django 1.9.

  pip install -r requirements/app.txt

Copy the local_settings file and update the settings to fit your machine.

  cp local_settings.py.example local_settings.py

Create a database for the application by first logging into postgres (`psql`) then running:

  CREATE DATABASE primerpeso2;

Test that Django is working and pointed at your database(migrations not yet created).

  ./manage.py migrate

Create a user to log in to and manage the application.

  ./manage.py createsuperuser

Load seed data (the existing dataset from Puerto Rico).

  ./manage.py load_legacy_data
