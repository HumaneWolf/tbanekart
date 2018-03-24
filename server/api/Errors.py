from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from flask import json

from api.Api import api


@api.errorhandler(BadRequest)
def handle_bad_request(e):
    return json.jsonify(
        error=True,
        response='bad request'
    )


@api.errorhandler(NotFound)
def handle_bad_request(e):
    return json.jsonify(
        error=True,
        response='Not found'
    )


@api.errorhandler(InternalServerError)
def handle_bad_request(e):
    return json.jsonify(
        error=True,
        response='Server Error'
    )