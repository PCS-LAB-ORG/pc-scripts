import json
import sys
import os
import requests as req

api = ''

"""
Check the result of a restful API call
"""
def result_ok(result, message):
    if ( not result.ok ):
        print(message)
        result.raise_for_status()

"""
Authenticate against Prisma cloud. Return authentication JWT token
"""
def auth_prisma():
    global api
    api = os.getenv('PRISMA_API_URL')
    username = os.getenv('PRISMA_ACCESS_KEY_ID')
    password = os.getenv('PRISMA_SECRET_KEY')
    if ( api is None or username is None or password is None):
        print('Missing environment variables')
        sys.exit(1)

    payload = { 'username': username, 'password': password }
    headers = { 'Content-Type': 'application/json; charset=UTF-8', 'Accept': 'application/json; charset=UTF-8' }

    result = req.post(f"{api}/login", data=json.dumps(payload), headers=headers)
    result_ok(result,'Could not authenticate to Prisma.')

    return result.json()['token']

"""
Renews existing token. Returns new token to use.
"""
def extend_token(mytoken):
    headers =  {'Accept': 'application/json; charset=UTF-8','x-redlock-auth': mytoken}
    result = req.get(f"{api}/auth_token/extend", headers=headers)
    result_ok(result, 'Could not extend current token.')
    return result.json()['token']

"""
Create headers for the RESTful API calls, returns a headers object.
"""
def create_headers(token):
    return { 'Content-Type': 'application/json; charset=UTF-8', 'Accept': 'application/json; charset=UTF-8','x-redlock-auth': token}

"""
Retrieve CAS Repositoires Raw Meta Data
"""
def get_cas_repo_metadata():
    token = auth_prisma()
    headers = create_headers(token)

    # Get all build policies
    result = req.get(f"{api}/bridgecrew/api/v1/vcs-repository/repositories", headers=headers)
    result_ok(result,'Could not get build policies.')

    raw_metadata = result.json()
    print('Writing metadata.json')
    with open('metadata.json', 'w') as outfile:
        outfile.write(json.dumps(raw_metadata))

    


if __name__ == '__main__':
    print('Get CAS Repositoires Raw Meta Data -  0.0.1')
    get_cas_repo_metadata()
    print('Done')