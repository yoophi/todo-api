from urllib.parse import urlparse

from flask import Blueprint, current_app, jsonify, request, url_for
from flask_swagger import swagger, _parse_docstring, _sanitize

from app.__meta__ import __api_name__, __version__

swagger_bp = Blueprint('swagger', __name__)

_swagger_definition = {}


@swagger_bp.route('/spec')
def spec():
    swag = swagger(current_app)

    swag['info']['title'] = __api_name__
    swag['info']['version'] = __version__
    swag['host'] = request.host
    swag['basePath'] = url_for('main.index', ).rstrip('/')
    swag["definitions"] = _swagger_definition

    o = urlparse(url_for('main.index', _external=True))

    swag['schemes'] = [o.scheme, ]

    return jsonify(swag)


def swagger_definition(class_):
    name, _, adict = _parse_docstring(class_, _sanitize, None)
    _swagger_definition[name] = adict

    return class_


from app.schema import *  # noqa
