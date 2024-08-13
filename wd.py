import requests
import json
from pathlib import Path
import os


# Prisma Cloud API URL
PRISMA_API_URL = "https://api2.prismacloud.io"

# Replace with your Prisma Cloud access key and secret key
ACCESS_KEY = os.getenv('PRISMA_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('PRISMA_SECRET_KEY')


HEADERS = {
    "Content-Type": "application/json",
    "x-redlock-auth": None
}


def authenticate():
    auth_data = {"username": ACCESS_KEY, "password": SECRET_KEY}

    global HEADERS

    response = requests.post(
        f"{PRISMA_API_URL}/login", data=json.dumps(auth_data), headers=HEADERS
    )
    if response.status_code == 200:
        HEADERS["x-redlock-auth"] = response.json()["token"]
    else:
        raise Exception("Authentication failed")


def get_repo_scan_results():
    response = requests.get(f"{PRISMA_API_URL}/code/api/v1/development-pipeline/code-review/runs/data", headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to get runs data")


def get_repo_scan_results_v2():
    payload = json.dumps({
  "filters": {
    "checkStatus": "Error",
    "codeCategories": [
      "IacMisconfiguration",
      "IacExternalModule",
      "ImageReferencerVul",
      "ImageReferencerLicenses",
      "Vulnerabilities",
      "Licenses",
      "Secrets"
    ],
    "runId": 1628884,
    "repositories": [
      "fcbe1e52-4185-4b92-8517-f1121ca8e2b9"
    ],
    "severities": [
      "INFO",
      "LOW",
      "MEDIUM",
      "HIGH",
      "CRITICAL"
    ]
  },
  "limit": 50,
  "offset": 0
})
    head = {
        'Authorization': f"Bearer {HEADERS['x-redlock-auth']}",
        'Content-Type': 'application/json',
        "Accept": 'application/json'
    }
    response = requests.post(
        f"{PRISMA_API_URL}/code/api/v2/code-issues/code_review_scan",
        headers=HEADERS,
        data=payload
    )

    print(response)
    print(response.status_code)
    print(response.reason)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to get account groups")


if __name__ == "__main__":
    authenticate()
    data = get_repo_scan_results()
    Path("output.json").write_text(json.dumps(data, indent=4))
    data_2 = get_repo_scan_results_v2()