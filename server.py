from myapp import create_app
from myapp.database import db, Message
from flask_socketio import emit, join_room, leave_room

app, socket = create_app()


# COMMUNICATION ARCHITECTURE

# Join-chat event. Emit online message to other users and join the room
@socket.on("join-chat")
def join_private_chat(data):
    room = data["rid"]
    join_room(room=room)
    socket.emit(
        "joined-chat",
        {"msg": f"{room} is now online."},
        room=room,
        # include_self=False,
    )


# Outgoing event handler
@socket.on("outgoing")
def chatting_event(json, methods=["GET", "POST"]):
    """
    handles saving messages and sending messages to all clients
    :param json: json
    :param methods: POST GET
    :return: None
    """
    room_id = json["rid"]
    timestamp = json["timestamp"]
    message = json["message"]
    sender_id = json["sender_id"]
    sender_username = json["sender_username"]

    # Get the message entry for the chat room
    chat_message = Message.query.filter_by(room_id=room_id).first()

    # Add the new message to the conversation
    updated_message = chat_message.conversation + [{
        "timestamp": timestamp,
        "sender_username": sender_username,
        "sender_id": sender_id,
        "message": message,
    }]
    chat_message.conversation = updated_message

    # Updated the database with the new message
    try:
        chat_message.save_to_db()
    except Exception as e:
        # Handle the database error, e.g., log the error or send an error response to the client.
        print(f"Error saving message to the database: {str(e)}")
        db.session.rollback()

    # Emit the message(s) sent to other users in the room
    socket.emit(
        "message",
        json,
        room=room_id,
        include_self=False,
    )


if __name__ == "__main__":
    socket.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True, debug=True)
