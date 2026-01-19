import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Load your dataset (Download a 'phishing.csv' from Kaggle)
# For this example, we assume columns: 'url_length', 'dots', 'hyphens', 'label'
data = pd.read_csv('phishing_dataset.csv')

# 2. Define Features (X) and Target (y)
X = data[['url_length', 'dots', 'hyphens', 'has_at_symbol', 'has_https']]
y = data['label']

# 3. Split data into Training and Testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 4. Initialize and Train XGBoost
model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

# 5. Check Accuracy
predictions = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")

# 6. Save the model to a file
model.save_model("phishing_model.json")
print("Model saved as phishing_model.json")
