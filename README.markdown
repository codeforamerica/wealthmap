#Primer Peso 2

Primer Peso is a django project for the Puerto Rican government to allow local businesses to find and explore opportunities.

##Install Instructions

Requires Postgres and Django be installed.  This project is developed and tested with Python 3.5 and Django 1.9.

  pip install -r requirements/apps.txt

Copy the local_settings file and update the settings to fit your machine.

  cp local_settings.py.example local_settings.py

Test that Django is working and pointed at your database(migrations not yet created).

  ./manage migrate

