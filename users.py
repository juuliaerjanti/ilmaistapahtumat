"""
users.py: Functions for managing user-related operations in the application.

Each function interacts with the database and returns relevant data or performs
necessary operations.
"""


from werkzeug.security import generate_password_hash, check_password_hash
import db

def get_user(user_id):
    """
    Retrieves a user by their ID.

    Args:
        user_id (int): ID of the user.

    Returns:
        dict or None: User details if found, otherwise None.
    """

    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_events(user_id):
    """
    Retrieves events created by a specific user.

    Args:
        user_id (int): ID of the user.

    Returns:
        list[sqlite3.Row]: List of events created by the user.
    """

    sql = "SELECT id, title, date FROM events WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])

def create_user(username, password1):
    """
    Creates a new user with a hashed password.

    Args:
        username (str): Username of the new user.
        password1 (str): Plaintext password to be hashed.
    """

    password_hash = generate_password_hash(password1)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    """
    Validates user login credentials.

    Args:
        username (str): Username provided by the user.
        password (str): Plaintext password provided by the user.

    Returns:
        int or None: User ID if credentials are valid, otherwise None.
    """

    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id =  result[0]["id"]
    password_hash =  result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None

def get_user_comments(user_id):
    """
    Retrieves comments made by a specific user.

    Args:
        user_id (int): ID of the user.

    Returns:
        list[sqlite3.Row]: List of comments made by the user, including event titles and timestamps.
    """

    sql = """SELECT comments.comment, events.title, comments.created_at
             FROM comments
             JOIN events ON comments.event_id = events.id
             WHERE comments.user_id = ?
             ORDER BY comments.created_at DESC"""
    return db.query(sql, [user_id])
