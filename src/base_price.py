import numpy as np
import pandas as pd


def estimate_base_price(df: pd.DataFrame, vehicle_type: str, duration_min: int, window: int = 5) -> float:

    lo = max(0, int(duration_min) - int(window))
    hi = int(duration_min) + int(window)
    m1_series = df[(df["Vehicle_Type"] == vehicle_type) & (df["Expected_Ride_Duration"].between(lo, hi))][
        "Historical_Cost_of_Ride"
    ]
    m1 = float(np.median(np.asarray(m1_series, dtype=float))) if len(m1_series) else np.nan
    if not np.isnan(m1):
        return float(m1)

    df2 = df.copy()
    df2["duration_bin"] = (df2["Expected_Ride_Duration"] // 10) * 10
    target_bin = (int(duration_min) // 10) * 10
    m2_series = df2[(df2["Vehicle_Type"] == vehicle_type) & (df2["duration_bin"] == target_bin)][
        "Historical_Cost_of_Ride"
    ]
    m2 = float(np.median(np.asarray(m2_series, dtype=float))) if len(m2_series) else np.nan
    if not np.isnan(m2):
        return float(m2)

    m3_series = df[df["Vehicle_Type"] == vehicle_type]["Historical_Cost_of_Ride"]
    m3 = float(np.median(np.asarray(m3_series, dtype=float))) if len(m3_series) else np.nan
    if not np.isnan(m3):
        return float(m3)

    return float(np.median(np.asarray(df["Historical_Cost_of_Ride"], dtype=float)))


