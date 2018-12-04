from flask import redirect, render_template, request, url_for

from main.app import APP, session
from main.security import authentication


# ERROR HANDLERS
@APP.errorhandler(404)
def not_found(error=None):
    return '{} - 404 - Not found'.format(request.url)


# VIEWS
@APP.route('/')
@APP.route('/index')
def index():
    return render_template('index.html')


@APP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            auth, reason = authentication.authenticate(username, password)
            if auth:
                # Add username to session
                session['username'] = username
            return 'Success: {}\nReason: {}'.format(auth, reason)
    return render_template('login.html')


@APP.route('/logout', methods=['GET'])
def logout():
    # Release the username from the session
    username = session.get('username')
    if username:
        session.pop('username', None)
    return redirect(url_for('login'))

