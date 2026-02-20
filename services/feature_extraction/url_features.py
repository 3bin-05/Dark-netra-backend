import re
from urllib.parse import urlparse

def extract_url_features(url):
    parsed = urlparse(url)

    features = {}

    # -----------------------
    # HTTPS
    # -----------------------
    features["IsHTTPS"] = 1 if parsed.scheme == "https" else 0

    # -----------------------
    # Domain is IP
    # -----------------------
    features["IsDomainIP"] = 1 if re.match(r"\d+\.\d+\.\d+\.\d+", parsed.netloc) else 0

    # -----------------------
    # TLD
    # -----------------------
    domain_parts = parsed.netloc.split(".")
    features["TLD"] = domain_parts[-1] if len(domain_parts) > 1 else "unknown"

    # -----------------------
    # Length Features
    # -----------------------
    features["URLLength"] = len(url)
    features["NoOfSubDomain"] = len(domain_parts) - 2 if len(domain_parts) > 2 else 0
    features["NoOfDots"] = url.count(".")
    features["NoOfObfuscatedChar"] = len(re.findall(r"[%@]", url))
    features["NoOfEqual"] = url.count("=")
    features["NoOfQmark"] = url.count("?")
    features["NoOfAmp"] = url.count("&")
    features["NoOfDigits"] = sum(c.isdigit() for c in url)

    return features