# 📧 SpamShield: Premium Email Detector

An AI-powered spam detection web application with a modern, secure architecture.

## 🚀 How to Run the Project

### 1. Set Up the Environment (Done)
The virtual environment and dependencies are already installed in the `venv` folder.

### 2. Train the Model (Optional)
If you update `spam.csv` with more data, you should re-train the model:
```powershell
.\venv\Scripts\python train_model.py
```
*This will generate `spam_model.pkl` and `vectorizer.pkl`.*

### 3. Start the Server
Run the Flask backend server:
```powershell
.\venv\Scripts\python app.py
```
*The server will start at `http://127.0.0.1:5000`.*

### 4. Access the Website
Open your browser and navigate to:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🛡️ Security Features
- **Input Sanitization**: Prevents XSS by stripping HTML tags.
- **Request Limiting**: Maximum message length of 5000 characters.
- **Security Headers**: Includes CSP, X-Frame-Options, and X-Content-Type-Options.
- **Isolation**: Runs in a managed virtual environment (`venv`).

## 🎨 Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML5, Vanilla CSS (Glassmorphism), JavaScript
- **AI/ML**: Scikit-learn (Naive Bayes Tfidf)
