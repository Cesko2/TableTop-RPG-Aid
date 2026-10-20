import bcrypt

from database_interface import get_user_by_username

def authenticate_user(username, password):
    user = get_user_by_username(username)

    # Checks to see if queried user exists
    if user is None:
        return {
            "success": False,
            "message": "Invalid username or password."
        }

    # Validates password
    password_is_valid = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password_hash"].encode("utf-8")
    )

    # Return unsuccessfully
    if not password_is_valid:
        return {
            "success": False,
            "message": "Invalid username or password."
        }

    # Return successfully
    return {
        "success": True,
        "message": "Authentication successful.",
        "user_id": user["user_id"],
        "username": user["username"]
    }

def create_user(username, password):
    #TODO: Define this function later
    pass
