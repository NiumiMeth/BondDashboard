import pandas as pd

def build_liquidity_ladder(bonds_df):
    # Convert Maturity to datetime
    bonds_df["Maturity"] = pd.to_datetime(bonds_df["Maturity"])
    now = pd.Timestamp.today()
    buckets = {
        "0–30 days": (now, now + pd.Timedelta(days=30)),
        "30–90 days": (now + pd.Timedelta(days=30), now + pd.Timedelta(days=90)),
        "90–180 days": (now + pd.Timedelta(days=90), now + pd.Timedelta(days=180)),
        "1 year+": (now + pd.Timedelta(days=180), None)
    }
    ladder = {}
    for bucket, (start, end) in buckets.items():
        if end:
            mask = (bonds_df["Maturity"] >= start) & (bonds_df["Maturity"] < end)
        else:
            mask = (bonds_df["Maturity"] >= start)
        ladder[bucket] = bonds_df.loc[mask, "Market Value"].sum()
    return ladder
