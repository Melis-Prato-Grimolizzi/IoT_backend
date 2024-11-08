from flask import Blueprint
from _utils import user

user = Blueprint('users', __name__, url_prefix="/users")


"""
Route usate per gestire gli utenti.
"""

@user.route("/login", methods=["POST"])
def login():
    """
    Route per il login.
    """
    return user.login()
