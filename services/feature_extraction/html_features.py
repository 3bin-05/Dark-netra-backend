import requests
from bs4 import BeautifulSoup
from config import REQUEST_TIMEOUT

KEYWORDS_BANK = ["bank"]
KEYWORDS_PAY = ["pay", "payment"]
KEYWORDS_CRYPTO = ["crypto", "bitcoin", "wallet"]

def extract_html_features(url):

    features = {
        "LineLength": 0,
        "HasTitle": 0,
        "HasMeta": 0,
        "HasFavicon": 0,
        "HasExternalFormSubmit": 0,
        "HasCopyright": 0,
        "HasSocialNetworking": 0,
        "HasPasswordField": 0,
        "HasSubmitButton": 0,
        "HasKeywordBank": 0,
        "HasKeywordPay": 0,
        "HasKeywordCrypto": 0,
        "NoOfPopup": 0,
        "NoOfiFrame": 0,
        "NoOfImage": 0,
        "NoOfJS": 0,
        "NoOfCSS": 0,
        "NoOfURLRedirect": 0,
        "NoOfHyperlink": 0
    }

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        html = response.text

        features["LineLength"] = len(html.splitlines())

        soup = BeautifulSoup(html, "html.parser")

        # Basic tag presence
        features["HasTitle"] = 1 if soup.title else 0
        features["HasMeta"] = 1 if soup.find("meta") else 0
        features["HasFavicon"] = 1 if soup.find("link", rel="icon") else 0
        features["HasPasswordField"] = 1 if soup.find("input", {"type": "password"}) else 0
        features["HasSubmitButton"] = 1 if soup.find("input", {"type": "submit"}) else 0

        # Count tags
        features["NoOfiFrame"] = len(soup.find_all("iframe"))
        features["NoOfImage"] = len(soup.find_all("img"))
        features["NoOfJS"] = len(soup.find_all("script"))
        features["NoOfCSS"] = len(soup.find_all("link", rel="stylesheet"))
        features["NoOfHyperlink"] = len(soup.find_all("a"))

        # Simple popup detection (window.open)
        features["NoOfPopup"] = html.lower().count("window.open")

        # Keyword checks
        text_content = soup.get_text().lower()

        features["HasKeywordBank"] = 1 if any(k in text_content for k in KEYWORDS_BANK) else 0
        features["HasKeywordPay"] = 1 if any(k in text_content for k in KEYWORDS_PAY) else 0
        features["HasKeywordCrypto"] = 1 if any(k in text_content for k in KEYWORDS_CRYPTO) else 0

        # Social media presence
        if any(s in html.lower() for s in ["facebook", "twitter", "instagram"]):
            features["HasSocialNetworking"] = 1

        # Copyright
        if "copyright" in text_content:
            features["HasCopyright"] = 1

        # External form submit
        forms = soup.find_all("form")
        for form in forms:
            action = form.get("action")
            if action and not action.startswith(url):
                features["HasExternalFormSubmit"] = 1
                break

        # Redirect count
        features["NoOfURLRedirect"] = len(response.history)

    except Exception:
        # If site fails to load, keep default values
        pass

    return features