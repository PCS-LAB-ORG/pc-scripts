"""
Extract billing data from Prisma Cloud CAS
"""
import json
import os
import sys
import requests as req

api = os.getenv('PRISMA_API_URL')
username = os.getenv('PRISMA_ACCESS_KEY_ID')
password = os.getenv('PRISMA_SECRET_KEY')
if ( api is None or username is None or password is None):
    print('Missing environment variables')
    sys.exit(1)

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
    payload = { 'username': username, 'password': password }
    headers = { 
        'Content-Type': 'application/json; charset=UTF-8', 
        'Accept': 'application/json; charset=UTF-8' 
    }
    result = req.post(f"{api}/login", data=json.dumps(payload), headers=headers)
    result_ok(result,'Could not authenticate to Prisma.')
    return result.json()['token']

"""
Create headers for the RESTful API calls. Returns a headers object.
"""
def get_headers(token):
    return { 
        'Content-Type': 'application/json; charset=UTF-8', 
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': token
    }

"""
Get all repos
"""
def get_all_repos():
    print('Getting all repos.')
    url = f"{api}/code/api/v1/repositories"
    result = req.get(url, headers=headers)
    result_ok(result, 'Could not retrieve repositories.')
    return json.loads(result.text)


"""
Get unique owners from all repos
"""
def get_all_owners():
    print('Getting unique owners from repos.')
    repos = get_all_repos()
    owners = []
    for r in repos:
        if r['owner'] not in owners:
            owners.append(r['owner'])
    return owners

"""
Get unique contributors from all repos
"""
def get_all_contributors():
    print('Getting unique contributors from all repos.')
    url = f"{api}/code/api/v1/billing/contributors"
    result = req.get(url, headers=headers)
    result_ok(result, 'Could not retrieve contributors.')
    return json.loads(result.text)

"""
Get contributor details from all repos
"""
def get_all_contributor_details():
    print('Getting contributor details from all repos.')
    url = f"{api}/code/api/v1/billing/contributors/detail"
    result = req.get(url, headers=headers)
    result_ok(result, 'Could not retrieve contributor detailss.')
    return json.loads(result.text)

if __name__ == '__main__':
    headers = get_headers(auth_prisma())
    # r = get_all_repos()
    # print(r)
    # r = get_all_owners()
    # print(r)
    r = get_all_contributor_details()
    print(r)
    r = get_all_contributors()
    print(r)
