import requests
from config import VIRUSTOTAL_API_KEY

def check_virustotal(url):

    try:
        headers = {"x-apikey": VIRUSTOTAL_API_KEY}

        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url}
        )

        if response.status_code == 200:
            return "safe"
        else:
            return "malicious"

    except:
        return "safe"