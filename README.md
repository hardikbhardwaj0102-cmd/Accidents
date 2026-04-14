# 🚗 Accident Risk Prediction System

An AI-based web application that predicts accident risk based on road, environmental, and human factors.  
The system not only predicts risk but also provides explanations and safety recommendations to help prevent accidents.

---

## 📌 Features

- 🔍 Predict accident risk (Low / Medium / High)
- 📊 Probability visualization using graphs
- ⚠️ Explainability (why the risk is high/medium)
- 🛡️ Safety suggestions for prevention
- 📄 Downloadable risk report
- 💻 Interactive UI using Streamlit

---

## 🧠 Tech Stack

- Python
- Streamlit
- Scikit-learn
- NumPy
- Matplotlib

---

## ⚙️ How It Works

1. User inputs road and environmental conditions  
2. Data is encoded and passed to the ML model  
3. Model predicts accident risk  
4. System displays:
   - Risk level  
   - Confidence score  
   - Probability graph  
   - Risk explanation  
   - Safety suggestions  
5. User can download a report  

---

## 🤖 Machine Learning Model

- Algorithm: **Random Forest Classifier**
- Why used:
  - Handles complex and non-linear data
  - Works well with mixed features
  - Reduces overfitting

---

## 📸 Demo

### 🔹 Input Page
![Input Page](images/input.png)

### 🔹 Result Page
![Result Page](images/result.png)

### 🔹 Graph & Suggestions
![Graph](images/graph.png)
