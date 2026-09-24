from flask import Flask, request, jsonify, send_from_directory, session, redirect
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

app.secret_key = "sree-venkateswara-admin-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "orders.db")


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            pincode TEXT NOT NULL,
            items TEXT NOT NULL,
            total REAL NOT NULL,
            payment_status TEXT NOT NULL,
            order_status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# =========================
# WEBSITE
# =========================

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


# =========================
# ADMIN LOGIN
# =========================

@app.route("/admin-login")
def admin_login():
    if session.get("admin_logged_in"):
        return redirect("/admin")

    return send_from_directory(
        os.path.join(BASE_DIR, "admin"),
        "admin-login.html"
    )


@app.route("/api/admin-login", methods=["POST"])
def admin_login_api():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Login data missing."
        }), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")

    # Admin credentials
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "Admin@123"

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

        session["admin_logged_in"] = True

        return jsonify({
            "success": True,
            "message": "Login successful."
        })

    return jsonify({
        "success": False,
        "message": "Invalid username or password."
    }), 401


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin")
def admin():

    if not session.get("admin_logged_in"):
        return redirect("/admin-login")

    return send_from_directory(
        os.path.join(BASE_DIR, "admin"),
        "admin.html"
    )


# =========================
# ADMIN LOGOUT
# =========================

@app.route("/admin-logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect("/admin-login")


# =========================
# CREATE ORDER
# =========================

@app.route("/api/orders", methods=["POST"])
def create_order():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No order data received."
        }), 400

    customer_name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    address = data.get("address", "").strip()
    pincode = data.get("pincode", "").strip()
    items = data.get("items", [])
    total = data.get("total", 0)

    if not customer_name:
        return jsonify({
            "success": False,
            "message": "Name is required."
        }), 400

    if not phone.isdigit() or len(phone) != 10:
        return jsonify({
            "success": False,
            "message": "Enter a valid 10-digit mobile number."
        }), 400

    if not address:
        return jsonify({
            "success": False,
            "message": "Address is required."
        }), 400

    if not pincode.isdigit() or len(pincode) != 6:
        return jsonify({
            "success": False,
            "message": "Enter a valid pincode."
        }), 400

    if not items:
        return jsonify({
            "success": False,
            "message": "Cart is empty."
        }), 400

    try:
        total = float(total)
    except:
        return jsonify({
            "success": False,
            "message": "Invalid order total."
        }), 400

    connection = get_db()

    cursor = connection.execute("""
        INSERT INTO orders (
            customer_name,
            phone,
            address,
            pincode,
            items,
            total,
            payment_status,
            order_status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        customer_name,
        phone,
        address,
        pincode,
        str(items),
        total,
        "Pending",
        "New",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    order_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "order_id": order_id,
        "message": "Order created successfully."
    })


# =========================
# GET ORDERS
# =========================

@app.route("/api/orders", methods=["GET"])
def get_orders():

    if not session.get("admin_logged_in"):
        return jsonify({
            "success": False,
            "message": "Admin login required."
        }), 401

    connection = get_db()

    rows = connection.execute("""
        SELECT
            id,
            customer_name,
            phone,
            address,
            pincode,
            items,
            total,
            payment_status,
            order_status,
            created_at
        FROM orders
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    orders = []

    for row in rows:

        orders.append({
            "id": row["id"],
            "customer_name": row["customer_name"],
            "phone": row["phone"],
            "address": row["address"],
            "pincode": row["pincode"],
            "items": row["items"],
            "total": row["total"],
            "payment_status": row["payment_status"],
            "order_status": row["order_status"],
            "created_at": row["created_at"]
        })

    return jsonify({
        "success": True,
        "orders": orders
    })


# =========================
# STATIC FILES
# =========================

@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(BASE_DIR, filename)


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    create_database()

    print("=" * 50)
    print("SREE VENKATESWARA ORGANICS")
    print("=" * 50)
    print("Website: http://127.0.0.1:5000")
    print("Admin:   http://127.0.0.1:5000/admin")
    print("=" * 50)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )