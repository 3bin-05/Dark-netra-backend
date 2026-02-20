import pandas as pd
from catboost import CatBoostClassifier
from config import MODEL_PATH

# Load model once at startup
model = CatBoostClassifier()
model.load_model(MODEL_PATH)

# 🔥 IMPORTANT: Exact feature order used during training
FEATURE_COLUMNS = [
    'IsHTTPS',
    'IsDomainIP',
    'TLD',
    'URLLength',
    'NoOfSubDomain',
    'NoOfDots',
    'NoOfObfuscatedChar',
    'NoOfEqual',
    'NoOfQmark',
    'NoOfAmp',
    'NoOfDigits',
    'LineLength',
    'HasTitle',
    'HasMeta',
    'HasFavicon',
    'HasExternalFormSubmit',
    'HasCopyright',
    'HasSocialNetworking',
    'HasPasswordField',
    'HasSubmitButton',
    'HasKeywordBank',
    'HasKeywordPay',
    'HasKeywordCrypto',
    'NoOfPopup',
    'NoOfiFrame',
    'NoOfImage',
    'NoOfJS',
    'NoOfCSS',
    'NoOfURLRedirect',
    'NoOfHyperlink',
    'SuspiciousCharRatio',
    'URLComplexityScore',
    'HTMLContentDensity',
    'InteractiveElementDensity'
]

def predict(features_dict):
    """
    Takes dictionary of features and returns:
    - predicted class
    - prediction probability
    """

    df = pd.DataFrame([features_dict])

    # Ensure correct order
    df = df[FEATURE_COLUMNS]

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return {
        "prediction": int(prediction),
        "probability": float(probability)
    }