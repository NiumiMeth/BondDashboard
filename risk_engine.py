import pandas as pd
import numpy as np

def calculate_portfolio_metrics(bonds_df):
    total_market_value = bonds_df["Market Value"].sum()
    weighted_yield = np.average(bonds_df["Yield"], weights=bonds_df["Market Value"])
    weighted_duration = np.average(bonds_df["Duration"], weights=bonds_df["Market Value"])
    # DV01: Dollar value of 1bp change in yield
    dv01 = total_market_value * weighted_duration * 0.0001
    # Convexity placeholder (can be expanded)
    convexity = np.average(bonds_df.get("Convexity", pd.Series([0]*len(bonds_df))), weights=bonds_df["Market Value"])
    return {
        "Total Market Value": total_market_value,
        "Weighted Yield": weighted_yield,
        "Weighted Duration": weighted_duration,
        "DV01": dv01,
        "Convexity": convexity
    }

def simulate_rate_shocks(bonds_df, shocks):
    results = []
    for shock in shocks:
        # Price change approximation: -Duration * Market Value * Shock
        weighted_duration = np.average(bonds_df["Duration"], weights=bonds_df["Market Value"])
        total_market_value = bonds_df["Market Value"].sum()
        dv01 = total_market_value * weighted_duration * 0.0001
        # Portfolio value change for shock (in %)
        value_change = -weighted_duration * total_market_value * (shock / 100)
        pct_impact = value_change / total_market_value * 100
        # Risk classification
        if abs(pct_impact) < 1:
            risk = "Low"
        elif abs(pct_impact) < 3:
            risk = "Moderate"
        else:
            risk = "High"
        results.append({
            "Shock": f"{shock:+.1f}%",
            "Gain/Loss": value_change,
            "% Impact": pct_impact,
            "Risk": risk
        })
    return results
