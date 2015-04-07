import os
from falcon.testing import TestBase
from database import database_url


class DatabaseUtilsTestCase(TestBase):

    def test_database_url(self):
        if os.getenv('DB_PORT_5432_TCP_ADDR', None):
            del os.environ['DB_PORT_5432_TCP_ADDR']
        os.environ['DATABASE_URL'] = 'testing'
        result = database_url()
        self.assertEqual(result, 'testing')
