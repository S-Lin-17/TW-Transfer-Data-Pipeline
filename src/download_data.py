import requests

def download_csv(gas_day, cycle):
    BASE_URL = "https://twtransfer.energytransfer.com/ipost/TW/capacity/operationally-available"
    params = {
        "f": "csv",
        "extension": "csv",
        "asset": "TW",
        "gasDay": gas_day.strftime("%m/%d/%Y"),
        "cycle": cycle,
        "searchType": "NOM",
        "searchString": "",
        "locType": "ALL",
        "locZone": "ALL"
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download CSV for {gas_day}, cycle {cycle}")