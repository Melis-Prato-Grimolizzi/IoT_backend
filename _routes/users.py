from flask import Blueprint
from _utils import user

users = Blueprint('users', __name__, url_prefix="/users")


"""
Route usate per gestire gli utenti.
"""

@users.route("/login", methods=["POST"])
def login():
    """
    Route per il login.
    """
    return "login"
