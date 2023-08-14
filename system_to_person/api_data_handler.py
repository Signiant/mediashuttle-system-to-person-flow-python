from datetime import datetime, timedelta
import openapi_client
from openapi_client.apis.tags import portals_api, system_to_person_api
from openapi_client.model.package_token_request import PackageTokenRequest
from openapi_client.model.package_token_response import PackageTokenResponse
from fastapi.encoders import jsonable_encoder
from enum import Enum
from system_to_person.app_config import AppConfig
from openapi_client.paths.portals.post import SchemaForRequestBodyApplicationJson


class WorkflowType(str, Enum):
    FILE_ACQUISITION = 'file_acquisition'
    FILE_DISTRIBUTION = 'file_distribution'


config = AppConfig()


def auth():
    """
        This function sets up and returns an authenticated API client
        using the provided configuration and developer key.
    """
    configuration = openapi_client.Configuration(
        host=config.base_path
    )
    configuration.api_key['ApiKey'] = config.developer_key
    with openapi_client.ApiClient(configuration) as api_client:
        return api_client


def get_portals():
    """
        This function retrieves the ID and type of a portal by making an API call
        to the portals endpoint. If successful, it returns the portal ID and type;
        otherwise, it prints an exception message.
    """
    api_client = auth()
    try:
        url = config.portal_url
        query_params = {'url': url}
        api_instance = portals_api.PortalsApi(api_client)
        api_response = api_instance.list_portals(query_params=query_params)
        portal_data = api_response.body

        portal_item = portal_data.get("items", [{}])[0]
        portal_id = portal_item.get("id")
        portal_type = portal_item.get("type")

        return portal_id, portal_type
    except Exception as e:
        print("Exception when calling PortalsApi -> list portals: %s\n" % e)


def create_transfer_link(workflow_type):
    """
        This function creates a transfer link for a specified workflow type.
        It authenticates the API client, retrieves portals, creates a package,
        and generates a token request.
        The token request includes user information, grants, expiry date, notifications,
        and an optional destination path. Finally, it returns the token response in JSON format.
    """
    try:
        # Authentication
        api_client = auth()

        # Get portals
        portal_id, portal_type = get_portals()

        # Create package
        api_instance = system_to_person_api.CreatePackage(api_client)
        path_params = {'portalId': portal_id}
        api_response = api_instance.create_package(path_params=path_params)
        package_id = api_response.body['id']
        path_params = {'packageId': package_id, 'portalId': portal_id}

        grants_type = "upload"

        if workflow_type == WorkflowType.FILE_DISTRIBUTION:
            grants_type = "download"
            packages_file_instance = system_to_person_api.PutPackages(api_client)

            package_request_body = SchemaForRequestBodyApplicationJson(config.transfer_files)
            packages_file_instance.put_packages(body=package_request_body, path_params=path_params)

        # Create token request
        instance_kwargs = {
            "user": {"email": config.user_mail},
            "grants": [grants_type],
            "expiresOn": datetime.now() + timedelta(days=config.token_expiry_day),
            "notifications": [{"type": "webhook", "url": config.webhook_url}]
        }

        if config.destination_path is not None and config.destination_path != "" and portal_type != "Send":
            instance_kwargs["destinationPath"] = config.destination_path

        instance = PackageTokenRequest(**instance_kwargs)

        token_instance = system_to_person_api.CreateToken(api_client)
        request_body = SchemaForRequestBodyApplicationJson(instance)

        token_response = token_instance.create_token(body=request_body, path_params=path_params)
        resp = PackageTokenResponse(token_response.body)

        if workflow_type == WorkflowType.FILE_DISTRIBUTION:
            body = jsonable_encoder(resp)
            body['isReusable'] = bool(resp.get('isReusable'))
            return body
        else:
            return jsonable_encoder(resp)

    except Exception as e:
        print("Exception when creating the token url -> %s\n" % e)
