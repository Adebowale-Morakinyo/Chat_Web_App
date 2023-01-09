from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socket = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    return render_template('client.html')


@socket.on('connect')
def connect():
    """Handles client's connection."""
    print("[CLIENT CONNECTED]:", request.sid)


@socket.on('disconnect')
def disconn():
    """Handles client's disconnection."""
    print("[CLIENT DISCONNECTED]:", request.sid)


@socket.on('notify')
def notify(user):
    """Broadcasts a notification msg (join or left) to all the clients."""
    emit('notify', user, broadcast=True, skip_sid=request.sid)


@socket.on('data')
def emitback(data):
    """Broadcasts a message to all the clients."""
    emit('returndata', data, broadcast=True)


if __name__ == "__main__":
    socket.run(app, debug=True, allow_unsafe_werkzeug=True)
