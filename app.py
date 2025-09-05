
import numpy as np
import streamlit as st

from src.preprocessing import load_data, preprocess, make_state_from_inputs
from src.rl import DynamicPricingEnv, train_q_agent
from src.base_price import estimate_base_price
from src.utils import add_buckets

st.set_page_config(page_title="Smart Dynamic Pricing (Hybrid ML + RL)", page_icon="🚖", layout="centered")

st.title("🚖 Smart Dynamic Pricing Predictor (Hybrid ML + RL)")
st.caption("Reconstructed from project report — Random Forest baseline + optional MLP + Q-Learning for adaptive multiplier.")

@st.cache_data(show_spinner=False)
def get_dataset():
    df = load_data("data/dynamic_pricing.csv")
    return df

@st.cache_data(show_spinner=False)
def get_processed_dataset():
    df = get_dataset()
    processed = preprocess(df)
    with_buckets = add_buckets(processed)
    return processed, with_buckets

@st.cache_resource(show_spinner=False)
def train_agent():
    _, with_buckets = get_processed_dataset()
    env = DynamicPricingEnv(with_buckets)
    agent = train_q_agent(env, episodes=25)
    return agent

# Sidebar
with st.sidebar:
    st.header("Inputs")
    riders = st.slider("Number of Riders (demand)", 0, 150, 85, 1)
    drivers = st.slider("Number of Drivers (supply)", 0, 100, 20, 1)
    vt = st.selectbox("Vehicle Type", ["Economy", "Premium", "Luxury"])
    duration = st.number_input("Expected Ride Duration (minutes)", min_value=0, value=25, step=1)
    hist_cost = st.number_input("Historical Ride Cost (₹)", min_value=0.0, value=120.0, step=1.0)
    use_estimator = st.toggle("Auto-estimate base price from history", value=True)

    st.caption("Base price uses your Historical Ride Cost; RL provides the multiplier.")

vehicle_to_num = {"Economy": 0, "Premium": 1, "Luxury": 2}
vt_num = vehicle_to_num[vt]

q_agent = train_agent()

if use_estimator:
    df_raw = get_dataset()
    base_price = estimate_base_price(df_raw, vt, int(duration))
else:
    base_price = float(hist_cost)

# RL state & multiplier
state = make_state_from_inputs(riders, drivers, vt_num)
# safe lookup for unseen states
q_row = q_agent.q.get(state)
if q_row is None:
    # fallback: assume neutral multiplier
    recommended_multiplier = 1.0
else:
    best_idx = int(np.argmax(q_row))
    # Use the static action list since we know the actions are [0.8, 1.0, 1.2, 1.4]
    recommended_multiplier = [0.8, 1.0, 1.2, 1.4][best_idx]

final_price = base_price * recommended_multiplier

st.subheader("📈 Prediction")
c1, c2 = st.columns(2)
with c1:
    st.metric("Base Price (input)", f"₹{base_price:,.2f}")
with c2:
    st.metric("RL Multiplier", f"{recommended_multiplier:.2f}×")

st.success(f"💰 Final Recommended Price: **₹{final_price:,.2f}**")
st.caption(f"State = {state}")

with st.expander("ℹ️ Details"):
    source = "historical estimator" if use_estimator else "manual input"
    st.write(f"Base price from {source}; multiplier from Q-learning policy trained over bucketed demand/supply states.")


