import falcon
from cerberus import Validator


def validate_user_create(req, res, resource, params):
    schema = {
        'email': {
            'type': 'string',
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'required': True
        },
        'password': {
            'type': 'string',
            'minlength': 8,
            'required': True
        }
    }

    v = Validator(schema)
    if not v.validate(req.context['data']):
        raise falcon.HTTPBadRequest('Bad request', v.errors)


def validate_user_auth(req, res, resource, params):
    schema = {
        'email': {
            'type': 'string',
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'required': True
        },
        'password': {
            'type': 'string',
            'required': True
        }
    }

    v = Validator(schema)
    if not v.validate(req.context['data']):
        raise falcon.HTTPBadRequest('Bad request', v.errors)
