from flask import jsonify, request, Blueprint, make_response
import json
from flask_json_schema import JsonValidationError

from db import Status, Severity, Ticket, db
from schema import schema, template_request, template_request_delete
from core.error import RecordNotExist

bp = Blueprint('ticket', __name__, url_prefix='/ticket')


@bp.route('/', methods=['GET'])
def read_tickets():
    tickets = [ticket.json() for ticket in Ticket.query.all()]
    return jsonify(tickets)


@bp.route('/addition', methods=['POST'])
@schema.validate(template_request)
def add_ticket():
    request_data = request.get_json()
    severity_name = request_data.get("severity", "low")
    dict_to_add = {
            "title": request_data.get("title", None),
            "description": request_data.get("description", "None"),
            "severity": Severity[severity_name],
            "status": Status.new
        }

    db.session.add(Ticket(**dict_to_add))
    db.session.commit()
    return json.dumps(dict_to_add, default=lambda x: x.value)


@bp.route('/deleting', methods=['DELETE'])
@schema.validate(template_request_delete)
def delete_tickets():
    request_data = request.get_json()
    ticket = Ticket.query.filter_by(ticket_id=request_data.get("ticket_id", "None")).first()
    if ticket is None:
        raise RecordNotExist
    dict_ticket = ticket.json()
    db.session.delete(ticket)
    return jsonify(dict_ticket)


@bp.route('/<string:field>/change', methods=['POST'])
def change_tickets(field):
    request_data = request.get_json()
    try:
        if field == 'status':
            number_of_changed_tickets = Ticket.query.filter_by(ticket_id=request_data.get("ticket_id", None)).update(
                {field: Status[request_data.get('value', None)]})
        if field == 'severity':
            number_of_changed_tickets = Ticket.query.filter_by(ticket_id=request_data.get("ticket_id", None)).update(
                {field: Severity[request_data.get('value', None)]})
        if field == 'ticket_id':
            raise ValueError
        else:
            number_of_changed_tickets = Ticket.query.filter_by(ticket_id=request_data.get("ticket_id", None)).update(
                {field: request_data.get('value', None)})
    except Exception:
        raise RecordNotExist

    changed_ticket = Ticket.query.filter_by(ticket_id=request_data.get("ticket_id", None)).first()
    return jsonify(changed_ticket.json())


@bp.errorhandler(JsonValidationError)
def validation_error(error):
    return jsonify({"error-type": "Bad Request",
                    'text': error.message}), 400


@bp.errorhandler(RecordNotExist)
def record_error(error):
    return jsonify({"warning": error.message}), 200


@bp.errorhandler(Exception)
def validation_error(error):
    return jsonify({"error-type": error}), 404

