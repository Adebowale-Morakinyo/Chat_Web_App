from myapp import create_app
from myapp.database import db, Message
from flask import request

app, socket = create_app()


# COMMUNICATION ARCHITECTURE
@socket.on('disconnect')
def handle_disconnect():
    """
    handles disconnection event
    :return: None
    """
    print(f'{request.sid} disconnected')
    socket.emit('disconnect', {'sid': request.sid}, broadcast=True)


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
        message = Message(name=data['name'], message=data['message'], time=data['date'])
        db.session.add(message)
        db.session.commit()

    socket.emit('message response', json, broadcast=True)


if __name__ == "__main__":
    socket.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True, debug=True)
