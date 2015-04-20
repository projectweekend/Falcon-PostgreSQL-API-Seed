import json

from urlparse import urlparse
from falcon.testing import TestBase
from app import api, db
from app.config import DATABASE_URL


HEADERS = {'Content-Type': 'application/json'}


class APITestCase(TestBase):

    def setUp(self):
        super(APITestCase, self).setUp()
        self._empty_tables()

    @staticmethod
    def _empty_tables():
        parsed = urlparse(DATABASE_URL)

        app_tables_query = """
        SELECT          table_name
        FROM            information_schema.tables
        WHERE           table_schema = 'public' AND
                        table_catalog = '{0}' AND
                        table_name != 'schema_version';""".format(parsed.path.strip('/'))
        cursor = db.cursor()
        cursor.execute(app_tables_query)
        tables = [r[0] for r in cursor.fetchall()]
        for t in tables:
            query = 'TRUNCATE TABLE {0} CASCADE;'.format(t)
            cursor.execute(query)
            db.commit()
        cursor.close()

    def _simulate_request(self, method, path, data, token=None):
        if token:
            HEADERS['Authorization'] = token

        self.api = api

        result = self.simulate_request(
            path=path,
            method=method,
            headers=HEADERS,
            body=json.dumps(data))
        return json.loads(result[0])

    def simulate_get(self, path, data, token=None):
        return self._simulate_request(
            method='GET',
            path=path,
            data=data,
            token=token)

    def simulate_post(self, path, data, token=None):
        return self._simulate_request(
            method='POST',
            path=path,
            data=data,
            token=token)

    def simulate_put(self, path, data, token=None):
        return self._simulate_request(
            method='PUT',
            path=path,
            data=data,
            token=token)

    def simulate_patch(self, path, data, token=None):
        return self._simulate_request(
            method='PATCH',
            path=path,
            data=data,
            token=token)

    def simulate_delete(self, path, data, token=None):
        return self._simulate_request(
            method='DELETE',
            path=path,
            data=data,
            token=token)
