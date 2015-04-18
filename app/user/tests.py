import falcon
from app import db
from app.utils.testing import APITestCase


USER_RESOURCE_ROUTE = '/v1/user'
USER_AUTH_ROUTE = '/v1/authenticate'
PASSWORD_RESET_REQUEST_ROUTE = '/v1/password-reset/request'

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
