# System-to-Person Automation API

Media Shuttle’s System-to-Person API allows you to generate single use links that allow specified users to upload or download content using a Media Shuttle portal.

## Getting Started

### Generate the code with OpenAPI Codegen

1. Follow these instructions to generate the code using OpenAPI Codegen:

- Install OpenAPI Codegen by referring to the documentation found at [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator)
-  Once installed, execute the following command.

2. If you have the JAR file, execute the command below.
```
java -jar /path_to_open_api_generator_jar_file generate -i /path_to_yaml_file -g python -o ./output_path --global-property skipFormModel=false
```

### Note
If you encounter the following error while running the code generator:
```
Exception in thread "main" java.lang.RuntimeException: Could not generate model 'AzureBlobStorage'
at org.openapitools.codegen.DefaultGenerator.generateModels(DefaultGenerator.java:569)
at org.openapitools.codegen.DefaultGenerator.generate(DefaultGenerator.java:926)
```
- Please ensure that your system is equipped with the compatible Java 11 version for code generation.
- The OpenAPI Generator is continuously maintained, and new versions are regularly released. We recommend checking the official OpenAPI Generator repository on  [GitHub](https://github.com/OpenAPITools/openapi-generator) for the most recent version and updated system requirements.



### Project Execution

1. Clone the code from the repository and import in the generated code folder.
2. Add and install packages specified in the requirements file.
``` 
pip install -r requirements.txt
```
4. Configure all the fields defined in the [Configuration]() section
5. After successfully installing the module and configuring the properties, execute the following commands:
```sh
python setup.py install --user
```
```sh
python app.py
```

## Note
In case you come across any errors while running the command ``python app.py``, consider the following fixes:

1. If you encounter following error for data classes  **ApiResponseFor200** and **ApiResponseForDefault**

```
    ]
    ^
SyntaxError: invalid syntax

```
For data class **ApiResponseFor200**, update the file
- `openapi_client/paths/portals_portal_id_subscriptions_subscription_id/delete.py`

with the following code

```python
SchemaFor200ResponseBodyApplicationJson = ResponseForPortalMember

@dataclass
class ApiResponseFor200(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[SchemaFor200ResponseBodyApplicationJson
    ]
    headers: schemas.Unset = schemas.unset
```

For data class **ApiResponseForDefault**, update the files

- `openapi_client/paths/portals_portal_id_packages_package_id/get.py`
- `openapi_client/paths/portals_portal_id_packages_package_id_files/get.py`
- `openapi_client/paths/portals_portal_id_packages_package_id_events/get.py`
- `openapi_client/paths/portals_portal_id_packages_package_id_files/put.py`

with the following code

 ```python
 SchemaFor0ResponseBodyApplicationJson = Error
 
@dataclass
class ApiResponseForDefault(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[SchemaFor0ResponseBodyApplicationJson
    ]
    headers: schemas.Unset = schemas.unset
    
 ```

2. If you encounter the following error:
```python
Exception when calling PortalsApi-> list portals: Invalid content_type returned. Content_type='application/json; charset=utf-8' was returned when only {'application/json'} are defined for status_code=200
```

update the files

- `openapi_client/paths/portals_portal_id_packages_package_id_files/put.py`
- `openapi_client/paths/portals/get.py`

with the following code for input **_response_for_200**

```python
_response_for_200 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor200,
    content={
        'application/json': api_client.MediaType(
            schema=SchemaFor200ResponseBodyApplicationJson),
        'application/json; charset=utf-8': api_client.MediaType(
            schema=SchemaFor200ResponseBodyApplicationJson),
    },
)
```

update the files

- `openapi_client/paths/portals_portal_id_packages_package_id_tokens/post.py`
- `openapi_client/paths/portals_portal_id_packages/post.py`

with the following code for input **__response_for_201**

```python
_response_for_201 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor201,
    content={
        'application/json': api_client.MediaType(
            schema=SchemaFor201ResponseBodyApplicationJson),
        'application/json; charset=utf-8': api_client.MediaType(
            schema=SchemaFor201ResponseBodyApplicationJson),
    },
)
```

3. If encounter the following error:

```
Exception when calling PortalsApi-> list portals: Invalid value Share passed in to <class 'openapi_client.model.portal.Portal.MetaOapg.properties.type'>, allowed_values=dict_keys(['send', 'share', 'submit'])
```


Fix: Please update the file located at
- `openapi_client/model/portal.py`

```python
class MetaOapg:
    enum_value_to_name = {
        "Send": "SEND",
        "Share": "SHARE",
        "Submit": "SUBMIT",
    }

@schemas.classproperty
def SEND(cls):
    return cls("Send")

@schemas.classproperty
def SHARE(cls):
    return cls("Share")

@schemas.classproperty
def SUBMIT(cls):
    return cls("Submit")

```

## Configuration
Please add the following fields to the `config.yaml` file in your project:
```yaml
developer:
  key: #dev key
portal:
  url: #portal url
webhook:
  url: #webhook url
tokenUrl:
  expiryDay: #expiry days
base:
  path: # base path
user:
  mail: #usermail
destination:
  path:
server:
  port: # server port : 8080
transferfiles:
  files:
    -
      path: #filePath1
      isDirectory: #true or false
      size: #filesize
```
- `developer key`: Add your Media Shuttle API key. You can generate an API key from your IT Administration Console in the Developer menu.
- `portal url`: Add the URL of the Media Shuttle portal.
- `webhook url`: Add the URL of the webhook where events will be received.
- `tokenUrl expiryDay`: Add the number of days for the token URL expiry.
- `base path`: Add the Media Shuttle API base URL for API calls.
- `user mail`: Add the email address where you will receive notifications of file transfers.
- `server port`: Port on which application will run
- `destination path`: Add the destination path if you want to receive files at a different location.
- `transferfiles files`: Add the following details for each transfer file:
    - `path`: Add the file path.
    - `isDirectory`: Set to `true` or `false` based on whether it's a directory.
    - `size`: Add the file size.