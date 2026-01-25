from fastapi import FastAPI
from pydantic import BaseModel
import xgboost as xgb
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from typing import Optional, List, Dict
from dotenv import load_dotenv
import shap

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# This allows your React frontend to communicate with this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google Safe Browsing API configuration
GOOGLE_SAFE_BROWSING_API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY", "YOUR_API_KEY_HERE")
SAFE_BROWSING_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

# Load the trained XGBoost model
# Get the directory where this app.py is located
APP_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(APP_DIR, "phishing_model.json")
MODEL = None
EXPLAINER = None

# Feature names for explainability
FEATURE_NAMES = [
    "URL Length",
    "Number of Dots",
    "Number of Hyphens",
    "Presence of @ Symbol",
    "HTTPS Usage"
]

# Feature descriptions
FEATURE_DESCRIPTIONS = {
    "URL Length": "Shorter URLs are typically more legitimate",
    "Number of Dots": "More dots suggest domain spoofing attempts",
    "Number of Hyphens": "Hyphens are common in phishing URLs to disguise domains",
    "Presence of @ Symbol": "@ symbol can hide the real domain in phishing URLs",
    "HTTPS Usage": "Legitimate sites typically use HTTPS for security"
}

def load_model():
    """Load the trained XGBoost model and create SHAP explainer"""
    global MODEL, EXPLAINER
    try:
        if os.path.exists(MODEL_PATH):
            MODEL = xgb.Booster(model_file=MODEL_PATH)
            print(f"✓ Trained XGBoost model loaded from {MODEL_PATH}")
            
            # Initialize SHAP explainer (using TreeExplainer for XGBoost)
            try:
                EXPLAINER = shap.TreeExplainer(MODEL)
                print(f"✓ SHAP Explainer initialized successfully")
            except Exception as e:
                print(f"⚠ Warning: Could not initialize SHAP Explainer: {str(e)}")
                EXPLAINER = None
        else:
            print(f"⚠ Warning: Model file '{MODEL_PATH}' not found. Please run train_model.py first.")
            print("  Using fallback analysis for now.")
            MODEL = None
            EXPLAINER = None
    except Exception as e:
        print(f"✗ Error loading model: {str(e)}")
        print("  Using fallback analysis for now.")
        MODEL = None
        EXPLAINER = None

# Load model on startup
load_model()


class URLData(BaseModel):
    url: str


def extract_features(url):
    # ML models need numbers. This converts the URL into data points.
    return [
        len(url),                   # URL length
        url.count('.'),             # Number of dots
        url.count('-'),             # Number of hyphens
        1 if "@" in url else 0,     # Presence of @ symbol
        1 if "https" in url else 0  # Presence of HTTPS
    ]


