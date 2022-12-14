import os
from pprint import pprint
import subprocess
import requests
from dotenv import load_dotenv
import json
import argparse

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--status", help="select from 'incomplete', 'complete'", default="complete")
parser.add_argument("--uuids", help="", required=False)
args = parser.parse_args()


url = "https://api.notion.com/v1/databases/e19eff6dfb4745919abd6cfd66dc54f2/query"


if args.status == "complete":
    payload = {
        "page_size": 100,
        "filter": {
            "and": [
                {"property": "Completed", "checkbox": {"equals": True}}  # ,
                # {
                #     "or": [
                #         {"property": "Tags", "contains": "A"},
                #         {"property": "Tags", "contains": "B"},
                #     ]
                # },
            ]
        },
    }
else:
    payload = {
        "page_size": 100,
        "filter": {
            "and": [
                {"property": "Completed", "checkbox": {"equals": False}}  # ,
                # {
                #     "or": [
                #         {"property": "Tags", "contains": "A"},
                #         {"property": "Tags", "contains": "B"},
                #     ]
                # },
            ]
        },
    }
headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json",
    "authorization": os.getenv("TOKEN"),
}

response = requests.post(url, json=payload, headers=headers)

# print(response.text)

data = json.loads(response.text)

item = data["results"]
pprint(item)

print(subprocess.run(['shortcuts', 'run', 'Get all reminders with status'], capture_output=True, text=True).stdout)