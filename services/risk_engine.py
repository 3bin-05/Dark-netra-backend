def calculate_final_risk(ml_score, google_safe, vt_score):
    """
    ml_score: 0–100
    google_safe: True or False
    vt_score: 0–100 (percentage of engines detecting)
    """

    # Case 1: Strong malicious signal from reputation
    if not google_safe or vt_score >= 30:
        final_score = 90

    # Case 2: Reputation clean → reduce ML dominance
    elif google_safe and vt_score < 5:
        final_score = ml_score * 0.4

    # Case 3: Mixed signals
    else:
        final_score = (ml_score * 0.6) + (vt_score * 0.4)

    # Risk classification
    if final_score < 30:
        risk_level = "Low"
    elif final_score < 60:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return round(final_score, 2), risk_level