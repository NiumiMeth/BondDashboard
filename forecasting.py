import pandas as pd
import numpy as np
import statsmodels.api as sm

def yield_curve_monitor(yields):
    import plotly.graph_objs as go
    tenors = ["3M", "6M", "1Y", "2Y", "5Y", "10Y"]
    curve = [yields.get(t, None) for t in tenors]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tenors, y=curve, mode="lines+markers", name="Yield Curve"))
    # Detect steepening/flattening
    slope_short = curve[2] - curve[0] if curve[2] and curve[0] else None
    slope_long = curve[-1] - curve[2] if curve[-1] and curve[2] else None
    steepening = slope_long > slope_short if slope_long and slope_short else None
    spread_changes = {f"{tenors[i]}-{tenors[j]}": curve[i] - curve[j] if curve[i] and curve[j] else None for i, j in [(5, 0), (4, 2)]}
    return fig, steepening, spread_changes
