# Extracting  github repo data through ETL pipline to perform microsoft VS code developers behavior analysis
#1 import  libraries
import pandas as pd
import requests
import  json

import os
import requests

from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

#  Github REST API endpoints for repository contents  https://api.github.com/repos/OWNER/REPO/contents/PATH

url = "https://api.github.com/repos/microsoft/vscode/pulls?state=all&per_page=30"


def fetch_data(url):

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    print(
        "Status:", response.status_code,
        "| Remaining:", response.headers.get("X-RateLimit-Remaining")
    )

    status = response.status_code
    content_type = response.headers.get("Content-Type", "")

    if status == 200:

        if "application/json" in content_type:
            data = response.json()

        elif "text/html" in content_type:
            data = response.text

        else:
            data = response.content

        return data

    else:
        print("Request failed:", status)
        print(response.text[:300])
        return None


def fetch_all_pages(url):

    all_data = []
    page = 1

    while True:

        print(f"\nFetching page {page}...")

        data = fetch_data(f"{url}&page={page}")

        if not data:
            break

        all_data.extend(data)

        print(f"Page {page}: {len(data)} records")
        print(f"Total collected: {len(all_data)}")

        page += 1

    return all_data



fetched_data = fetch_all_pages(url)
print("\nFinal total:", len(fetched_data))


def extract_pr_fields(fetched_data):

    records = []

    for pr in fetched_data:
        records.append({
            "pr_id": pr["id"],
            "pr_number": pr["number"],
            "author_id": pr["user"]["id"],
            "author_login": pr["user"]["login"],
            "contributor_type": pr["author_association"],
            "title": pr["title"],
            "state": pr["state"],
            "draft": pr["draft"],
            "created_at": pr["created_at"],
            "updated_at": pr["updated_at"],
            "closed_at": pr["closed_at"],
            "merged_at": pr["merged_at"],
        })

    pr_records = pd.DataFrame(records)

    return pr_records


df_pr = extract_pr_fields(fetched_data)