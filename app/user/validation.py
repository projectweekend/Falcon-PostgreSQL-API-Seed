import falcon
from cerberus import Validator


FIELDS = {
    'email': {
        'type': 'string',
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        'required': True
    },
    'password_create': {
        'type': 'string',
        'required': True,
        'minlength': 8
    },
    'password': {
        'type': 'string',
        'required': True
    },
    'code': {
        'type': 'string',
        'required': True
    },
}


def validate_user_create(req, res, resource, params):
    schema = {
        'email': FIELDS['email'],
        'password': FIELDS['password_create']
    }

    v = Validator(schema)
    if not v.validate(req.context['data']):
        raise falcon.HTTPBadRequest('Bad request', v.errors)


def validate_user_auth(req, res, resource, params):
    schema = {
        'email': FIELDS['email'],
        'password': FIELDS['password']
    }

    v = Validator(schema)
    if not v.validate(req.context['data']):
        raise falcon.HTTPBadRequest('Bad request', v.errors)


def validate_request_password_reset(req, res, resource, params):
    schema = {
        'email': FIELDS['email']
    }

    v = Validator(schema)
    if not v.validate(req.context['data']):
        raise falcon.HTTPBadRequest('Bad request', v.errors)


def validate_confirm_password_reset(req, res, resource, params):
    schema = {
        'code': FIELDS['code'],
        'password': FIELDS['password_create']
    }

    v = Validator(schema)
    if not v.validate(req.context['data']):
        raise falcon.HTTPBadRequest('Bad request', v.errors)
