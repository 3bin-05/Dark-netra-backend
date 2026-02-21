import pandas as pd
from catboost import CatBoostClassifier
from config import MODEL_PATH
from services.risk_engine import calculate_final_risk

# Load model once at startup
model = CatBoostClassifier()
model.load_model(MODEL_PATH)

# Exact feature order used during training
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


def predict(features_dict, google_safe=None, vt_score=None):
    # Default fallback so old route calls don’t crash
    if google_safe is None:
        google_safe = True
    if vt_score is None:
        vt_score = 0

    df = pd.DataFrame([features_dict])

    # Ensure correct feature order
    df = df[FEATURE_COLUMNS]

    # ML prediction
    prediction = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])

    # Convert ML probability to 0–100 score
    ml_score = probability * 100

    # 🔥 Hybrid Risk Calculation
    final_score, risk_level = calculate_final_risk(
        ml_score=ml_score,
        google_safe=google_safe,
        vt_score=vt_score
    )

    return {
        "ml_prediction": prediction,
        "ml_probability": round(probability, 4),
        "ml_score": round(ml_score, 2),
        "google_safe": google_safe,
        "vt_score": round(vt_score, 2),
        "final_score": final_score,
        "risk_level": risk_level
    }