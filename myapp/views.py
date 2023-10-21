from flask import Blueprint, render_template, request, url_for, redirect, session, flash, jsonify
from myapp.database import *
from functools import wraps

import pandas as pd
import matplotlib.pyplot as plt
from myapp import socket

views = Blueprint('views', __name__, static_folder='static', template_folder='templates')


# Login decorator to ensure user is logged in before accessing certain routes
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("views.login"))
        return f(*args, **kwargs)

    return decorated


# Index route, this route redirects to login/register page
@views.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("views.login"))


# Register a new user and hash password
@views.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        username = request.form["username"].strip().lower()
        password = request.form["password"]

        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("User already exists with that username.")
            return redirect(url_for("views.login"))

        # Create a new user
        new_user = User(username=username, email=email, password=password)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # Create a new chat list for the newly registered user
        new_chat = Chat(user_id=new_user.id, chat_list=[])
        db.session.add(new_chat)
        db.session.commit()

        flash("Registration successful.")
        return redirect(url_for("views.login"))

    return render_template("auth.html")


@views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        # Query the database for the inputted email address
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Create a new session for the newly logged-in user
            session["user"] = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
            return redirect(url_for("views.chat"))
        else:
            flash("Invalid login credentials. Please try again.")
            return redirect(url_for("views.login"))

    return render_template("auth.html")


@views.route("/new-chat", methods=["POST"])
@login_required
def new_chat():
    user_id = session["user"]["id"]
    new_chat_email = request.form["email"].strip().lower()

    # If user is trying to add themselves, do nothing
    if new_chat_email == session["user"]["email"]:
        return redirect(url_for("views.chat"))

    # Check if the recipient user exists
    recipient_user = User.query.filter_by(email=new_chat_email).first()
    if not recipient_user:
        return redirect(url_for("views.chat"))

    # Check if the chat already exists
    existing_chat = Chat.query.filter_by(user_id=user_id).first()
    """if not existing_chat:
        existing_chat = Chat(user_id=user_id, chat_list=[])
        db.session.add(existing_chat)
        db.session.commit()"""

    # Check if the new chat is already in the chat list
    if recipient_user.id not in [user_chat["user_id"] for user_chat in existing_chat.chat_list]:
        # Generate a room_id (you may use your logic to generate it)
        room_id = str(int(recipient_user.id) + int(user_id))[-4:]

        # Add the new chat to the chat list of the current user
        updated_chat_list = existing_chat.chat_list + [{"user_id": recipient_user.id, "room_id": room_id}]
        existing_chat.chat_list = updated_chat_list

        # Save the changes to the database
        existing_chat.save_to_db()

        # Create a new chat list for the recipient user if it doesn't exist
        recipient_chat = Chat.query.filter_by(user_id=recipient_user.id).first()
        if not recipient_chat:
            recipient_chat = Chat(user_id=recipient_user.id, chat_list=[])
            db.session.add(recipient_chat)
            db.session.commit()

        # Add the new chat to the chat list of the recipient user
        updated_chat_list = recipient_chat.chat_list + [{"user_id": user_id, "room_id": room_id}]
        recipient_chat.chat_list = updated_chat_list
        recipient_chat.save_to_db()

        # Create a new message entry for the chat room
        new_message = Message(room_id=room_id, conversation=[])
        db.session.add(new_message)
        db.session.commit()

    return redirect(url_for("views.chat"))


@views.route("/chat/", methods=["GET", "POST"])
@login_required
def chat():
    # Get the room id in the URL or set to None
    room_id = request.args.get("rid", None)

    # Get the chat list for the user
    current_user_id = session["user"]["id"]
    current_user_chats = Chat.query.filter_by(user_id=current_user_id).first()
    chat_list = current_user_chats.chat_list if current_user_chats else []

    # Initialize context that contains information about the chat room
    data = []

    for chat in chat_list:
        # Query the database to get the username of users in a user's chat list
        username = User.query.get(chat["user_id"]).username
        is_active = room_id == chat["room_id"]

        try:
            # Get the last message for each chat room
            last_message = Message.query.filter_by(room_id=chat["room_id"]).first().conversation[-1]["message"]
        except (AttributeError, IndexError):
            # Set variable to this when no messages have been sent to the room
            last_message = "This place is empty. No messages ..."

        data.append({
            "username": username,
            "room_id": chat["room_id"],
            "is_active": is_active,
            "last_message": last_message,
        })

    # Get all the message history in a certain room
    messages = Message.query.filter_by(room_id=room_id).first().conversation if room_id else []

    return render_template(
        "chat.html",
        user_data=session["user"],
        room_id=room_id,
        data=data,
        messages=messages,
    )


# Custom time filter to be used in the jinja template
@views.app_template_filter("ftime")
def ftime(date):
    return datetime.fromtimestamp(int(date)).strftime("%m.%d. %H:%M")


@views.route('/visualize')
def visualize():
    # Query the database to get all the messages
    messages = Message.query.all()

    # Convert the messages to a pandas dataframe
    df = pd.DataFrame([(msg.name, msg.message, msg.time) for msg in messages],
                      columns=['Name', 'Message', 'Time'])

    # Group the messages by hour
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M')
    df['Hour'] = pd.to_datetime(df['Time']).dt.hour
    groupby_hour = df.groupby('Hour').count()['Name']

    # Create a bar chart of the messages by hour
    plt.bar(groupby_hour.index, groupby_hour.values)
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Messages')
    plt.title('Messages by Hour')

    # Convert the chart to base64 encoding to be displayed in the template
    from io import BytesIO
    import base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    # Render the template with the chart
    return render_template('visualize.html', chart=chart)


@views.route('/get_name')
def get_name():
    """
    :return: json object with username
    """
    data = {'name': ''}
    if 'username' in session:
        data = {'name': session['username']}

    return jsonify(data)


@views.route('/get_messages')
def get_messages():
    """
    query the database for messages o in a particular room id
    :return: all messages
    """
    pass


@views.route('/leave')
def leave():
    socket.emit('disconnect')
    return redirect(url_for('views.home'))
