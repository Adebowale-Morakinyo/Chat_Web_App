from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from views import views
from test import database

app = Flask(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
app.register_blueprint(views, url_prefix='')
CORS(app)
socket = SocketIO(app, cors_allowed_origins="*")


# COMMUNICATION ARCHITECTURE

@socket.on('connect')
def connect():
    print("[CLIENT CONNECTED]:", request.sid)


@socket.on('disconnect')
def disconn():
    print("[CLIENT DISCONNECTED]:", request.sid)


@socket.on('event')
def custom_event(json, methods=['GET', 'POST']):
    """
    handles saving messages and sending message to other clients
    :param json: json
    :param methods: POST GET
    :return: None
    """
    data = dict(json)
    if 'name' in data:
        database.append({'name': data['name'],
                         'message': data['message'],
                         'time': data['date']})

    socket.emit('message response', json)


if __name__ == "__main__":
    socket.run(app, allow_unsafe_werkzeug=True, debug=True)
