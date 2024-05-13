import json
from base64 import b64encode
import requests

# takes api key and secret and turns them into HTTP BASIC credentials header value string
def xapi_auth_header(api_key, secret_key):
    token = b64encode(f"{api_key}:{secret_key}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

# post xAPI array to an LRS.
def post_xapi(xapi_data, host, api_key, secret_key, 
    batch=50, 
    protocol='https', 
    path='/xapi', 
    port=None, 
    version='1.0.3'
):
    with requests.Session() as s:
        # Auth and headers
        s.headers.update({ 
            'Authorization': xapi_auth_header(api_key, secret_key),
            'X-Experience-API-Version': version
            })
        
        # Create URL string
        port_string = '' if (port is None) else f':{port}'
        address = f"{protocol}://{host}{port_string}{path}/statements"
        
        # POST, one batch size at a time
        r = None
        while (len(xapi_data) > 0):
            payload = xapi_data[:batch]
            r = s.post(address, json=xapi_data)
            if r.status_code != 200:
                return r.status_code
            xapi_data = xapi_data[batch:]
        return r.status_code
    

# reads a file and passes the contents as a batch to be posted to post_xapi
def post_file(filename, host, api_key, secret_key, **kwargs):
    f = open(filename)
    data = json.load(f)
    return post_xapi(data, host, api_key, secret_key, **kwargs)
