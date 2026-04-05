from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import string

app = Flask(__name__)
app.secret_key = "supersecretkey"
socketio = SocketIO(app, cors_allowed_origins="*")

# Rate limiter setup
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per minute"],
    storage_uri="memory://",
)

rooms = {}

# ── Database Setup ──
def init_db():
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_code TEXT UNIQUE NOT NULL,
                owner_username TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS room_participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_code TEXT NOT NULL,
                username TEXT NOT NULL,
                joined_at TEXT NOT NULL
            )
        """)
    print("Database initialized.")

init_db()

# ── Helpers ──
def generate_room_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def validate_password(password):
    """Validate password meets all requirements"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        return False, "Password must contain at least one special character"
    return True, "Password is valid"

# ── Routes ──
@app.route("/")
def landing():
    return render_template("login.html")

@app.route("/landing")
def createRoom():
    return render_template("landing.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/waiting")
def waiting():
    name = request.args.get("name", "Guest")
    room = request.args.get("room", "N/A")
    return render_template("waiting.html", name=name, room=room)

@app.route("/call")
@limiter.limit("10 per minute")
def call():
    return render_template("call.html")

@app.route("/slslchart")
def slslchart():
    return render_template("slslchart.html")

@app.route("/video_tutorial")
def video_tutorial():
    return render_template("video-tutorial.html")

@app.route("/user_guide")
def user_guide():
    return render_template("user_guide.html")

@app.route("/error")
def error():
    return render_template("error.html")

# ── Register ──
@app.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()
    username, email, password = data.get("username"), data.get("email"), data.get("password")

    if not username or not email or not password:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    # Validate password requirements
    is_valid, message = validate_password(password)
    if not is_valid:
        return jsonify({"success": False, "message": message}), 400

    # Check if the user entered a username that already exists in the application
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username = ?", (username,))
        if c.fetchone():
            return jsonify({"success": False, "message": f"'{username}' is already exists in the application. Please enter a different username."}), 400
        
        # Check if the user entered an email that already exists in the application (when registering).
        c.execute("SELECT email FROM users WHERE email = ?", (email,))
        if c.fetchone():
            return jsonify({"success": False, "message": "This email is already registered. Please use a different email."}), 400

    hashed = generate_password_hash(password)

    try:
        with sqlite3.connect("users.db") as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, email, password, created_at) VALUES (?, ?, ?, ?)",
                (username, email, hashed, datetime.now().isoformat())
            )
        return jsonify({"success": True, "message": "Registered successfully"})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Registration failed. Please try again."}), 400

# ── Login ──
@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    username, password = data.get("username"), data.get("password")

    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = c.fetchone()

    if user and check_password_hash(user[1], password):
        session["user_id"] = user[0]
        return jsonify({"success": True, "message": "Login successful"})

    return jsonify({"success": False, "message": "Invalid username or password"}), 401

# ── Create Room ──
@app.route("/create-room", methods=["POST"])
@limiter.limit("5 per minute")
def create_room():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"success": False, "message": "Username required"}), 400

    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        while True:
            code = generate_room_code()
            c.execute("SELECT id FROM rooms WHERE room_code = ?", (code,))
            if not c.fetchone():
                break

        created_at = datetime.now().isoformat()
        c.execute("INSERT INTO rooms (room_code, owner_username, created_at) VALUES (?, ?, ?)",
                  (code, username, created_at))
        c.execute("INSERT INTO room_participants (room_code, username, joined_at) VALUES (?, ?, ?)",
                  (code, username, created_at))

    return jsonify({"success": True, "room_code": code})

# ── Join Room ──
@app.route("/join-room", methods=["POST"])
@limiter.limit("10 per minute")
def join_room_route():
    data = request.get_json()
    username, room_code = data.get("username"), data.get("room_code")

    if not username or not room_code:
        return jsonify({"success": False, "message": "Username and room code required"}), 400

    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM rooms WHERE room_code = ?", (room_code,))
        if not c.fetchone():
            return jsonify({"success": False, "message": "Room does not exist"}), 404

        c.execute("INSERT INTO room_participants (room_code, username, joined_at) VALUES (?, ?, ?)",
                  (room_code, username, datetime.now().isoformat()))

    return jsonify({"success": True, "message": f"{username} joined room {room_code}"})

# ── Errors ──
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(429)
def ratelimit_exceeded(e):
    return "Too many requests. Please slow down.", 429

# ── SocketIO ──
@socketio.on("join")
def on_join(data):
    room = data["room"]
    join_room(room)

    rooms[room] = rooms.get(room, 0) + 1

    if rooms[room] == 1:
        emit("role", {"role": "caller"})
    elif rooms[room] == 2:
        emit("role", {"role": "callee"})
        emit("ready", room=room)

@socketio.on("signal")
def handle_signal(data):
    emit("signal", data, room=data["room"], include_self=False)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)