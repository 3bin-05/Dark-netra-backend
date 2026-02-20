import requests
from config import GOOGLE_SAFE_BROWSING_API_KEY

def check_google_safe(url):

    try:
        body = {
            "client": {
                "clientId": "dark-netra",
                "clientVersion": "1.0"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }

        response = requests.post(
            f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_API_KEY}",
            json=body
        )

        if response.json():
            return "malicious"
        else:
            return "safe"

    except:
        return "safe"