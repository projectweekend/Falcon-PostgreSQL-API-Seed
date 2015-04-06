import json
import subprocess
from urlparse import urlparse
from falcon.testing import TestBase
from app import api
from app.utils.database import database_url


HEADERS = {'Content-Type': 'application/json'}


class APITestCase(TestBase):

    def setUp(self):
        super(APITestCase, self).setUp()
        self.flyway_migrate()

    def tearDown(self):
        super(APITestCase, self).tearDown()
        self.flyway_clean()

    def _run_flyway_command(self, flyway_command):
        parsed = urlparse(database_url())
        user = parsed.username
        host = parsed.hostname
        port = parsed.port
        database = parsed.path.strip('/')

        command = 'flyway -url=jdbc:postgresql://{0}:{1}/{2} -user={3} {4}'
        command = command.format(host, port, database, user, flyway_command)
        subprocess.check_call(command.split())

    def flyway_migrate(self):
        self._run_flyway_command('migrate')

    def flyway_clean(self):
        self._run_flyway_command('clean')

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
