# GrandStay — Python Hotel Management System

A beginner-friendly hotel reservation project built with **Python Flask, SQLite, HTML, CSS and Bootstrap**.

## Features
- Room listings and prices
- Reservation form with basic validation
- Automatic estimated price calculation
- SQLite database stores booking records
- Admin dashboard shows bookings and estimated revenue
- Delete booking option
- Responsive layout

## Run on your computer (Windows)
1. Install Python 3.10 or newer from https://www.python.org/downloads/
2. Extract this ZIP folder.
3. Open Command Prompt inside the extracted project folder.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the application:
   ```bash
   python app.py
   ```
6. Open the local address shown in the terminal, usually http://127.0.0.1:5000
7. Open the dashboard at http://127.0.0.1:5000/admin

The SQLite database `hotel.db` is created automatically when the app starts.

## Put it on GitHub
1. Sign in to GitHub and create a new repository, for example `hotel-management-system-python`.
2. Upload the contents of this folder (upload the files and folders, not the ZIP file).
3. Commit the files.

**Important:** GitHub stores the Python source but GitHub Pages cannot run Flask/Python applications. To publish it as a live website, deploy the repository to a Python-capable host such as Render or PythonAnywhere. Deployment availability and free-plan limits can change. For Render, this project includes a `Procfile`; set the build command to `pip install -r requirements.txt` and the start command to `gunicorn app:app`.

## Academic demo notes
- This is a learning/demo project, not production-ready hotel software.
- The admin page has no login protection. Add authentication before real use.
- The default SQLite database is local to the running instance. For some hosted platforms, local files may not persist across redeployments or restarts; use a managed database for long-term hosted data.
