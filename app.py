from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_NAME = "hotel.db"

ROOMS = [
    {"id": 1, "name": "Deluxe Room", "price": 2500, "capacity": 2, "description": "Comfortable room with a queen bed and modern amenities.", "icon": "🛏️"},
    {"id": 2, "name": "Family Suite", "price": 4200, "capacity": 4, "description": "Spacious suite for families, with a separate sitting area.", "icon": "🏨"},
    {"id": 3, "name": "Premium Room", "price": 3500, "capacity": 2, "description": "Elegant room with premium furnishings and city views.", "icon": "✨"},
    {"id": 4, "name": "Executive Suite", "price": 6000, "capacity": 3, "description": "A larger suite for business and special stays.", "icon": "🌆"}
]

def get_db():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guest_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                room_name TEXT NOT NULL,
                check_in TEXT NOT NULL,
                check_out TEXT NOT NULL,
                guests INTEGER NOT NULL,
                total_price INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

@app.route("/")
def index():
    return render_template("index.html", rooms=ROOMS)

@app.route("/book", methods=["POST"])
def book():
    guest_name = request.form.get("guest_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    check_in = request.form.get("check_in", "")
    check_out = request.form.get("check_out", "")
    room_id = request.form.get("room_id", type=int)
    guests = request.form.get("guests", type=int)

    room = next((r for r in ROOMS if r["id"] == room_id), None)
    try:
        start = datetime.strptime(check_in, "%Y-%m-%d").date()
        end = datetime.strptime(check_out, "%Y-%m-%d").date()
        nights = (end - start).days
    except ValueError:
        nights = 0

    if not all([guest_name, email, phone, room, check_in, check_out, guests]):
        flash("Please complete all booking fields.", "error")
        return redirect(url_for("index") + "#booking")
    if nights < 1:
        flash("Check-out date must be after check-in date.", "error")
        return redirect(url_for("index") + "#booking")
    if guests < 1 or guests > room["capacity"]:
        flash(f'{room["name"]} allows 1 to {room["capacity"]} guests.', "error")
        return redirect(url_for("index") + "#booking")

    total = nights * room["price"]
    with get_db() as db:
        db.execute("""
            INSERT INTO bookings
            (guest_name, email, phone, room_name, check_in, check_out, guests, total_price, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (guest_name, email, phone, room["name"], check_in, check_out, guests, total,
              datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    flash(f"Booking saved successfully! Estimated total: ₹{total:,} for {nights} night(s).", "success")
    return redirect(url_for("index") + "#booking")

@app.route("/admin")
def admin():
    with get_db() as db:
        bookings = db.execute("SELECT * FROM bookings ORDER BY id DESC").fetchall()
        count = db.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
        revenue = db.execute("SELECT COALESCE(SUM(total_price), 0) FROM bookings").fetchone()[0]
    return render_template("admin.html", bookings=bookings, count=count, revenue=revenue)

@app.route("/delete/<int:booking_id>", methods=["POST"])
def delete_booking(booking_id):
    with get_db() as db:
        db.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    flash("Booking deleted.", "success")
    return redirect(url_for("admin"))

init_db()

if __name__ == "__main__":
    app.run(debug=True)
