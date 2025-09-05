
# Dynamic Pricing Strategy — RL-based

This repository now exposes an **RL-based** Streamlit app: a Q-learning agent recommends a dynamic price multiplier based on demand/supply buckets.  
The previous Random Forest / MLP base models have been removed for simplicity.

## Project Structure

```
dynamic-pricing-strategy/
├── app.py
├── data/
│   └── dynamic_pricing.csv
├── src/
│   ├── preprocessing.py
│   ├── rl.py
│   └── utils.py
├── requirements.txt
└── README.md
```

## Quickstart

```bash
# 1) (Recommended) create a fresh virtual environment for Python 3.10–3.13
pip install -r requirements.txt

# 2) run the Streamlit app
streamlit run app.py
```

The app trains a **Q-learning** agent that outputs a price multiplier based on demand/supply buckets.  
Base price is taken from your input (Historical Ride Cost) in the sidebar.

## Dataset

For convenience, a small **synthetic** dataset is provided in `data/dynamic_pricing.csv`.  
You can replace it with your original Kaggle dataset (keeping these columns):

- `Number_of_Riders`  
- `Number_of_Drivers`  
- `Vehicle_Type` in `{Economy, Premium, Luxury}`  
- `Expected_Ride_Duration`  
- `Historical_Cost_of_Ride`

## Notes

- The RL environment is a lightweight episodic simulator aligned with the report’s Appendix I.
- The app is self-contained and should run out-of-the-box without external downloads.

## Screenshots

Add your screenshots (from the original report) or capture new ones while using the app.

---
Rebuilt for portfolio/GitHub use. ✨
