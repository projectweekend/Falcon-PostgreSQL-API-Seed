import falcon
from app.utils.testing import APITestCase


VALID_DATA = {
    'email': 'abcd@efgh.com',
    'password': '12345678'
}


class UserResourceTestCase(APITestCase):

    def test_create_a_user(self):
        body = self.simulate_post('/user', VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        self.assertNotEqual(len(body['token']), 0)

    def test_create_a_dup_user(self):
        self.simulate_post('/user', VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)

        self.simulate_post('/user', VALID_DATA)
        self.assertEqual(self.srmock.status, falcon.HTTP_409)
