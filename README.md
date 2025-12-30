# 🏥 AI-Driven Hospital Allocation System

An intelligent, web-based healthcare decision support system that recommends the most suitable hospital during medical emergencies. The system evaluates hospitals using ICU availability, emergency severity, and geographic proximity, and presents explainable, data-backed recommendations through a clean user interface and an assistant chatbot.

---

## 📌 Problem Statement

During medical emergencies, patients and caregivers often struggle to identify the right hospital quickly. Critical information such as ICU bed availability, ICU load, hospital capability, and distance is rarely accessible in real time. This lack of visibility can result in delayed treatment and unsafe decisions.

This project aims to solve this problem by providing an AI-assisted hospital recommendation system that supports faster, safer, and more informed decision-making.

---

## 💡 Solution Overview

The AI-Driven Hospital Allocation System analyzes hospital data and ranks hospitals based on multiple critical parameters. The system highlights the most suitable hospital and provides clear explanations to build trust and transparency.

The solution focuses on:
- Emergency severity
- ICU capacity and current load
- Geographic proximity
- Explainable decision-making

---

## ✨ Key Features

- 🏥 Smart hospital ranking based on ICU data and severity
- 📊 ICU load and ICU bed availability analysis
- 📍 Distance calculation using latitude and longitude
- 🗺️ Interactive hospital map with Google Maps directions
- 🤖 Explainable chatbot assistant
- 🚨 Emergency call support (All India Emergency Number – 112)
- 📈 ICU load comparison chart
- ⚠️ Severity-based medical guidance

---
## 🖼 Dashboard Screenshots

### Crime in India – Overview
---
![Crime Dashboard Overview](Screenshot%202025-12-30%20033006.png)

### Crime Trend & Victim Analysis
---
![Crime Trend Analysis](Screenshot%202025-12-30%20033026.png)

### Property Crime Analysis
---
![Property Crime Analysis](Screenshot%202025-12-30%20033034.png)

### Area-wise Focused View
---
![State Wise Analysis](Screenshot%202025-12-30%20033049.png)

---
## 🧠 How the System Works

1. The user selects a city, emergency type, and severity level
2. Hospitals are filtered based on the selected city
3. Each hospital is scored using:
   - ICU load (lower load is prioritized)
   - ICU bed availability
   - Emergency compatibility
4. Hospitals are ranked based on the final score
5. The top-ranked hospital is highlighted as the best match
6. The chatbot explains why a hospital was recommended

---

## ⚙️ Technology Stack

### Backend
- Python
- Flask
- Pandas
- RapidFuzz (for fuzzy city matching)

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js
- Leaflet.js

### Data
- CSV-based hospital dataset containing city, state, ICU beds, ICU load, hospital level, and geographic coordinates

---

## 🏗️ Project Structure

```
hospital-allocation-system/
├── app.py
├── config.py
├── requirements.txt
├── services/
│   └── allocation_engine.py
├── utils/
│   └── data_loader.py
├── templates/
│   ├── index.html
│   └── result.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── chat.js
└── data/
    └── hospitals.csv
```

---

## 🚀 How to Run the Project

1. Clone the repository
```
git clone https://github.com/your-username/hospital-allocation-system.git
cd hospital-allocation-system
```

2. (Optional) Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Run the application
```
python app.py
```

5. Open the application in your browser
```
http://127.0.0.1:5000/
```

---

## 💬 Chatbot Capabilities

The assistant helps users understand system decisions by answering:
- Why a particular hospital was recommended
- What ICU load means
- How severity affects hospital selection
- Why other hospitals were ranked lower

This ensures transparency and explainability in healthcare decision-making.

---

## 🎯 Evaluation Highlights

- Real-world healthcare use case
- Focus on emergency decision support
- Explainable and transparent logic
- Clean and professional UI
- Scalable and modular architecture

---

## 🔮 Future Enhancements

- Real-time ICU data integration
- Ambulance routing and ETA estimation
- Doctor and specialty matching
- Multilingual support
- Cloud deployment
- Machine learning–based predictive modeling

---

## 👤 Author

**Krunal Jadhav**  
AI & Machine Learning Student  
Specializing in Data Science and Applied AI Systems

---

## ⚠️ Disclaimer

This application is intended for decision support only and does not replace professional medical advice or emergency services.

In case of a medical emergency, always contact **112** or local emergency services immediately.
