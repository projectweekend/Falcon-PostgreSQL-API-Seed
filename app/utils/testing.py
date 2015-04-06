import json
from falcon.testing import TestBase
from app import api


HEADERS = {'Content-Type': 'application/json'}


class APITestCase(TestBase):

    def simulate_get(self, path, data):
        self.api = api
        return self.simulate_request(
            path=path,
            method='GET',
            headers=HEADERS,
            body=json.dumps(data))

    def simulate_post(self, path, data):
        self.api = api
        return self.simulate_request(
            path=path,
            method='POST',
            headers=HEADERS,
            body=json.dumps(data))

    def simulate_put(self, path, data):
        self.api = api
        return self.simulate_request(
            path=path,
            method='PUT',
            headers=HEADERS,
            body=json.dumps(data))

    def simulate_patch(self, path, data):
        self.api = api
        return self.simulate_request(
            path=path,
            method='PATCH',
            headers=HEADERS,
            body=json.dumps(data))

    def simulate_delete(self, path, data):
        self.api = api
        return self.simulate_request(
            path=path,
            method='DELETE',
            headers=HEADERS,
            body=json.dumps(data))
