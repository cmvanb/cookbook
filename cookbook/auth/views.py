#-------------------------------------------------------------------------------
# Authentication Views
#-------------------------------------------------------------------------------

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from cookbook.auth import storage, validation


blueprint = Blueprint(
    'auth', __name__,
    url_prefix='/auth',
    static_folder='static',
    template_folder='templates',
)


@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    """ Registration view. """

    def post():
        """ POST validates user form data and adds the user to the database. """

        email        = request.form['email']
        display_name = request.form['display_name']
        password     = request.form['password']

        error = validation.validate_registration(email, display_name, password)

        if error is not None:
            return error

        error = storage.add_user(email, display_name, password)

        if error is not None:
            return error

        return None

    status = 200

    if request.method == 'POST':
        error = post()

        if error is None:
            return redirect(url_for('.login'))
        else:
            flash(error)
            status = 400

    return render_template('register.html'), status


@blueprint.route('/login', methods=('GET', 'POST'))
def login():
    """ Login view. """

    def post():
        """ POST validates the user login details and returns the user object. """

        email    = request.form['email']
        password = request.form['password']

        user = storage.get_user_by_email(email)
        error = validation.validate_login(user, password)

        return user, error

    status = 200

    if request.method == 'POST':
        user, error = post()

        if error is None:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('recipes.index'))
        else:
            flash(error)
            status = 400

    elif g.user is not None:
        return redirect(url_for('recipes.index'))

    return render_template('login.html'), status


@blueprint.route('/logout')
def logout():
    """ Logout view. """

    session.clear()

    return redirect(url_for('.login'))


@blueprint.before_app_request
def load_logged_in_user():
    """ Run this decorator before each view request, to retrieve logged in user. """

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = storage.get_user_by_id(user_id)
