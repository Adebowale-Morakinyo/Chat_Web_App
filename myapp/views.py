from flask import Blueprint, render_template, request, url_for, redirect, session, flash, jsonify
from myapp.database import db, Message

import pandas as pd
import matplotlib.pyplot as plt
from myapp import socket

views = Blueprint('views', __name__, static_folder='static', template_folder='templates')


@views.route('/')
@views.route('/home')
def home():
    """
    displays chat(home) window page, if logged in
    :return: None
    """

    if 'username' not in session:
        return redirect(url_for('views.login'))

    return render_template('home.html', **{'session': session})


@views.route('/chat')
def chat():
    return render_template('index.html', **{'session': session})


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


@views.route('/login', methods=['GET', 'POST'])
def login():
    """
    displays login and (redirect chat) window page,
    and handles saving name in session
    :return: None
    """
    if request.method == 'POST':
        username = request.form['username']
        if len(username) >= 2:
            session['username'] = username
            flash(f'You logged in as {username}.', category='success')
            return redirect(url_for('views.home'))
        flash('Username must be more than one character!', category='danger')

    return render_template('login.html', **{'session': session})


@views.route('/logout')
def logout():
    """
    remove the username from the session if it's there
    :return: None
    """
    session.pop('username', None)
    flash('You logged out!', category='danger')
    return redirect(url_for('views.login'))


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
    checking and cleaning duplicates because of in-memory list used
    :return: all messages
    """
    messages = db.session.query(Message).all()

    cleaned = set()
    clean_messages = []
    for message in messages:
        if message not in cleaned:
            cleaned.add(message)
            clean_messages.append(message.to_dict())

    return jsonify(clean_messages)


@views.route('/leave')
def leave():
    socket.emit('disconnect')
    return redirect(url_for('views.home'))
