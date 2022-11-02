import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from cookbook.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Registration route.
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        display_name = request.form['display_name']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not display_name:
            error = 'Display name is required.'
        elif not password:
            error = 'Password is required.'

        # TODO: Validate email adrress.

        if error is None:
            try:
                db.execute(
                    'INSERT INTO user (email, display_name, password) VALUES (?, ?, ?)',
                    (email, display_name, generate_password_hash(password)),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"Email address `{email}` is already registered to an account."
            else:
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

# Login route.
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
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

    return render_template('auth/login.html')

# Logout route.
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Runs before each view request, to retrieve logged in user.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
            ).fetchone()

# Decorator function to require authentication for a view.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

