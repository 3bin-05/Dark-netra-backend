from flask import Blueprint, request, jsonify
from services.feature_extraction.feature_pipeline import extract_all_features
from services.model_service import predict
from services.risk_scoring_service import calculate_risk
from services.threat_intelligence.virustotal_service import check_virustotal
from services.threat_intelligence.google_safe_browsing_service import check_google_safe

detection_bp = Blueprint("detection_bp", __name__)

@detection_bp.route("/api/check-url", methods=["POST"])
def check_url():

    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # 1️⃣ Feature Extraction
    features = extract_all_features(url)

    # 2️⃣ ML Prediction
    ml_result = predict(features)

    # 3️⃣ Threat Intelligence
    vt_result = check_virustotal(url)
    google_result = check_google_safe(url)

    # 4️⃣ Risk Scoring
    final_result = calculate_risk(ml_result, vt_result, google_result)

    return jsonify({
        "ml_prediction": ml_result["prediction"],
        "ml_probability": ml_result["probability"],
        "virustotal": vt_result,
        "google_safe": google_result,
        "risk_score": final_result["risk_score"],
        "verdict": final_result["verdict"]
    })