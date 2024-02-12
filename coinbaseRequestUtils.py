
from coinbase import jwt_generator
from coinbase.constants import USER_AGENT
import requests

# mysecrets is not uploaded for security reasons. it just contains api_key and api_secret.
from mysecrets import api_key, api_secret

# this is using the default base url to generate jwt uri. check format_jwt_uri for more
def getJWT(method, path):
    jwt_uri = jwt_generator.format_jwt_uri(method, path)
    return jwt_generator.build_rest_jwt(jwt_uri, api_key, api_secret)

def getJWT(method, apiDomain, path):
    jwt_uri = f"{method} {apiDomain}{path}"
    return jwt_generator.build_rest_jwt(jwt_uri, api_key, api_secret)

def getCBHeaders(jwt_token):
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}",
        "User-Agent": USER_AGENT,
    }

# returns response. use res.getcode() to get request code, use res.read() to get the response data.
def makeRequest(method, apiDomain, path):
    jwt_token = getJWT(method, apiDomain, path)
    headers = getCBHeaders(jwt_token)
    url = "https://" + apiDomain + path
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error for makeRequest of", method, path, "errorCode:", response.status_code)
        print("Err body: ", response.text)
    return response
