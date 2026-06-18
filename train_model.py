# ==========================================================
# Hydrate+
# Model Training Script
# ==========================================================

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("\nLoading dataset...\n")

# ==========================================================
# LOAD DATASET
# ==========================================================

data = pd.read_csv("Hydration_Updated.csv")

data.columns = data.columns.str.strip()

# ==========================================================
# LABEL ENCODING
# ==========================================================

gender_encoder = LabelEncoder()
activity_encoder = LabelEncoder()
weather_encoder = LabelEncoder()
target_encoder = LabelEncoder()

data["Gender"] = gender_encoder.fit_transform(
    data["Gender"]
)

data["Physical Activity Level"] = activity_encoder.fit_transform(
    data["Physical Activity Level"]
)

data["Weather"] = weather_encoder.fit_transform(
    data["Weather"]
)

data["Hydration Level"] = target_encoder.fit_transform(
    data["Hydration Level"]
)

# ==========================================================
# FEATURES
# ==========================================================

X = data[

    [

        "Age",

        "Gender",

        "Weight (kg)",

        "Daily Water Intake (liters)",

        "Physical Activity Level",

        "Weather"

    ]

]

y = data["Hydration Level"]

# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

# ==========================================================
# RANDOM FOREST MODEL
# ==========================================================

model = RandomForestClassifier(

    n_estimators=300,

    class_weight="balanced",

    random_state=42

)

print("Training Random Forest Model...\n")

model.fit(

    X_train,

    y_train

)

# ==========================================================
# ACCURACY
# ==========================================================

prediction = model.predict(X_test)

accuracy = accuracy_score(

    y_test,

    prediction

)

# ==========================================================
# SAVE MODEL
# ==========================================================

joblib.dump(

    model,

    "hydration_model.pkl"

)

# ==========================================================
# SAVE LABEL ENCODERS
# ==========================================================

encoders = {

    "gender": gender_encoder,

    "activity": activity_encoder,

    "weather": weather_encoder,

    "target": target_encoder

}

joblib.dump(

    encoders,

    "label_encoders.pkl"

)

# ==========================================================
# OUTPUT
# ==========================================================

print("=====================================")

print(" Hydrate+ Model Training Complete ")

print("=====================================")

print(f"\nModel Accuracy : {accuracy*100:.2f}%")

print("\nFiles Generated:")

print("✔ hydration_model.pkl")

print("✔ label_encoders.pkl")

print("\nReady for deployment.")