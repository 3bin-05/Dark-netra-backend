from flask import Blueprint, request, jsonify
from services.feature_extraction.feature_pipeline import extract_all_features
from services.model_service import predict
from services.threat_intelligence.virustotal_service import check_virustotal
from services.threat_intelligence.google_safe_browsing_service import check_google_safe

detection_bp = Blueprint("detection_bp", __name__)

@detection_bp.route("/api/check-url", methods=["POST"])
def check_url():

    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # 1️⃣ Feature Extraction
        features = extract_all_features(url)

        # 2️⃣ Threat Intelligence
        vt_result = check_virustotal(url)
        google_result = check_google_safe(url)

        # Normalize API results for risk engine
        vt_score = vt_result.get("malicious_score", 0)
        google_safe = google_result.get("safe", True)

        # 3️⃣ ML + Hybrid Risk Engine
        result = predict(
            features_dict=features,
            google_safe=google_safe,
            vt_score=vt_score
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500