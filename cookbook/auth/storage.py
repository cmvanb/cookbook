#-------------------------------------------------------------------------------
# Authentication storage layer
#-------------------------------------------------------------------------------

from werkzeug.security import generate_password_hash

from cookbook.db import get_db

# Add new user
#-------------------------------------------------------------------------------
def add_user(email, display_name, password):
    db = get_db()

    hashed_password = generate_password_hash(password)

    sql = """
        INSERT INTO user (email, display_name, password)
        VALUES (?, ?, ?)
    """
    args = (email, display_name, hashed_password)

    try:
        db.execute(sql, args)
        db.commit()
    except db.IntegrityError:
        return f'Email address `{email}` is already registered to an account.'

    return None

# Get user by id
#-------------------------------------------------------------------------------
def get_user_by_id(id):
    db = get_db()

    sql = """
        SELECT * FROM user WHERE id = ?
    """
    args = (id, )

    return db.execute(sql, args).fetchone()

# Get user by email
#-------------------------------------------------------------------------------
def get_user_by_email(email):
    db = get_db()

    sql = """
        SELECT * FROM user WHERE email = ?
    """
    args = (email, )

    return db.execute(sql, args).fetchone()
