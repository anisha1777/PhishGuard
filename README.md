# PhishGuard

## Description
PhishGuard is a cybersecurity project built to detect phishing threats using an intelligent combination of machine learning and web technologies. Its primary goal is to analyze user input (such as email content or URLs) and classify whether it is a phishing attempt.

---

## 🔍 Features
- 🛡️ Machine Learning–powered phishing detection  
- 🔗 URL and email analysis  
- 📊 Interactive frontend built with React  
- 🧠 Trainable model using `train_model.py`  
- 🐍 Backend API support using `app.py`  

---

## 🗂️ Project Structure
```text
PhishGuard/
├── public/                 # Static public assets (icons, index.html)
├── src/                    # React frontend source
├── app.py                  # Flask backend server
├── train_model.py          # Model training script
├── package.json            # Frontend dependencies & scripts
├── package-lock.json
├── tailwind.config.js      # Frontend styling configuration
├── .gitignore
└── README.md

🧰 Tech Stack

Frontend: React, Tailwind CSS
Backend: Python (Flask)
Machine Learning: Python, Scikit-Learn
Model Pipeline:
Data preprocessing → train_model.py → classification model
Deployment: Local or Cloud (e.g., Heroku, Vercel)
🚀 Installation
1. Clone the repository
git clone https://github.com/anisha1777/PhishGuard.git
cd PhishGuard

2. Install backend dependencies
pip install -r requirements.txt


(Optional) Create a virtual environment:

python3 -m venv venv
source venv/bin/activate

3. Install frontend dependencies
cd src
npm install
npm start

4. Train the model
python train_model.py

5. Run the backend server
python app.py

📌 How It Works

The user enters an email or URL.

The backend processes the input.

The machine learning model evaluates phishing risk.

The result is returned and displayed in the frontend UI.

🧪 Testing

Use known phishing emails and safe samples.

Validate model predictions.

Track false positives and false negatives for improvement.

🤝 Contributing

Contributions are welcome.

Please:

Open issues for bugs or feature requests

Submit pull requests
