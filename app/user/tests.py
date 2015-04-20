import falcon
from app import db
from app.utils.testing import APITestCase


USER_RESOURCE_ROUTE = '/v1/user'
USER_AUTH_ROUTE = '/v1/authenticate'
PASSWORD_RESET_REQUEST_ROUTE = '/v1/password-reset/request'
PASSWORD_RESET_CONFIRM_ROUTE = '/v1/password-reset/confirm'
AUTH_TEST_ROUTE = '/v1/test/auth'

VALID_DATA = {
    'email': 'abcd@efgh.com',
    'password': '12345678'
}

INVALID_DATA = {
    'MISSING_EMAIL': {
        'password': '12345678'
    },
    'BAD_EMAIL': {
        'email': 'not an email',
        'password': '12345678'
    },
    'MISSING_PASSWORD': {
        'email': 'abcd@efgh.com'
    },
    'BAD_PASSWORD': {
        'email': 'abcd@efgh.com',
        'password': 'short'
    },
    'NOT_REGISTERED': {
        'email': 'not@registered.com',
        'password': '11111111'
    }
}


class UserResourceTestCase(APITestCase):

    def test_create_a_user(self):
        body = self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        self.assertNotEqual(len(body['token']), 0)

    def test_create_a_dup_user(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_409)

    def test_invalid_create_a_user(self):
        self.simulate_post(USER_RESOURCE_ROUTE, INVALID_DATA['MISSING_EMAIL'])
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

        self.simulate_post(USER_RESOURCE_ROUTE, INVALID_DATA['BAD_EMAIL'])
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

        self.simulate_post(USER_RESOURCE_ROUTE, INVALID_DATA['MISSING_PASSWORD'])
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

        self.simulate_post(USER_RESOURCE_ROUTE, INVALID_DATA['BAD_PASSWORD'])
        self.assertEqual(self.srmock.status, falcon.HTTP_400)


class AuthenticationResourceTestCase(APITestCase):

    def test_successful_auth(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

        body = self.simulate_post(USER_AUTH_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertNotEqual(len(body['token']), 0)

    def test_invalid_auth_request(self):
        self.simulate_post(USER_AUTH_ROUTE, INVALID_DATA['MISSING_EMAIL'])
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

        self.simulate_post(USER_AUTH_ROUTE, INVALID_DATA['MISSING_PASSWORD'])
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

        self.simulate_post(USER_AUTH_ROUTE, INVALID_DATA['BAD_EMAIL'])
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

    def test_failed_auth(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

        self.simulate_post(USER_AUTH_ROUTE, INVALID_DATA['BAD_PASSWORD'])
        self.assertEqual(self.srmock.status, falcon.HTTP_401)

        self.simulate_post(USER_AUTH_ROUTE, INVALID_DATA['NOT_REGISTERED'])
        self.assertEqual(self.srmock.status, falcon.HTTP_401)


class PasswordResetRequestResourceTestCase(APITestCase):

    def test_password_reset_request_with_matching_user(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

        self.simulate_post(PASSWORD_RESET_REQUEST_ROUTE, {'email': VALID_DATA['email']})
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

        cursor = db.cursor()
        cursor.execute('SELECT COUNT(id) FROM app_password_reset')
        result = cursor.fetchone()
        self.assertEqual(int(result[0]), 1)
        cursor.close()

    def test_password_reset_request_with_no_matching_user(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

        self.simulate_post(PASSWORD_RESET_REQUEST_ROUTE, {'email': INVALID_DATA['NOT_REGISTERED']['email']})
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

    def test_password_reset_request_with_invalid_data(self):
        self.simulate_post(PASSWORD_RESET_REQUEST_ROUTE, {'email': INVALID_DATA['BAD_EMAIL']['email']})
        self.assertEqual(self.srmock.status, falcon.HTTP_400)


class PasswordResetConfirmResourceTestCase(APITestCase):

    def test_password_reset_confirm_with_matching_code(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

        self.simulate_post(PASSWORD_RESET_REQUEST_ROUTE, {'email': VALID_DATA['email']})
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

        cursor = db.cursor()
        cursor.execute('SELECT code FROM app_password_reset')
        result = cursor.fetchone()
        cursor.close()

        request_data = {
            'code': result[0],
            'password': 'newpassword'
        }
        self.simulate_post(PASSWORD_RESET_CONFIRM_ROUTE, request_data)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

        request_data = {
            'email': VALID_DATA['email'],
            'password': 'newpassword'
        }
        body = self.simulate_post(USER_AUTH_ROUTE, request_data)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertNotEqual(len(body['token']), 0)

    def test_password_reset_confirm_with_no_matching_code(self):
        self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

        self.simulate_post(PASSWORD_RESET_REQUEST_ROUTE, {'email': VALID_DATA['email']})
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

        request_data = {
            'code': 'does not exist',
            'password': 'newpassword'
        }
        self.simulate_post(PASSWORD_RESET_CONFIRM_ROUTE, request_data)
        self.assertEqual(self.srmock.status, falcon.HTTP_401)

    def test_password_reset_confirm_with_invalid_data(self):
        missing_password = {
            'code': 'some-fake-code'
        }
        self.simulate_post(PASSWORD_RESET_CONFIRM_ROUTE, missing_password)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

        missing_code = {
            'password': 'newpassword'
        }
        self.simulate_post(PASSWORD_RESET_CONFIRM_ROUTE, missing_code)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)


class AuthTestResourceTestCase(APITestCase):

    def test_auth_required_with_valid_token(self):
        body = self.simulate_post(USER_RESOURCE_ROUTE, VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

        body = self.simulate_get(AUTH_TEST_ROUTE, body['token'])
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(body['email'], VALID_DATA['email'])

    def test_auth_required_with_invalid_token(self):
        self.simulate_get(AUTH_TEST_ROUTE, 'fake token')
        self.assertEqual(self.srmock.status, falcon.HTTP_401)

    def test_auth_required_with_no_token(self):
        self.simulate_get(AUTH_TEST_ROUTE)
        self.assertEqual(self.srmock.status, falcon.HTTP_401)