async def check_google_safe_browsing(url: str) -> Optional[dict]:
    """
    Check URL using Google Safe Browsing API
    Returns threat information if found, None if safe
    """
    if GOOGLE_SAFE_BROWSING_API_KEY == "YOUR_API_KEY_HERE":
        return None
    
    try:
        payload = {
            "client": {
                "clientId": "phishguard",
                "clientVersion": "1.0.0"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "POTENTIALLY_HARMFUL_APPLICATION", "UNWANTED_SOFTWARE"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [
                    {"url": url}
                ]
            }
        }
        
        response = requests.post(
            f"{SAFE_BROWSING_URL}?key={GOOGLE_SAFE_BROWSING_API_KEY}",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if "matches" in data and data["matches"]:
                return {
                    "threats": data["matches"],
                    "safe": False
                }
        return {"safe": True}
    except Exception as e:
        print(f"Google Safe Browsing error: {str(e)}")
        return None


def get_feature_explanations(features_array: np.ndarray, prediction: float) -> List[Dict]:
    """
    Generate SHAP-based explanations for the model prediction
    Shows which features contributed to the decision
    """
    explanations = []
    
    if EXPLAINER is None:
        return explanations
    
    try:
        # Get SHAP values for this prediction
        dmatrix = xgb.DMatrix(features_array)
        shap_values = EXPLAINER.shap_values(dmatrix)
        
        # Get the base value (model's average prediction)
        base_value = EXPLAINER.expected_value
        
        # Create explanation for each feature
        for i, feature_name in enumerate(FEATURE_NAMES):
            shap_value = float(shap_values[0][i])
            feature_value = float(features_array[0][i])
            
            # Determine if feature pushed prediction towards phishing or safe
            contribution = "increases" if shap_value > 0 else "decreases"
            phishing_risk_text = "phishing risk" if shap_value > 0 else "safety confidence"
            
            explanations.append({
                "feature": feature_name,
                "value": feature_value,
                "shap_value": shap_value,
                "impact": abs(shap_value),
                "direction": "phishing" if shap_value > 0 else "safe",
                "description": FEATURE_DESCRIPTIONS.get(feature_name, ""),
                "explanation": f"{feature_name} (value: {feature_value:.1f}) {contribution} {phishing_risk_text}"
            })
        
        # Sort by absolute SHAP value (most important first)
        explanations.sort(key=lambda x: x["impact"], reverse=True)
        
        return explanations
    except Exception as e:
        print(f"Error generating SHAP explanations: {str(e)}")
        return []


@app.post("/analyze")
async def analyze_url(data: URLData):

    # 1. Convert URL to features
    features = extract_features(data.url)
    features_array = np.array([features], dtype=np.float32)
    
    # 2. Get prediction from trained XGBoost model or use fallback
    explanations = []
    if MODEL is not None:
        try:
            # Create DMatrix for XGBoost prediction
            dmatrix = xgb.DMatrix(features_array)
            prediction = MODEL.predict(dmatrix)
            
            # XGBoost returns probability for class 1 (phishing)
            phishing_probability = float(prediction[0])
            
            # Convert probability to risk score (0-100)
            risk_score = int(phishing_probability * 100)
            is_safe = phishing_probability < 0.5
            model_source = "Trained XGBoost Model"
            
            # Get SHAP explanations for why this decision was made
            explanations = get_feature_explanations(features_array, phishing_probability)
            
        except Exception as e:
            print(f"Model prediction error: {str(e)}")
            # Fallback to simulated logic if model prediction fails
            risk_score, is_safe = _get_fallback_risk_score(data.url)
            model_source = "Fallback Logic"
    else:
        # No model loaded, use fallback logic
        risk_score, is_safe = _get_fallback_risk_score(data.url)
        model_source = "Fallback Logic (Model not loaded)"

    # 3. Check Google Safe Browsing API
    google_result = await check_google_safe_browsing(data.url)
    google_safe = True
    google_threat = None
    
    if google_result:
        google_safe = google_result.get("safe", True)
        if not google_safe:
            google_threat = google_result.get("threats", [])
            risk_score = 95  # Critical risk if Google flags it
            is_safe = False

    return {
        "isSafe": is_safe,
        "riskScore": int(min(risk_score, 100)),
        "message": f"Analyzed using {model_source} and Google Safe Browsing API",
        "checks": {
            "xgboost": {
                "safe": is_safe if MODEL is not None else None,
                "riskScore": risk_score,
                "message": f"XGBoost analysis completed using {model_source}",
                "model_loaded": MODEL is not None,
                "explanations": explanations  # Add SHAP explanations
            },
            "googleSafeBrowsing": {
                "safe": google_safe,
                "threats": google_threat,
                "message": "Google Safe Browsing check completed" if google_result else "Google Safe Browsing API key not configured"
            }
        }
    }


def _get_fallback_risk_score(url: str):
    """
    Fallback risk scoring when model is not available
    This uses pattern-based heuristics similar to the original logic
    """
    risk_score = 0
    
    # URL length analysis (typical phishing URLs are longer)
    if len(url) > 75:
        risk_score += 20
    elif len(url) > 54:
        risk_score += 10
    
    # Number of dots (more dots = more suspicious)
    dot_count = url.count('.')
    if dot_count > 4:
        risk_score += 25
    elif dot_count > 2:
        risk_score += 10
    
    # Hyphen count
    if url.count('-') > 4:
        risk_score += 15
    
    # @ symbol (used to hide real domain)
    if "@" in url:
        risk_score += 30
    
    # HTTPS presence (legitimate sites usually have HTTPS)
    if "https" not in url:
        risk_score += 15
    
    # Known phishing keywords
    keywords = ['login', 'verify', 'account', 'banking', 'paypal', 'update', 'confirm']
    keyword_count = sum(1 for k in keywords if k in url.lower())
    if keyword_count > 0:
        risk_score += (keyword_count * 10)
    
    is_safe = risk_score < 45
    return risk_score, is_safe
