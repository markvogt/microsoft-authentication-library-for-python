import os
import json
import logging

from oauth2cli.oauth2 import Client
from oauth2cli.authcode import obtain_auth_code
from tests import unittest



THIS_FOLDER = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(THIS_FOLDER, 'config.json')


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(CONFIG_FILE) as f:
            cls.conf = json.load(f)
        cls.client = Client(
            cls.conf['client_id'], cls.conf['client_secret'],
            authorization_endpoint=cls.conf.get("authorization_endpoint"),
            token_endpoint=cls.conf["token_endpoint"])

    def test_client_credentials(self):
        result = self.client.obtain_token_with_client_credentials(
            self.conf['scope'])
        self.assertIn('access_token', result)

    def test_username_password(self):
        result = self.client.obtain_token_with_username_password(
            self.conf["username"], self.conf["password"],
            data={"resource": self.conf.get("resource")},  # MSFT AAD V1 only
            scope=self.conf.get("scope"))
        self.assertIn('access_token', result)

    def test_auth_code(self):
        port = self.conf.get("listen_port", 44331)
        auth_request_uri = self.client.build_auth_request_uri(
            "code", redirect_uri="http://localhost:%s" % port)
        ac = obtain_auth_code(port, auth_uri=auth_request_uri)
        self.assertNotEqual(ac, None)
