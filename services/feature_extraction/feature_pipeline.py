from services.feature_extraction.url_features import extract_url_features
from services.feature_extraction.html_features import extract_html_features
from services.feature_extraction.derived_features import compute_derived_features

def extract_all_features(url):
    """
    Master pipeline that:
    1️⃣ Extracts URL features
    2️⃣ Extracts HTML features
    3️⃣ Computes derived features
    4️⃣ Returns combined feature dictionary
    """

    # Step 1: URL features
    url_features = extract_url_features(url)

    # Step 2: HTML features
    html_features = extract_html_features(url)

    # Merge
    combined_features = {**url_features, **html_features}

    # Step 3: Derived features
    derived_features = compute_derived_features(combined_features)

    combined_features.update(derived_features)

    return combined_features