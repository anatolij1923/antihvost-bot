# Simple in-memory storage for authorized users
authorized_users = {}  # Dictionary to store user_id -> fullname mapping

def add_authorized_user(user_id, fullname):
    """Add a user to the authorized users list with their fullname"""
    authorized_users[user_id] = fullname

def get_authorized_user_name(user_id):
    """Get the fullname of an authorized user"""
    return authorized_users.get(user_id, "Неизвестный пользователь")