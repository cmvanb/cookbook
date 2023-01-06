#-------------------------------------------------------------------------------
# Authentication Views
#-------------------------------------------------------------------------------

import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from email_validator import validate_email, EmailNotValidError

from cookbook.db import get_db

# Authentication Blueprint
#-------------------------------------------------------------------------------
blueprint = Blueprint(
    'auth', __name__, 
    url_prefix='/auth', 
    static_folder='static', 
    template_folder='templates',
)

# Validation logic.
#-------------------------------------------------------------------------------
def validate_registration(email, display_name, password):
    if not email:
        return 'Email is required.'
    if not display_name:
        return 'Display name is required.'
    if not password:
        return 'Password is required.'

    # Validate email address.
    try:
        validation = validate_email(email, check_deliverability=True)
        email = validation.email
    except EmailNotValidError as e:
        return str(e)

    return None

# Registration view.
#-------------------------------------------------------------------------------
@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email        = request.form['email']
        display_name = request.form['display_name']
        password     = request.form['password']

        error = validate_registration(email, display_name, password)

        if error is not None:
            flash(error)
            return render_template('register.html')

        # Insert new user.
        db = get_db()
        try:
            db.execute(
                'INSERT INTO user (email, display_name, password) VALUES (?, ?, ?)',
                (email, display_name, generate_password_hash(password)),
                )
            db.commit()
        except db.IntegrityError:
            error = f'Email address `{email}` is already registered to an account.'
        else:
            return redirect(url_for('.login'))

        flash(error)

    # On GETs we simply render.
    return render_template('register.html')

# Login view.
#-------------------------------------------------------------------------------
@blueprint.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']

        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
            ).fetchone()

        error = None
        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('recipes.index'))

        flash(error)

    elif g.user is not None:
        return redirect(url_for('recipes.index'))

    return render_template('login.html')

# Logout view.
#-------------------------------------------------------------------------------
@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Runs before each view request, to retrieve logged in user.
#-------------------------------------------------------------------------------
@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
            ).fetchone()

