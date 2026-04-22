# core/mdapi.py

import requests
import os
import time
from datetime import datetime

# ---------------- API URLs ----------------
token_url = "https://mosdac.gov.in/download_api/gettoken"
search_url = "https://mosdac.gov.in/apios/datasets.json"
download_url = "https://mosdac.gov.in/download_api/download"
refresh_url = "https://mosdac.gov.in/download_api/refresh-token"

# ---------------- LOGIN ----------------
def get_token(username, password, log):

    log("🔐 Logging in...")

    data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(token_url, json=data)

        if response.status_code != 200:
            log(f"❌ Login failed: {response.text}")
            return None

        token_response = response.json()

        log("✅ Login successful")

        return {
            "access_token": token_response.get("access_token"),
            "refresh_token": token_response.get("refresh_token")
        }

    except Exception as e:
        log(f"❌ Login error: {e}")
        return None


# ---------------- SEARCH ----------------
def search_results(datasetId, start, end, log):

    log("🔍 Searching data...")

    params = {
        "datasetId": datasetId,
        "startTime": start,
        "endTime": end
    }

    try:
        res = requests.get(search_url, params=params)

        if res.status_code != 200:
            log(f"❌ Search failed: {res.text}")
            return 0, []

        data = res.json()

        total = data.get("totalResults", 0)
        entries = data.get("entries", [])

        log(f"📦 Found {total} files")

        return total, entries

    except Exception as e:
        log(f"❌ Search error: {e}")
        return 0, []


# ---------------- DOWNLOAD ----------------
def download_file(access_token, record_id, filename, output, log):

    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"id": record_id}

    try:
        response = requests.get(download_url, headers=headers, params=params, stream=True)

        if response.status_code != 200:
            log(f"❌ Failed: {filename}")
            return False

        file_path = os.path.join(output, filename)

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        log(f"⬇ Downloaded: {filename}")
        return True

    except Exception as e:
        log(f"❌ Download error {filename}: {e}")
        return False


# ---------------- FETCH + DOWNLOAD ----------------
def fetch_and_download_data(entries, access_token, output, log):

    if not os.path.exists(output):
        os.makedirs(output)

    success_count = 0

    for i, item in enumerate(entries, start=1):

        filename = item.get("identifier")
        record_id = item.get("id")

        log(f"⬇ [{i}/{len(entries)}] {filename}")

        ok = download_file(access_token, record_id, filename, output, log)

        if ok:
            success_count += 1

    log(f"✅ Download complete: {success_count}/{len(entries)}")

    return True, success_count