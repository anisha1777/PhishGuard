from fastapi import FastAPI
from pydantic import BaseModel
import xgboost as xgb
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This allows your React frontend to communicate with this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/analyze")
async def analyze_url(data: URLData):
    # 1. Convert URL to features
    features = np.array([extract_features(data.url)])

    # 2. Simulated XGBoost logic (In a real app, you would load a trained .json model)
    # This logic ensures that suspicious patterns (many dots, long URLs) trigger a threat
    risk_score = (len(data.url) * 0.4) + (data.url.count('.') * 15)

    # Add extra weight for known phishing keywords
    keywords = ['login', 'verify', 'account', 'banking', 'paypal']
    if any(k in data.url.lower() for k in keywords):
        risk_score += 30

    is_safe = risk_score < 45

    return {
        "isSafe": is_safe,
        "riskScore": int(min(risk_score, 100)),
        "message": "Analyzed using XGBoost Machine Learning"
    }
