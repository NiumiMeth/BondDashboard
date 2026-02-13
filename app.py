
import streamlit as st
import pandas as pd
from risk_engine import calculate_portfolio_metrics, simulate_rate_shocks
from streamlit_option_menu import option_menu

# Ensure bonds_df is always defined
bonds_df = None

st.set_page_config(page_title="Treasury Risk Intelligence Dashboard", layout="wide")
st.title("🏦 Treasury Risk Intelligence Dashboard")


# --- Custom CSS for professional look and collapsible sidebar ---
st.markdown("""
	<style>
	/* Smaller sidebar font and padding */
	.css-1d391kg, .css-1v0mbdj, .css-1cypcdb, .css-1lcbmhc, .css-1n76uvr, .css-1v3fvcr, .css-1oe5cao {
		font-size: 13px !important;
		padding: 0.3rem 0.5rem !important;
	}
	/* Option menu icon size */
	.iconify { font-size: 1.1em !important; }
	/* Hide default Streamlit hamburger and footer */
	#MainMenu {visibility: hidden;}
	footer {visibility: hidden;}
	/* Collapsible sidebar button */
	.sidebar-toggle { position: absolute; top: 10px; right: -18px; background: #222; color: #fff; border-radius: 0 5px 5px 0; padding: 2px 8px; cursor: pointer; z-index: 1000; font-size: 18px; }
	.sidebar-collapsed { width: 0 !important; min-width: 0 !important; overflow: hidden !important; }
	</style>
	<script>
	// Collapsible sidebar JS
	window.addEventListener('DOMContentLoaded', function() {
		let sidebar = window.parent.document.querySelector('.css-1lcbmhc, .css-1d391kg, .css-1v0mbdj, .css-1cypcdb, .css-1n76uvr, .css-1v3fvcr, .css-1oe5cao');
		if (sidebar && !window.sidebarToggleAdded) {
			let btn = document.createElement('div');
			btn.innerHTML = sidebar.offsetWidth > 50 ? '⏴' : '⏵';
			btn.className = 'sidebar-toggle';
			btn.onclick = function() {
				if (sidebar.classList.contains('sidebar-collapsed')) {
					sidebar.classList.remove('sidebar-collapsed');
					btn.innerHTML = '⏴';
				} else {
					sidebar.classList.add('sidebar-collapsed');
					btn.innerHTML = '⏵';
				}
			};
			sidebar.appendChild(btn);
			window.sidebarToggleAdded = true;
		}
	});
	</script>
""", unsafe_allow_html=True)

# Professional sidebar navigation with icons
with st.sidebar:
	st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=40)
	selected = option_menu(
		"Navigation",
		["Portfolio Overview", "Interest Rate Risk Engine", "Liquidity Ladder", "Yield Curve Monitor", "Decision Intelligence Layer"],
		icons=["bar-chart", "activity", "calendar3", "graph-up", "lightbulb"],
		menu_icon="cast",
		default_index=0,
		orientation="vertical"
	)

