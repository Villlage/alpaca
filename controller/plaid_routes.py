from flask import request
from controller.common import get_current_user, login_required
from serializers.plaid_serializers import plaid_request_schema, plaid_item_schema
from common.exceptions import ResourceConflictError
from app import app
from app import logger
from werkzeug import Response

from flask import request, jsonify
import marshmallow
from app import app
from common.exceptions import (
    ResourceConflictError,
    ResourceNotFound,
    AuthenticationError,
)
from controller.common import login_required
import plaid
from services.plaid_service import create_plaid_item
from typing import Tuple


@app.route("/plaid/items", methods=["POST"])
@login_required
def plaid_item_create() -> Tuple[Response, int]:
    user = get_current_user()

    try:
        request_data = plaid_request_schema.load(request.json)
        plaid_item = create_plaid_item(
            user=user,
            public_token=request_data["public_token"],
            metadata=request_data["metadata"],
        )
    except marshmallow.exceptions.ValidationError as error:
        return jsonify(error=error.messages), 400
    except ResourceConflictError:
        return (
            jsonify(error="User has linked a bank account with this institution"),
            422,
        )
    except plaid.errors.PlaidError as e:
        logger.error(
            "plaid error - request id: {} for user id:{}".format(e.request_id, user.id)
        )
        return jsonify(error=e.display_message or e.code), 500

    response = plaid_item_schema.dump(plaid_item)
    return jsonify(response), 200


@app.route("/plaid/items", methods=["GET"])
@login_required
def get_plaid_items() -> Tuple[Response, int]:
    user = get_current_user()
    response = plaid_item_schema.dump(user.plaid_items, many=True)

    return jsonify(response), 200
