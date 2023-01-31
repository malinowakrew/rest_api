from flask import Blueprint
from flask import send_from_directory

bp_swagger = Blueprint('ticket', __name__, url_prefix='/ticket')


@bp_swagger.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)