if selected == "Portfolio Overview":
	st.header("Portfolio Overview")
	st.subheader("Portfolio Input")
	uploaded_file = st.file_uploader("Upload Portfolio CSV", type=["csv"], key="portfolio_upload")
	bonds_df = None
	if uploaded_file:
		bonds_df = pd.read_csv(uploaded_file)
		st.success("Portfolio loaded from CSV.")
	st.markdown("**Or enter bonds manually:**")
	with st.expander("Manual Entry"):
		manual_data = st.text_area(
			"Enter bond data (ISIN, Maturity, Coupon, Yield, Market Value, Duration)",
			"US1234567890,2027-06-15,2.5,2.7,1000000,4.2\nUS0987654321,2029-12-01,3.0,3.1,500000,6.1",
			key="portfolio_manual"
		)
		if manual_data:
			import io
			bonds_df = pd.read_csv(io.StringIO(manual_data),
								  names=["ISIN", "Maturity", "Coupon", "Yield", "Market Value", "Duration"])
			st.success("Portfolio loaded from manual entry.")
	if bonds_df is not None:
		# Robust column normalization
		rename_map = {
			'isin': 'ISIN',
			'maturity': 'Maturity',
			'coupon': 'Coupon',
			'yield': 'Yield',
			'market value': 'Market Value',
			'market_value': 'Market Value',
			'value': 'Market Value',
			'marketvalue': 'Market Value',
			'duration': 'Duration',
		}
		bonds_df.columns = [rename_map.get(str(c).strip().lower().replace('_','').replace(' ','').replace('-',''), c) for c in bonds_df.columns]
		st.dataframe(bonds_df)
		required_cols = ["ISIN", "Maturity", "Coupon", "Yield", "Market Value", "Duration"]
		missing = [col for col in required_cols if col not in bonds_df.columns]
		if missing:
			st.error(f"Missing required columns: {', '.join(missing)}. Please check your data headers.")
		else:
			metrics = calculate_portfolio_metrics(bonds_df)
			st.subheader("Portfolio Metrics")
			st.write({
				"Total Market Value": f"${metrics['Total Market Value']:,.2f}",
				"Weighted Yield": f"{metrics['Weighted Yield']:.2f}%",
				"Weighted Duration": f"{metrics['Weighted Duration']:.2f}",
				"DV01": f"${metrics['DV01']:,.2f}",
				"Convexity": f"{metrics['Convexity']:.4f}"
			})
		missing = [col for col in required_cols if col not in bonds_df.columns]
		if missing:
			st.error(f"Missing required columns: {', '.join(missing)}. Please check your data headers.")
		else:
			metrics = calculate_portfolio_metrics(bonds_df)
			st.subheader("Portfolio Metrics")
			st.write({
				"Total Market Value": f"${metrics['Total Market Value']:,.2f}",
				"Weighted Yield": f"{metrics['Weighted Yield']:.2f}%",
				"Weighted Duration": f"{metrics['Weighted Duration']:.2f}",
				"DV01": f"${metrics['DV01']:,.2f}",
				"Convexity": f"{metrics['Convexity']:.4f}"
			})

elif selected == "Interest Rate Risk Engine":
	st.header("Interest Rate Risk Engine")
	st.subheader("Rate Shock Simulation")
	uploaded_file = st.file_uploader("Upload Portfolio CSV", type=["csv"], key="risk_engine_upload")
	bonds_df = None
	if uploaded_file:
		bonds_df = pd.read_csv(uploaded_file)
		st.success("Portfolio loaded from CSV.")
	st.markdown("**Or enter bonds manually:**")
	with st.expander("Manual Entry"):
		manual_data = st.text_area(
			"Enter bond data (ISIN, Maturity, Coupon, Yield, Market Value, Duration)",
			"US1234567890,2027-06-15,2.5,2.7,1000000,4.2\nUS0987654321,2029-12-01,3.0,3.1,500000,6.1",
			key="risk_engine_manual"
		)
		if manual_data:
			import io
			bonds_df = pd.read_csv(io.StringIO(manual_data),
								  names=["ISIN", "Maturity", "Coupon", "Yield", "Market Value", "Duration"])
			st.success("Portfolio loaded from manual entry.")
	if bonds_df is not None:
		shocks = st.multiselect(
			"Select rate shocks (%)",
			options=[-2, -1, 1, 2],
			default=[-2, -1, 1, 2]
		)
		if shocks:
	# --- Interest Rate Risk Engine ---
			results = simulate_rate_shocks(bonds_df, shocks)
			st.write("Stress Test Results:")
			st.dataframe(pd.DataFrame(results))

elif selected == "Liquidity Ladder":
	st.header("Liquidity Ladder")
	uploaded_file = st.file_uploader("Upload Portfolio CSV", type=["csv"], key="liquidity_upload")
	bonds_df = None
	if uploaded_file:
		bonds_df = pd.read_csv(uploaded_file)
		st.success("Portfolio loaded from CSV.")
	st.markdown("**Or enter bonds manually:**")
	with st.expander("Manual Entry"):
		manual_data = st.text_area(
			"Enter bond data (ISIN, Maturity, Coupon, Yield, Market Value, Duration)",
			"US1234567890,2027-06-15,2.5,2.7,1000000,4.2\nUS0987654321,2029-12-01,3.0,3.1,500000,6.1",
	# --- Liquidity Ladder ---
			key="liquidity_manual"
		)
		if manual_data:
			import io
			bonds_df = pd.read_csv(io.StringIO(manual_data),
								  names=["ISIN", "Maturity", "Coupon", "Yield", "Market Value", "Duration"])
			st.success("Portfolio loaded from manual entry.")
	if bonds_df is not None:
		from liquidity import build_liquidity_ladder
		ladder = build_liquidity_ladder(bonds_df)
		st.write("Maturity Ladder (Cash Inflows):")
	# --- Yield Curve Monitor ---
		st.table({k: f"${v:,.2f}" for k, v in ladder.items()})

