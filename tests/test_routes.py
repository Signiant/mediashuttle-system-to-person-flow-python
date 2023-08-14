import unittest
from flask import Flask
from unittest.mock import patch

from openapi_client.model.package_token_response import PackageTokenResponse


class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_file_acquisition(self):
        mocked_instance = PackageTokenResponse(
            user={"email": "test@gmail.com"},
            grants=["upload"],
            expiresOn="2023-05-29T09:56:39.911Z",
            createdOn="2023-05-29T09:56:39.911Z"
        )
        with patch.object(self.client, 'get', return_value=mocked_instance):
            response = self.client.get('/api/fileAcquisition')
            self.assertEqual(response, mocked_instance)

    def test_file_distribution(self):
        mocked_instance = PackageTokenResponse(
            user={"email": "test@gmail.com"},
            grants=["download"],
            expiresOn="2023-05-29T09:56:39.911Z",
            createdOn="2023-05-29T09:56:39.911Z"
        )
        with patch.object(self.client, 'get', return_value=mocked_instance):
            response = self.client.get('/api/fileDistribution')
            self.assertEqual(response, mocked_instance)


if __name__ == '__main__':
    unittest.main()
