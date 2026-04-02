from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room
from flask_limiter import Limiter # For rate limiting to prevent unwanted traffic and abuse
from flask_limiter.util import get_remote_address # to determine the client's IP address for rate limiting
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
    default_limits=["200 per minute"] ,
    storage_uri="memory://", # In-memory storage for rate limiting.
)

rooms = {}

# ── Database Setup ────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Rooms table
    c.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_code TEXT UNIQUE NOT NULL,
            owner_username TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Room participants table
    c.execute("""
        CREATE TABLE IF NOT EXISTS room_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_code TEXT NOT NULL,
            username TEXT NOT NULL,
            joined_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized with users, rooms, and room_participants tables.")

init_db()

# ── Helper ──
def generate_room_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# ── Registration ──
@app.route("/register", methods=["POST"])
@limiter.limit("5 per minute") # Limit registration attempts to prevent brute-force attacks
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    hashed_password = generate_password_hash(password)

    try:
        with sqlite3.connect("users.db") as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, email, password, created_at) VALUES (?, ?, ?, ?)",
                (username, email, hashed_password, datetime.now().isoformat())
            )
            conn.commit()
        return jsonify({"success": True, "message": "User registered successfully"})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Username or email already exists"}), 400

# ── Login ──
@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute") # Limit login attempts to prevent brute-force attacks
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[1], password):
        session["user_id"] = user[0]
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

# ── Create Room ──
@app.route("/create-room", methods=["POST"])
@limiter.limit("5 per minute") # Limit room creation attempts to prevent brute-force attacks
def create_room():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"success": False, "message": "Username is required"}), 400

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    # Generate unique room code
    while True:
        room_code = generate_room_code()
        c.execute("SELECT id FROM rooms WHERE room_code = ?", (room_code,))
        if not c.fetchone():
            break

    created_at = datetime.now().isoformat()
    c.execute("INSERT INTO rooms (room_code, owner_username, created_at) VALUES (?, ?, ?)",
              (room_code, username, created_at))
    # Add owner as first participant
    c.execute("INSERT INTO room_participants (room_code, username, joined_at) VALUES (?, ?, ?)",
              (room_code, username, created_at))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "room_code": room_code, "message": "Room created!"})

# ── Join Room ──
@app.route("/join-room", methods=["POST"])
@limiter.limit("10 per minute") # Limit join room attempts to prevent brute-force attacks
def join_room_route():
    data = request.get_json()
    username = data.get("username")
    room_code = data.get("room_code")

    if not username or not room_code:
        return jsonify({"success": False, "message": "Username and room code are required"}), 400

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT id FROM rooms WHERE room_code = ?", (room_code,))
    room = c.fetchone()
    if not room:
        conn.close()
        return jsonify({"success": False, "message": "Room does not exist"}), 404

    # Add participant
    joined_at = datetime.now().isoformat()
    try:
        c.execute("INSERT INTO room_participants (room_code, username, joined_at) VALUES (?, ?, ?)",
                  (room_code, username, joined_at))
        conn.commit()
        return jsonify({"success": True, "message": f"{username} joined room {room_code}"})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "User already in room"}), 400
    finally:
        conn.close()

# ── Page Routes ──
@app.route("/")
@app.route("/landing")
def landing():
    return render_template("landing.html")

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
    return render_template("waiting.html")

@app.route("/call")
@limiter.limit("10 per minute") # Limit access to call page to prevent abuse
def call():
    return render_template("call.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(429)
def ratelimit_exceeded(e):
    return "Too many requests. Please slow down.", 429

# ── SocketIO Events ──
@socketio.on("join")
def on_join(data):
    room = data["room"]
    join_room(room)

    if room not in rooms:
        rooms[room] = 0
    rooms[room] += 1

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