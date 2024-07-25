#-------------------------------------------------------------------------------
# Authentication storage layer
#-------------------------------------------------------------------------------

from werkzeug.security import generate_password_hash

from cookbook.db import get_db


def add_user(email, display_name, password):
    """ Add new user to the database; store a hashed password. """

    db = get_db()
    cursor = db.cursor()

    hashed_password = generate_password_hash(password)

    sql = """
        INSERT INTO user (email, display_name, password)
        VALUES (?, ?, ?)
    """
    args = (email, display_name, hashed_password)

    try:
        cursor.execute(sql, args)
        db.commit()
    except db.IntegrityError:
        return f'Email address `{email}` is already registered to an account.'

    return None


def get_user_by_id(id):
    """ Get user by ID. """

    db = get_db()
    cursor = db.cursor()

    sql = """
        SELECT * FROM user WHERE id = ?
    """
    args = (id, )

    return cursor.execute(sql, args).fetchone()


def get_user_by_email(email):
    """ Get user by email. """

    db = get_db()
    cursor = db.cursor()

    sql = """
        SELECT * FROM user WHERE email = ?
    """
    args = (email, )

    return cursor.execute(sql, args).fetchone()
