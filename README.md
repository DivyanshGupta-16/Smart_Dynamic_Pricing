# 🚖 Smart Dynamic Pricing (Hybrid ML + RL)

A **hybrid machine learning + reinforcement learning system** for simulating and predicting **dynamic ride pricing**.  
The project combines **historical price estimation** (ML) with a **Q-learning agent** (RL) to adaptively adjust prices based on demand, supply, and customer loyalty.

---

## 📌 Features
- **Base Price Estimation**
  - Median-based estimator using historical rides (`base_price.py`).
  - Falls back from tight duration window → duration bins → vehicle-type median → global median.
- **Data Preprocessing**
  - Missing value handling.
  - Vehicle type encoding (`Economy → 0`, `Premium → 1`, `Luxury → 2`).
  - State construction from riders, drivers, and loyalty (`preprocessing.py`).
- **Feature Engineering**
  - Buckets riders → `Low`, `Medium`, `High`, `Very High`.
  - Buckets drivers → `Low`, `Medium`, `High`.
  - Loyalty proxy from vehicle type (`Regular`, `Silver`, `Gold`) (`utils.py`).
- **Reinforcement Learning**
  - `DynamicPricingEnv` simulates rides as episodes.
  - `QLearningAgent` learns the best price multiplier.
  - Multipliers: `[0.8×, 1.0×, 1.2×, 1.4×]` (`rl.py`).
- **Interactive Streamlit App**
  - Sidebar for user input (demand, supply, vehicle type, ride duration, base price).
  - Option to auto-estimate base price.
  - Shows RL-chosen multiplier and final price recommendation (`app.py`).

---

## 📂 Project Structure
project-root/
│── data/
│ └── dynamic_pricing.csv # dataset
│
│── src/
│ ├── base_price.py # base price estimation logic
│ ├── preprocessing.py # data preprocessing + state builder
│ ├── rl.py # environment + Q-learning agent
│ ├── utils.py # bucket creation helpers
│
│── app.py # Streamlit app
│── README.md # this file
│── requirements.txt # dependencies

yaml
Copy code

---

## 🖼️ Demo

Here are some screenshots of the Streamlit app in action:

### 🔹 Base Price
![Home Screenshot](assets\base_price_1x.png)

### 🔹 More Demand
![Sidebar Screenshot](assets\base_price_1-2x.png)

### 🔹 More Demand with Less Supply
![Prediction Screenshot](assets\base_price_1-4x.png)

### 🔹 Estimated Increase in Base Price due to more ride duration
![Details Screenshot](assets\estimated_base_price.png)

---

## ⚙️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/smart-dynamic-pricing.git
   cd smart-dynamic-pricing
Create a virtual environment and install dependencies:

bash
Copy code
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

pip install -r requirements.txt
Dependencies (requirements.txt):

shell
Copy code
numpy>=1.21
pandas>=1.3
streamlit>=1.20
🚀 Usage
Place your dataset in data/dynamic_pricing.csv.
The CSV should include at least:

javascript
Copy code
Number_of_Riders, Number_of_Drivers, Vehicle_Type, Expected_Ride_Duration, Historical_Cost_of_Ride
Run the Streamlit app:

bash
Copy code
streamlit run app.py
Use the sidebar to input:

Riders, Drivers

Vehicle type (Economy / Premium / Luxury)

Expected ride duration

Historical cost (optional if auto-estimation enabled)

View results:

Base price (ML estimator or manual input)

RL-chosen multiplier

Final recommended price

🧠 Methodology
ML (Supervised / Statistical):
Estimate base ride price from historical rides.

RL (Q-Learning):
Agent trains on bucketed states → learns best multiplier to maximize reward (= revenue - base cost).

Hybrid Prediction:
Final price = Base Price × RL Multiplier.

📊 Example Output
lua
Copy code
Base Price (input): ₹120.00
RL Multiplier: 1.20×
---------------------------------
💰 Final Recommended Price: ₹144.00
State = ('High', 'Medium', 'Silver')


✨ Built with Python, Streamlit, Numpy, Pandas, Reinforcement Learning