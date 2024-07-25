#-------------------------------------------------------------------------------
# Authentication validation layer
#-------------------------------------------------------------------------------

from email_validator import validate_email, EmailNotValidError
from werkzeug.security import check_password_hash


def validate_registration(email, display_name, password):
    """ Validate user registration. """

    if not email:
        return 'Email is required.'
    if not display_name:
        return 'Display name is required.'
    if not password:
        return 'Password is required.'

    # Validate email address.
    try:
        v = validate_email(email, check_deliverability=True)
        email = v.email
    except EmailNotValidError as e:
        return str(e)

    return None


def validate_login(user, password):
    """ Validate user login. """

    if user is None:
        return 'Invalid email.'
    if not check_password_hash(user['password'], password):
        return 'Invalid password.'

    return None
