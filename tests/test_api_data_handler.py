import unittest
from unittest import mock

from system_to_person.api_data_handler import create_transfer_link, WorkflowType


class ApiHelperTestCase(unittest.TestCase):

    @mock.patch('system_to_person.api_data_handler.auth')
    @mock.patch('system_to_person.api_data_handler.get_portals')
    @mock.patch('system_to_person.api_data_handler.system_to_person_api.CreatePackage')
    @mock.patch('system_to_person.api_data_handler.system_to_person_api.PutPackages')
    @mock.patch('system_to_person.api_data_handler.system_to_person_api.CreateToken')
    def test_create_transfer_link(self, mock_create_token, mock_put_packages, mock_create_package,
                                  mock_get_portals, mock_api_client):
        # Mock ApiClient
        mock_api_instance = mock_api_client.return_value
        mock_api_instance.api_key['ApiKey'] = 'c6eadd9d-712a-41a4-a270-4044sd385da1'

        # Mock get_portals
        mock_get_portals.return_value = ('d6ecca9d-532a-a270-c352-5005ba385da1', 'Send')

        # Mock create_package
        mock_create_package_instance = mock_create_package.return_value
        mock_create_package_instance.create_package.return_value.body = {'id': '0dd4eda-ea8b-4e9e-bdc1-461f3bb53aa'}

        # Mock PutPackages
        mock_put_packages_instance = mock_put_packages.return_value

        # Mock CreateToken
        mock_create_token_instance = mock_create_token.return_value
        body = {
            'id': '4b5e654b-f8b7-48da-b7b6-e740e8fc9042',
            'isReusable': True,
            "createdOn": "2023-05-30T09:51:47.515Z",
            "expiresOn": "2023-06-09T15:21:46.635Z",
            "notifications": [
                {
                    "type": "webhook",
                    "url": "https://example.com",

                }
            ],
            "url": "https://tokenexampleurl.com",
            "user": {
                "email": "test@test.com"
            }
        }
        mock_create_token_instance.create_token.return_value.body = body

        result = create_transfer_link(WorkflowType.FILE_DISTRIBUTION)

        # Assertions
        mock_api_client.assert_called_once()
        mock_get_portals.assert_called_once()
        mock_create_package.assert_called_once_with(mock_api_instance)
        mock_put_packages.assert_called_once_with(mock_api_instance)
        mock_create_token.assert_called_once_with(mock_api_instance)

        mock_put_packages_instance.put_packages.assert_called_once()
        mock_create_token_instance.create_token.assert_called_once()

        self.assertEqual(result, body)


if __name__ == '__main__':
    unittest.main()
