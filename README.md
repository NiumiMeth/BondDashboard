# BondDashboard

> **Treasury Risk Intelligence Dashboard**

**Live Dashboard:** [https://bondanalyticsdashboard.streamlit.app/](https://bondanalyticsdashboard.streamlit.app/)

BondDashboard is a comprehensive Streamlit-powered dashboard for treasury and bond portfolio management. It provides analytics, risk assessment, liquidity analysis, yield curve monitoring, and actionable recommendations for decision intelligence.

## Key Features

- **Portfolio Overview:** Upload or manually enter your bond portfolio. View key metrics like total market value, weighted yield, duration, DV01, and convexity.
- **Interest Rate Risk Engine:** Simulate rate shocks and stress test your portfolio. Visualize potential gains/losses and risk levels under different interest rate scenarios.
- **Liquidity Ladder:** Analyze cash inflows by maturity buckets to assess liquidity risk and plan for upcoming obligations.
- **Yield Curve Monitor:** Input or upload yield curve data. Visualize the curve, detect steepening/flattening, and monitor spread changes.
- **Decision Intelligence Layer:** Get system-generated recommendations based on portfolio metrics and yield curve trends. Supports scenario analysis for strategic decision-making.

## How It Works

- The dashboard is built with Streamlit for interactive web-based analytics.
- Users can upload CSV files or manually input bond data for each module.
- Portfolio metrics are calculated using custom risk and analytics engines.
- Visualizations are provided for yield curves, liquidity ladders, and stress test results.
- Recommendations are generated based on risk metrics and market conditions.

## Project Structure

```
BondDashboard/
│   app.py           # Main Streamlit dashboard
│   forecasting.py   # Yield curve analytics and forecasting
│   liquidity.py     # Liquidity ladder analysis
│   risk_engine.py   # Portfolio metrics and rate shock simulation
│   utils.py         # Utility functions
│   README.md        # Project documentation
│   .gitignore       # Git ignore rules
│   __pycache__/     # Python cache files
```

## Setup Instructions

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd BondDashboard
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the dashboard**
   ```sh
   streamlit run app.py
   ```

## Module Descriptions

- **app.py:** Orchestrates the dashboard UI and navigation. Handles user input, file uploads, and displays analytics for each module.
- **forecasting.py:** Provides yield curve visualization and steepening/flattening detection.
- **liquidity.py:** Calculates maturity buckets and cash inflows for liquidity risk analysis.
- **risk_engine.py:** Computes portfolio metrics (market value, yield, duration, DV01, convexity) and simulates rate shocks for stress testing.
- **utils.py:** Placeholder for additional utility functions.

## User Guidance

- Use the sidebar to navigate between modules.
- Upload CSV files or manually enter data as prompted.
- Review metrics, charts, and recommendations for actionable insights.
- All calculations are performed locally; no data is sent to external servers.

## License
This project is licensed under the MIT License.
