# core/mdapi.py

import requests
import os
import json


BASE_URL = "https://mosdac.gov.in/api"


# ================= LOGIN =================
def get_token(username, password, log_func=print):
    try:
        log_func("🔐 Logging in...")

        url = f"{BASE_URL}/token"

        payload = {
            "username": username,
            "password": password
        }

        response = requests.post(url, data=payload)

        if response.status_code != 200:
            log_func("❌ Login failed")
            return None

        data = response.json()

        tokens = {
            "access_token": data.get("access"),
            "refresh_token": data.get("refresh")
        }

        log_func("✅ Login successful")

        return tokens

    except Exception as e:
        log_func(f"❌ Login error: {e}")
        return None


# ================= SEARCH =================
def search_results(datasetId, startTime, endTime, access_token, log_func=print):
    try:
        log_func("🔍 Searching datasets...")

        url = f"{BASE_URL}/search"

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        params = {
            "datasetId": datasetId,
            "startTime": startTime,
            "endTime": endTime
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            log_func("❌ Search failed")
            return 0, []

        data = response.json()

        files = data.get("data", [])

        log_func(f"📦 Found {len(files)} files")

        return len(files), files

    except Exception as e:
        log_func(f"❌ Search error: {e}")
        return 0, []


# ================= DOWNLOAD =================
def download_file(url, headers, output_path, filename, log_func=print):

    try:
        response = requests.get(url, headers=headers, stream=True)

        if response.status_code != 200:
            log_func(f"❌ Failed: {filename}")
            return False

        file_path = os.path.join(output_path, filename)

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        log_func(f"⬇ Downloaded: {filename}")
        return True

    except Exception as e:
        log_func(f"❌ Download error {filename}: {e}")
        return False


# ================= FETCH & DOWNLOAD =================
def fetch_and_download_data(files, access_token, output_path, log_func=print):

    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        success_count = 0

        for file in files:

            download_url = file.get("downloadUrl")
            filename = file.get("fileName")

            if not download_url or not filename:
                continue

            ok = download_file(download_url, headers, output_path, filename, log_func)

            if ok:
                success_count += 1

        log_func(f"✅ Download completed: {success_count}/{len(files)}")

        return True, success_count

    except Exception as e:
        log_func(f"❌ Download process error: {e}")
        return False, 0