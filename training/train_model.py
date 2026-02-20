import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("PhishOFE_ds.csv")

print("Columns:", df.columns)

# -----------------------
# DERIVED FEATURES
# -----------------------

df["SuspiciousCharRatio"] = (
    df["NoOfObfuscatedChar"] +
    df["NoOfEqual"] +
    df["NoOfQmark"] +
    df["NoOfAmp"]
) / df["URLLength"]

df["URLComplexityScore"] = (
    (df["URLLength"] + df["NoOfSubDomain"] + df["NoOfObfuscatedChar"]) / df["URLLength"]
) + (
    (df["NoOfEqual"] + df["NoOfAmp"]) / (df["NoOfQmark"] + 1)
)

df["HTMLContentDensity"] = (
    df["LineLength"] + df["NoOfImage"]
) / (
    df["NoOfJS"] + df["NoOfCSS"] + df["NoOfiFrame"] + 1
)

df["InteractiveElementDensity"] = (
    df["HasSubmitButton"] +
    df["HasPasswordField"] +
    df["NoOfPopup"]
) / (
    df["LineLength"] + df["NoOfImage"] + 1
)

# Drop raw URL column
df = df.drop("URL", axis=1)

# -----------------------
# Split Features & Label
# -----------------------

X = df.drop("label", axis=1)
y = df["label"]

# Identify categorical features
cat_features = ["TLD"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------
# Train CatBoost
# -----------------------

model = CatBoostClassifier(
    verbose=0
)

model.fit(
    X_train,
    y_train,
    cat_features=cat_features
)

# Evaluate
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
model.save_model("models/phishing_model.cbm")

print("✅ Model trained and saved successfully!")