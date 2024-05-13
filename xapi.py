import json
from base64 import b64encode
import requests

# takes api key and secret and turns them into HTTP BASIC credentials header value string
def xapi_auth_header(api_key, secret_key):
    token = b64encode(f"{api_key}:{secret_key}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

# post xAPI array to an LRS.
def post_xapi(xapi_data, host, api_key, secret_key, batch=50, protocol='https', path='/xapi', port=None):
    port_string = '' if (port is None) else f':{port}'
    s = requests.Session()
    s.headers.update({'Authorization': xapi_auth_header(api_key, secret_key),
                      'X-Experience-API-Version': '1.0.3'})
    result = s.post(f"{protocol}://{host}{port_string}{path}/statements", json=xapi_data)
    return result.status_code

# reads a file and passes the contents as a batch to be posted to post_xapi
def post_file(filename, host, api_key, secret_key, **kwargs):
    f = open(filename)
    data = json.load(f)
    return post_xapi(data, host, api_key, secret_key, **kwargs)
