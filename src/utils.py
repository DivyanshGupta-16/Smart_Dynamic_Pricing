
import pandas as pd

def add_buckets(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["Demand_Level"] = pd.cut(out["Number_of_Riders"], bins=[-1, 30, 60, 90, 10_000],
                                 labels=["Low", "Medium", "High", "Very High"])
    out["Supply_Level"] = pd.cut(out["Number_of_Drivers"], bins=[-1, 15, 30, 10_000],
                                 labels=["Low", "Medium", "High"])

    # simple derived customer status (proxy)
    vt_to_status = {0: "Regular", 1: "Silver", 2: "Gold"}
    if "Vehicle_Type" in out.columns:
        out["Customer_Loyalty_Status"] = out["Vehicle_Type"].replace(vt_to_status)
    else:
        out["Customer_Loyalty_Status"] = "Regular"
    return out
