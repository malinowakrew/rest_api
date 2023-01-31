from flask_json_schema import JsonSchema
schema = JsonSchema()

template_request = {
    'required': ["title", "description", "severity"],
    'properties': {
        'title': {'type': 'string'},
        'description': {'type': 'string'},
        'severity': {'type': 'string'}
    }
}

template_request_delete = {
    'required': ["ticket_id"],
    'properties': {
        'ticket_id': {'type': 'integer'}
    }
}

template_request_update = {
    'required': ["ticket_id", "value"],
    'properties': {
        'ticket_id': {'type': 'integer'},
        'value': {'type': 'string'}
    }
}