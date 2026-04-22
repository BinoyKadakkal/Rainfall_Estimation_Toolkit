from core import mdapi


def run_download(username, password, start, end, source, output, log):

    dataset_map = {
        "TERLS": "RCTLS_L2B_STD",
        "SHAR": "RSHAR_L2B_STD",
        "CHERRAPUNJI": "RCHER_L2B_STD"
    }

    datasetId = dataset_map.get(source, "RCTLS_L2B_STD")

    tokens = mdapi.get_token(username, password, log)

    if not tokens:
        return

    total, entries = mdapi.search_results(datasetId, start, end, log)

    if total == 0:
        log("⚠ No files found")
        return

    mdapi.fetch_and_download_data(entries, tokens["access_token"], output, log)