elif selected == "Yield Curve Monitor":
	st.header("Yield Curve Monitor")
	mode = st.selectbox("Yield Curve Input Mode", ["CSV Upload", "Manual"], key="yield_mode")
	tenors = ["3M", "6M", "1Y", "2Y", "5Y", "10Y"]
	yield_inputs = {}
	if mode == "CSV Upload":
		st.info("Upload a CSV file with columns: Tenor,Yield. Example rows: 3M,5.2")
		uploaded_file = st.file_uploader("Upload Yield Curve CSV", type=["csv"], key="yieldcurve_csv")
		if uploaded_file:
			import pandas as pd
			df = pd.read_csv(uploaded_file)
			for tenor in tenors:
				val = df[df['Tenor'].str.upper() == tenor.upper()]['Yield']
				yield_inputs[tenor] = float(val.values[0]) if not val.empty else 0.0
			st.success("Loaded yield curve from CSV.")
		else:
			for tenor in tenors:
				yield_inputs[tenor] = 0.0
	else:
		cols = st.columns(len(tenors))
		for i, tenor in enumerate(tenors):
			yield_inputs[tenor] = cols[i].number_input(f"{tenor}", min_value=0.0, max_value=20.0, value=0.0, step=0.01)
	# Only show chart if at least one yield is entered (not all zero)
	if any(y > 0 for y in yield_inputs.values()):
		from forecasting import yield_curve_monitor
		fig, steepening, spread_changes = yield_curve_monitor(yield_inputs)
	# --- Decision Intelligence Layer ---
		st.plotly_chart(fig)
		st.write("Spread Changes:", spread_changes)
		if steepening is not None:
			st.write(f"Curve Steepening Detected: {steepening}")

elif selected == "Decision Intelligence Layer":
	st.header("Decision Intelligence Layer")
	uploaded_file = st.file_uploader("Upload Portfolio CSV", type=["csv"], key="decision_upload")
	bonds_df = None
	if uploaded_file:
		bonds_df = pd.read_csv(uploaded_file)
		st.success("Portfolio loaded from CSV.")
	st.markdown("**Or enter bonds manually:**")
	with st.expander("Manual Entry"):
		manual_data = st.text_area(
			"Enter bond data (ISIN, Maturity, Coupon, Yield, Market Value, Duration)",
			"US1234567890,2027-06-15,2.5,2.7,1000000,4.2\nUS0987654321,2029-12-01,3.0,3.1,500000,6.1",
			key="decision_manual"
		)
		if manual_data:
			import io
			bonds_df = pd.read_csv(io.StringIO(manual_data),
								  names=["ISIN", "Maturity", "Coupon", "Yield", "Market Value", "Duration"])
			st.success("Portfolio loaded from manual entry.")
	if bonds_df is not None:
		metrics = calculate_portfolio_metrics(bonds_df)
		recs = []
		if metrics['Weighted Duration'] > 5:
			recs.append(f"Portfolio duration is high ({metrics['Weighted Duration']:.2f}). If rates rise 1%, estimated loss = {metrics['DV01']*100:.2f}. Consider reducing long maturity exposure.")
		if metrics['Weighted Yield'] < 2:
			recs.append("Portfolio yield is low. Consider increasing exposure to higher-yielding assets.")
		tenors = ["3M", "6M", "1Y", "2Y", "5Y", "10Y"]
		yield_inputs = {}
		cols = st.columns(len(tenors))
		for i, tenor in enumerate(tenors):
			yield_inputs[tenor] = cols[i].number_input(f"{tenor}", min_value=0.0, max_value=20.0, value=0.0, step=0.01, key=f"decision_{tenor}")
		if any(y > 0 for y in yield_inputs.values()):
			from forecasting import yield_curve_monitor
			_, steepening, _ = yield_curve_monitor(yield_inputs)
			if steepening:
				recs.append("Yield curve steepening detected. Long bonds may outperform if rate cuts expected.")
			else:
				recs.append("Yield curve flattening detected. Consider short duration positioning.")
		st.subheader("System Recommendations")
		for r in recs:
			st.write(f"- {r}")
		if not recs:
			st.write("No actionable recommendations at this time.")
