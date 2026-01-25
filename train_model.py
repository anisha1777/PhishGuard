"""
Train XGBoost model for phishing detection
This script loads the phishing dataset and trains an XGBoost classifier
"""

import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import os

def main():
    # Check if dataset exists
    dataset_file = 'phishing_dataset.csv'
    
    if not os.path.exists(dataset_file):
        print(f"❌ Error: '{dataset_file}' not found!")
        print("\n📝 Please create the dataset first by running:")
        print("   python create_training_data.py\n")
        return False
    
    print("🔄 Loading dataset...")
    data = pd.read_csv(dataset_file)
    print(f"  • Loaded {len(data)} samples")
    print(f"  • Features: {list(data.columns[:-1])}")
    
    # Define Features (X) and Target (y)
    X = data[['url_length', 'dots', 'hyphens', 'has_at_symbol', 'has_https']]
    y = data['label']
    
    print(f"\n📊 Data distribution:")
    print(f"  • Safe URLs (0): {len(y[y == 0])}")
    print(f"  • Phishing URLs (1): {len(y[y == 1])}")
    
    # Split data into Training and Testing sets
    print(f"\n🔀 Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"  • Training samples: {len(X_train)}")
    print(f"  • Testing samples: {len(X_test)}")
    
    # Initialize and Train XGBoost
    print(f"\n🤖 Training XGBoost model...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42,
        verbosity=0
    )
    
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )
    
    # Make predictions
    print(f"\n📈 Evaluating model...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"\n✅ Model Performance Metrics:")
    print(f"  • Accuracy:  {accuracy * 100:.2f}%")
    print(f"  • Precision: {precision * 100:.2f}%")
    print(f"  • Recall:    {recall * 100:.2f}%")
    print(f"  • F1 Score:  {f1 * 100:.2f}%")
    
    print(f"\n📊 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Safe', 'Phishing']))
    
    print(f"\n📋 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Feature importance
    print(f"\n🎯 Feature Importance:")
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    for idx, row in feature_importance.iterrows():
        print(f"  • {row['Feature']}: {row['Importance']:.4f}")
    
    # Save the model
    model_path = "phishing_model.json"
    model.save_model(model_path)
    print(f"\n💾 Model saved as '{model_path}'")
    
    # Also save as Booster model for consistency
    booster = model.get_booster()
    booster.save_model(model_path)
    
    print(f"\n✅ Training complete! The app will now use this trained model.")
    print(f"   Restart the backend to load the new model.")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()

