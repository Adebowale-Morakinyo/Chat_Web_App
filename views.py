from flask import Blueprint, render_template, request, url_for, redirect, session, flash, jsonify
from test import database

views = Blueprint('views', __name__, static_folder='static', template_folder='templates')


@views.route('/')
@views.route('/home')
def index():
    """
    displays chat(home) window page, if logged in
    :return: None
    """

    if 'username' not in session:
        return redirect(url_for('views.login'))

    return render_template('index.html', **{'session': session})


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
            return redirect(url_for('views.index'))
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

    messages = database

    cleaned = set()
    clean_messages = []
    for d in messages:
        t = tuple(d.items())
        if t not in cleaned:
            cleaned.add(t)
            clean_messages.append(d)

    return jsonify(clean_messages)
