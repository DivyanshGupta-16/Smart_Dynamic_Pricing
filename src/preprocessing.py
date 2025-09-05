
import pandas as pd
import numpy as np

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()

    numeric_features = data.select_dtypes(include=["float", "int"]).columns
    if len(numeric_features) > 0:
        data[numeric_features] = data[numeric_features].fillna(data[numeric_features].mean())

    categorical_features = data.select_dtypes(include=["object"]).columns
    if len(categorical_features) > 0:
        data[categorical_features] = data[categorical_features].fillna(
            data[categorical_features].mode().iloc[0]
        )

    # Encode Vehicle_Type as in the report
    if "Vehicle_Type" in data.columns:
        data["Vehicle_Type"] = data["Vehicle_Type"].replace({"Economy": 0, "Premium": 1, "Luxury": 2})

    return data

def make_state_from_inputs(num_riders: int, num_drivers: int, vehicle_type_numeric: int):
    # Bucketing like in the report's appendix
    if num_riders <= 30:
        demand = "Low"
    elif num_riders <= 60:
        demand = "Medium"
    elif num_riders <= 90:
        demand = "High"
    else:
        demand = "Very High"

    if num_drivers <= 15:
        supply = "Low"
    elif num_drivers <= 30:
        supply = "Medium"
    else:
        supply = "High"

    # Derive a simple loyalty-like proxy from vehicle tier
    loyalty = "Regular" if vehicle_type_numeric == 0 else ("Silver" if vehicle_type_numeric == 1 else "Gold")
    return (demand, supply, loyalty)
