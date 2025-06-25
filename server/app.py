import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

@app.route("/")
def index():
    return "Flask server is running"

@socketio.on("connect")
def handle_connect():
    print("New client connected!")

@socketio.on("progress")
def handle_progress(data):
    print("Progress from client:", data)
    socketio.emit("progress_update", data)

if __name__ == "__main__":
    socketio.run(app, debug=True)
