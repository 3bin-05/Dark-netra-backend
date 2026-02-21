from config import ML_WEIGHT, VIRUSTOTAL_WEIGHT, GOOGLE_WEIGHT

def calculate_risk(ml_result, vt_result, google_result):

    ml_score = ml_result["probability"]

    vt_score = 1 if vt_result == "malicious" else 0
    google_score = 1 if google_result == "malicious" else 0

    final_score = (
        ml_score * ML_WEIGHT +
        vt_score * VIRUSTOTAL_WEIGHT +
        google_score * GOOGLE_WEIGHT
    )

    risk_percentage = round(final_score * 100, 2)

    if risk_percentage >= 75:
        verdict = "Dangerous"
    elif risk_percentage >= 40:
        verdict = "Suspicious"
    else:
        verdict = "Safe"

    return {
        "risk_score": risk_percentage,
        "verdict": verdict
    }