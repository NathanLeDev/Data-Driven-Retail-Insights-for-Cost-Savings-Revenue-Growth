# 🛒 Data-Driven Retail Engine: Segmentation, MBA & Predictive ROI

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-DSTI-purple)](LICENSE)

## 🎯 Executive Summary
This project delivers a high-performance retail analytics pipeline designed to transform raw transactional data into a profitable promotional strategy. By processing **33 million rows**, the engine segments customers, identifies stable product associations, and triggers personalized "just-in-time" recommendations with a validated financial impact.

**Key Achievement:** Developed an automated decision system generating **€5,378 in validated net profit** while protecting margins through a predictive "GO/NO GO" audit.

---

## 🏗️ Technical Architecture & Key Features

### 1. High-Performance Engineering (Polars)
Unlike traditional Pandas-based pipelines, this project is architected with **Polars**.
* **Scalability:** Leveraging Lazy Evaluation and optimized memory management to handle massive datasets.
* **Efficiency:** Streamlined data processing from 33M transactions to structured behavioral indices.

### 2. Behavioral Persona Profiling (Clustering)
I moved beyond basic demographics to engineer complex behavioral features:
* **Proprietary Indices:** Developed the **HAI** (Healthy Affinity Index) and **PSI** (Price Sensitivity Index).
* **Robustness:** Segmentation validated via **Adjusted Rand Index (ARI)** to ensure cluster stability over time.

### 3. Stratified Association Rules (MBA)
Implemented a "Production-Ready" Market Basket Analysis:
* **Generalization:** Used a **User-level stratified Train/Test split** to ensure co-purchase patterns generalize to new customers.
* **Metrics:** Optimized via Support, Confidence, and Lift, focusing on high-value "Opportunity Scores."

### 4. The "Golden Basket" Strategy
Developed a strategic classification framework based on a **Diffusion-Fidelity Matrix**:
* **Product Roles:** Categorized the catalog into **Core** (pillars), **Niche** (loyalty drivers), and **Opportunistic** (impulse) products.
* **Personalized Assortment:** Designed the optimal product mix for each persona to maximize penetration and reorder rates.

### 5. Predictive Couponing Engine
* **Just-in-Time Triggering:** Calculated individual **repurchase cycles** per product.
* **Automated Scheduling:** Promotions are triggered at **80% of the consumption cycle** to capture intent precisely before stock exhaustion.

### 6. Value-Aware ROI Measurement
The ultimate layer of the project is a financial audit of the strategy:
* **Margin Protection:** Integrated departmental margins and a **0.7 cannibalization factor**.
* **Decision Logic:** An automated verdict system filters out unprofitable offers, shielding the retailer from promotional value destruction.

---

## 📊 Business Insights
* **Segment 0 (Premium Healths):** Inelastic to price, high HAI, driven by "Niche" organic products.
* **Segment 1 (Daily Economizers):** High frequency, high PSI, driven by "Core" staples and volume.
* **Validated Impact:** €5,378 incremental profit / €174 avoided losses (margin shield).

---

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NathanLeDev/Data-Driven-Retail-Insights-for-Cost-Savings-Revenue-Growth.git
   
2. **Install dependencies:**
   ```bash
   pip install polars pandas scikit-learn seaborn plotly streamlit
   ``` 
3. **Run the Streamlit app:**
   ```bash
    python -m streamlit run web_server/app.py
    ```
## 🛠️ Tech Stack
* Language: Python 3.10+
* Data Processing: Polars (LazyFrames), NumPy
* Machine Learning: Scikit-Learn (K-Means, StandardScaler)
* Visualization: Plotly, Seaborn, Matplotlib
* Environment: Jupyter Notebook / Streamlit

## 👤 Author
* **Nathan Goyer** - Data Scientist - [LinkedIn](https://www.linkedin.com/in/nathan-le-dev/)
* **Disha Srinivasa Chary** - Data Scientist
* **Armand Courvoisier** - Data Analyst
* **Ndifreke Charles** - Data Scientist
* **Jérémy Trochon** - Data Scientist
* **Harini Magudeswaran** - Data Analyst