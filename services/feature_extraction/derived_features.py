def compute_derived_features(features):

    derived = {}

    # Avoid division by zero
    url_length = features.get("URLLength", 1)
    qmark = features.get("NoOfQmark", 0)
    line_length = features.get("LineLength", 1)

    # SuspiciousCharRatio
    derived["SuspiciousCharRatio"] = (
        features.get("NoOfObfuscatedChar", 0) +
        features.get("NoOfEqual", 0) +
        features.get("NoOfQmark", 0) +
        features.get("NoOfAmp", 0)
    ) / max(url_length, 1)

    # URLComplexityScore
    derived["URLComplexityScore"] = (
        (url_length +
         features.get("NoOfSubDomain", 0) +
         features.get("NoOfObfuscatedChar", 0)) / max(url_length, 1)
    ) + (
        (features.get("NoOfEqual", 0) +
         features.get("NoOfAmp", 0)) / (qmark + 1)
    )

    # HTMLContentDensity
    derived["HTMLContentDensity"] = (
        features.get("LineLength", 0) +
        features.get("NoOfImage", 0)
    ) / (
        features.get("NoOfJS", 0) +
        features.get("NoOfCSS", 0) +
        features.get("NoOfiFrame", 0) + 1
    )

    # InteractiveElementDensity
    derived["InteractiveElementDensity"] = (
        features.get("HasSubmitButton", 0) +
        features.get("HasPasswordField", 0) +
        features.get("NoOfPopup", 0)
    ) / (
        line_length +
        features.get("NoOfImage", 0) + 1
    )

    return derived