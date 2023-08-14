import yaml
from openapi_client.model.file_request import FileRequest


def parse_transfer_files(files_data):

    """
    This code parses transfer file data into a list of FileRequest objects
     and returns it as a dictionary with a 'files' key. If the input is None,
     an empty list is returned.
    """

    transfer_files = []
    files = {}
    if files_data is None:
        return transfer_files

    if isinstance(files_data, dict):
        files_data = [files_data]

    for file_data in files_data:
        file_path = file_data.get('path')
        is_directory = file_data.get('isDirectory')
        file_size = file_data.get('size')
        transfer_files.append(FileRequest(path=file_path, isDirectory=is_directory, size=file_size))
    files['files'] = transfer_files
    return files


class AppConfig:

    """
        The code initializes an AppConfig class by reading configuration
         values from a YAML file. It assigns various attributes based on
         the values extracted from the file.
    """

    def __init__(self):
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

        self.developer_key = config.get('developer', {}).get('key')
        self.portal_url = config.get('portal', {}).get('url')
        self.webhook_url = config.get('webhook', {}).get('url')
        self.token_expiry_day = config.get('tokenUrl', {}).get('expiryDay')
        self.base_path = config.get('base', {}).get('path')
        self.user_mail = config.get('user', {}).get('mail')
        self.server_port = config.get('server', {}).get('port')
        self.destination_path = config.get('destination', {}).get('path')
        self.transfer_files = parse_transfer_files(config.get('transferfiles', {}).get('files'))

