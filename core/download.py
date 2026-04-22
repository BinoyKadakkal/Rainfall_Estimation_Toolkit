from core import mdapi


def run_download(username, password, start, end, source, output, log):

    try:
        log("⬇ Starting download...")

        # LOGIN
        tokens = mdapi.get_token(username, password, log)

        if not tokens:
            log("❌ Login failed")
            return

        access_token = tokens["access_token"]

        # DATASET MAP
        dataset_map = {
            "TERLS": "RCTLS_L2B_STD",
            "SHAR": "RSHAR_L2B_STD",
            "CHERRAPUNJI": "RCHER_L2B_STD"
        }

        datasetId = dataset_map.get(source, "RCTLS_L2B_STD")

        # SEARCH (FIXED)
        total, files = mdapi.search_results(
            datasetId,
            start,
            end,
            access_token,
            log
        )

        if total == 0:
            log("⚠ No files found")
            return

        # DOWNLOAD
        success, count = mdapi.fetch_and_download_data(
            files,
            access_token,
            output,
            log
        )

        if success:
            log(f"✅ Download complete: {count} files")

    except Exception as e:
        log(f"❌ Error: {e}")