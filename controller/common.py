from flask import request
from flask_login import current_user
from typing import Optional, Any

from flask import request, jsonify
from functools import wraps
from typing import Callable
from app import login_manager
from common.exceptions import (
    ResourceConflictError,
    ResourceNotFound,
    AuthenticationError,
)
from flask_login import current_user


@login_manager.user_loader
def load_user(user_id):  # type: ignore
    from models.user import User

    return User.get_user(user_id)


def login_required(function: Callable):  # type: ignore
    @wraps(function)
    def wrapped(*args, **kwargs):  # type: ignore
        if not current_user.is_authenticated:
            return login_manager.unauthorized(), 401
        return function(*args, **kwargs)

    return wrapped


def admin_login_required(function: Callable) -> Callable:  # type: ignore
    @wraps(function)
    def wrapped(*args, **kwargs):  # type: ignore
        if current_user.is_anonymous or not current_user.is_admin():
            return jsonify(error="Admin login required"), 403
        return function(*args, **kwargs)

    return wrapped


def _get_user_id_from_request() -> Any:
    if request.method == "GET":
        return request.args.get("user_id", None)

    return request.json.get("user_id", None)


def get_current_user(user_id: Optional[int] = None) -> Any:
    """
    if we have a user_id in the signature - use that
    if se have a user_id in the request - use that
    if user is admin, get the user_id we want

    and if user is not admin, return current_user
    """
    from models.user import User

    if not user_id:
        user_id = _get_user_id_from_request()

    if user_id and current_user.is_admin():
        return User.get_user(user_id)
    elif current_user:
        return User.get_user(current_user.id)

    return None
