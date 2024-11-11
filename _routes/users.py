from flask import Blueprint, jsonify, request, Response
from _utils import models, decorators, user

users = Blueprint('users', __name__, url_prefix="/users")


"""
Route usate per gestire gli utenti.
"""

@users.route("/", methods=["GET"])
def get_users():
    """
    Route per ottenere tutti gli utenti.
    """
    result = user.get_all()
    return jsonify([u.serialize() for u in result])

@users.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    """
    Route per ottenere un singolo utente.
    """
    result = user.get(user_id)
    return jsonify(result.serialize())

@users.route("/verify", methods=['GET'])
@decorators.auth_decorator
def get_logged_in_status(user_id):
    return {"id": user_id}

@users.route("/signup", methods=['POST'])
@decorators.FormValidatorDecorator(
    required_fields=["username", "password"],
    validators=[models.User.validate_username, models.User.validate_password])
def signup():
    try:
        user.signup(request.form['username'], request.form['password'])
        return Response("OK", status=201)
    except user.DuplicateUserError:
        return Response("username conflict", status=409)

@users.route("/login", methods=['POST'])
@decorators.FormValidatorDecorator(
    required_fields=["username", "password"],
    validators=[models.User.validate_username, models.User.validate_password])
def login():
    try:
        return user.login(request.form['username'], request.form['password'])
    except user.BadCredentialsError:
        return Response("bad credentials", status=401)