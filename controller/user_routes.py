from flask import request, jsonify
from typing import Tuple
import marshmallow
from werkzeug import Response
from app import app
from common.exceptions import (
    ResourceConflictError,
    ResourceNotFound,
    AuthenticationError,
)
from services.user_service import create_user, get_user
from serializers.user_serializers import login_schema
from flask_login import login_user, logout_user
from controller.common import login_required


@app.route("/login", methods=["POST"])
def login() -> Tuple[Response, int]:
    """
    login a user with email and password
    """
    try:
        schema = login_schema.load(request.json)
        user = get_user(email=schema["email"], password=schema["password"])
        login_user(user)
    except marshmallow.exceptions.ValidationError as error:
        return jsonify(error=error.messages), 400
    except ResourceNotFound as error:
        return jsonify(error=error.message), 404
    except AuthenticationError as error:
        return jsonify(error=error.message), 403

    return jsonify("successfully logged in user"), 200


@app.route("/register", methods=["POST"])
def register() -> Tuple[Response, int]:
    """
    register a user with an email and a password
    """
    try:
        schema = login_schema.load(request.json)
        user = create_user(email=schema["email"], password=schema["password"])
        login_user(user)
    except marshmallow.exceptions.ValidationError as error:
        return jsonify(error=error.messages), 400
    except ResourceConflictError as error:
        return jsonify(error=error.message), 409

    return jsonify("user registered successfully"), 200


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout() -> Tuple[Response, int]:
    """
    logout a user
    """
    logout_user()
    return jsonify("logged out user successfully"), 200
