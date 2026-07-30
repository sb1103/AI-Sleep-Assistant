#  AI Sleep Assistant – Multi-Agent Sleep Analysis System

An AI-powered **Sleep Analysis and Health Recommendation System** developed as a **B.Tech Final Year Project**. The application uses a **Multi-Agent Architecture**, **Machine Learning**, and **Google Gemini AI** to analyze sleep patterns, generate personalized insights, predict future sleep trends, and provide intelligent sleep coaching.

---

## 📌 Project Overview

AI Sleep Assistant helps users evaluate their sleep quality by analyzing:

- Sleep Duration
- Heart Rate
- Stress Level

The system combines rule-based analysis, machine learning, and Google Gemini AI to provide:

- Sleep Quality Assessment
- Sleep Score
- Health Analysis
- Personalized Recommendations
- AI-Generated Summary
- AI Trend Prediction
- AI Sleep Coach

---

##  Features

###  Sleep Analysis
- Rule-based sleep quality analysis
- Sleep stage prediction using Machine Learning
- Sleep score generation

### Health Analysis
- Heart rate analysis
- Stress level evaluation
- Health insights

### 🤖 AI Features (Powered by Google Gemini)
- AI-generated sleep report summary
- Personalized sleep recommendations
- 3-day sleep trend prediction
- Interactive AI Sleep Coach

### 📊 Visualization
- Sleep charts
- Health metrics visualization
- Sleep score dashboard

### 📁 Report Management
- Save reports automatically
- View previous reports
- Export reports as PDF

---

# 🏗 System Architecture

```
                User Input
                     │
                     ▼
           Data Collector Agent
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
 Sleep Analysis Agent      Health Agent
         │                       │
         └───────────┬───────────┘
                     ▼
            ML Sleep Agent
                     │
                     ▼
          Recommendation Agent
                     │
                     ▼
         Google Gemini AI Agent
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
 AI Generated Summary      Trend Prediction
                     │
                     ▼
             Streamlit Dashboard
```

---

# 🛠 Technologies Used

### Programming Language

- Python

### Framework

- Streamlit

### Machine Learning

- TensorFlow
- Scikit-Learn
- NumPy
- Pandas

### Artificial Intelligence

- Google Gemini API

### Visualization

- Matplotlib

### PDF Generation

- FPDF

### Environment

- Python Virtual Environment

---

# 📂 Project Structure

```
AI-Sleep-Assistant
│
├── agents/
│   ├── collector_agent.py
│   ├── coordinator.py
│   ├── health_agent.py
│   ├── llm_agent_cloud.py
│   ├── ml_sleep_agent.py
│   ├── recommendation_agent.py
│   ├── score_agent.py
│   └── sleep_analysis_agent.py
│
├── models/
│   ├── sleep_model.h5
│   └── hrv_sleep_model.pkl
│
├── scripts/
│
├── data/
│
├── app.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/sb1103/AI-Sleep-Assistant.git
```

Move into the project directory

```bash
cd AI-Sleep-Assistant
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configure Google Gemini API

Create a `.env` file in the project root.

```
GEMINI_API_KEY=YOUR_API_KEY
```

Get your API key from:

https://aistudio.google.com/app/apikey

---

#  Running the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 📸 Screenshots

## Home Page

_Add screenshot here_

---

## Sleep Analysis

_Add screenshot here_

---

## AI Summary

_Add screenshot here_

---

## AI Sleep Coach

_Add screenshot here_

---

## Charts

_Add screenshot here_

---

#  Future Enhancements

- Wearable device integration
- Real-time sleep monitoring
- Deep learning-based prediction
- Mobile application
- Cloud deployment
- User authentication
- Personalized long-term analytics

---

# 👨‍💻 Author

**Sumit Barman**

B.Tech in Computer Science & Engineering

KIIT University, Bhubaneswar

GitHub:
https://github.com/sb1103

---

# ⭐ Acknowledgements
- Google Gemini AI
- Streamlit
- TensorFlow
- Scikit-Learn

---

## 🌟 If you like this project, consider giving it a Star on GitHub!
