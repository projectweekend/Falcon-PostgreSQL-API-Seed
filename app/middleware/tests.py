import falcon
from falcon.testing import TestBase
from app import api


class MiddlewareTestCase(TestBase):

    def test_json_body_parser(self):
        self.api = api
        self.simulate_request(
            path='/user',
            method='POST',
            headers={'Content-Type': 'application/json'},
            body='not json')
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