if bonds_df is not None:
	metrics = calculate_portfolio_metrics(bonds_df)
	# Example recommendations
	recs = []
	if metrics['Weighted Duration'] > 5:
		recs.append(f"Portfolio duration is high ({metrics['Weighted Duration']:.2f}). If rates rise 1%, estimated loss = {metrics['DV01']*100:.2f}. Consider reducing long maturity exposure.")
	if metrics['Weighted Yield'] < 2:
		recs.append("Portfolio yield is low. Consider increasing exposure to higher-yielding assets.")
	# Yield curve logic
	if 'yield_inputs' in locals() and any(y > 0 for y in yield_inputs.values()):
		from forecasting import yield_curve_monitor
		_, steepening, _ = yield_curve_monitor(yield_inputs)
		if steepening:
			recs.append("Yield curve steepening detected. Long bonds may outperform if rate cuts expected.")
		else:
			recs.append("Yield curve flattening detected. Consider short duration positioning.")
	if recs:
		st.subheader("System Recommendations")
		for r in recs:
			st.write(f"- {r}")
	else:
		st.write("No actionable recommendations at this time.")
# More modules will be added as we build

st.header("Yield Curve Monitor")
st.subheader("Input Current Yields")
yield_inputs = {}
tenors = ["3M", "6M", "1Y", "2Y", "5Y", "10Y"]
cols = st.columns(len(tenors))
for i, tenor in enumerate(tenors):
	yield_inputs[tenor] = cols[i].number_input(f"{tenor}", min_value=0.0, max_value=20.0, value=0.0, step=0.01)

if any(y > 0 for y in yield_inputs.values()):
	from forecasting import yield_curve_monitor
	fig, steepening, spread_changes = yield_curve_monitor(yield_inputs)
	st.plotly_chart(fig)
	st.write("Spread Changes:", spread_changes)
	if steepening is not None:
		st.write(f"Curve Steepening Detected: {steepening}")
# More modules will be added as we build

st.header("Liquidity Ladder")
if bonds_df is not None:
	from liquidity import build_liquidity_ladder
	ladder = build_liquidity_ladder(bonds_df)
	st.write("Maturity Ladder (Cash Inflows):")
	st.table({k: f"${v:,.2f}" for k, v in ladder.items()})
import streamlit as st
from risk_engine import calculate_portfolio_metrics, simulate_rate_shocks

st.set_page_config(page_title="Treasury Risk Intelligence Dashboard", layout="wide")
st.title("🏦 Treasury Risk Intelligence Dashboard")

st.header("Portfolio Overview")
st.subheader("Portfolio Input")

# CSV upload
uploaded_file = st.file_uploader("Upload Portfolio CSV", type=["csv"])
bonds_df = None
if uploaded_file:
	bonds_df = pd.read_csv(uploaded_file)
	st.success("Portfolio loaded from CSV.")

# Manual entry
st.markdown("**Or enter bonds manually:**")
with st.expander("Manual Entry"):
	manual_data = st.text_area(
		"Enter bond data (ISIN, Maturity, Coupon, Yield, Market Value, Duration)",
		"US1234567890,2027-06-15,2.5,2.7,1000000,4.2\nUS0987654321,2029-12-01,3.0,3.1,500000,6.1"
	)
	if manual_data:
		import io
		bonds_df = pd.read_csv(io.StringIO(manual_data),
							  names=["ISIN", "Maturity", "Coupon", "Yield", "Market Value", "Duration"])
		st.success("Portfolio loaded from manual entry.")

if bonds_df is not None:
	st.dataframe(bonds_df)
	metrics = calculate_portfolio_metrics(bonds_df)
	st.subheader("Portfolio Metrics")
	st.write({
		"Total Market Value": f"${metrics['Total Market Value']:,.2f}",
		"Weighted Yield": f"{metrics['Weighted Yield']:.2f}%",
		"Weighted Duration": f"{metrics['Weighted Duration']:.2f}",
		"DV01": f"${metrics['DV01']:,.2f}",
		"Convexity": f"{metrics['Convexity']:.4f}"
	})

st.header("Interest Rate Risk Engine")

st.subheader("Rate Shock Simulation")
if bonds_df is not None:
	shocks = st.multiselect(
		"Select rate shocks (%)",
		options=[-2, -1, 1, 2],
		default=[-2, -1, 1, 2]
	)
	if shocks:
		results = simulate_rate_shocks(bonds_df, shocks)
		st.write("Stress Test Results:")
		st.dataframe(pd.DataFrame(results))

# More modules will be added as we build
