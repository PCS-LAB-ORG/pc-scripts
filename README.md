# cas-repo-metadata

# Download a json file of repositories metadata from Prisma Cloud

Simple python 3 script to initiate and download a json file of repositories metadata from Prisma Cloud.

To get started:

```
export PRISMA_API_URL=<your value>
export PRISMA_ACCESS_KEY_ID=<your value>
export PRISMA_SECRET_KEY=<your value>

# Very first run
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 metadata.py

```
Your JSON file will be saved in the current directory