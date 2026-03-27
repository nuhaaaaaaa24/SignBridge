from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}

# ── Page Routes ───────────────────────────────────────────────────────────────

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
def call():
    return render_template("call.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# ── SocketIO Events ───────────────────────────────────────────────────────────

@socketio.on("join")
def on_join(data):
    room = data["room"]
    join_room(room)

    if room not in rooms:
        rooms[room] = 0

    rooms[room] += 1

    # Assign roles
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
