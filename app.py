import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Commercial Pricing and Scenario Simulator", layout="wide")

st.title("Commercial Pricing and Scenario Simulator")
st.caption("Model pricing, volume, discount, and cost trade-offs to support commercial decisions.")

# ----------------------------
# Sidebar inputs
# ----------------------------
st.sidebar.header("Commercial Assumptions")

scenario_name = st.sidebar.text_input("Scenario Name", value="Base Case")
price = st.sidebar.number_input("Selling Price per Unit (€)", min_value=0.0, value=50.0, step=1.0)
volume = st.sidebar.number_input("Expected Units Sold", min_value=0, value=5000, step=100)
variable_cost = st.sidebar.number_input("Variable Cost per Unit (€)", min_value=0.0, value=25.0, step=1.0)
fixed_cost = st.sidebar.number_input("Fixed Cost (€)", min_value=0.0, value=50000.0, step=1000.0)
discount = st.sidebar.slider("Discount (%)", min_value=0, max_value=50, value=10)
marketing_spend = st.sidebar.number_input("Marketing Spend (€)", min_value=0.0, value=10000.0, step=1000.0)
growth = st.sidebar.slider("Demand Growth (%)", min_value=-50, max_value=100, value=0)

# ----------------------------
# Core calculations
# ----------------------------
adjusted_price = price * (1 - discount / 100)
adjusted_volume = int(volume * (1 + growth / 100))

revenue = adjusted_price * adjusted_volume
total_variable_cost = variable_cost * adjusted_volume
total_cost = total_variable_cost + fixed_cost + marketing_spend
gross_profit = revenue - total_variable_cost
net_profit = revenue - total_cost
profit_margin = (net_profit / revenue * 100) if revenue > 0 else 0.0

contribution_per_unit = adjusted_price - variable_cost
break_even_units = (
    (fixed_cost + marketing_spend) / contribution_per_unit
    if contribution_per_unit > 0 else None
)

# ----------------------------
# Executive summary
# ----------------------------
st.subheader("Executive Summary")

k1, k2, k3 = st.columns(3)
k1.metric("Revenue", f"€{revenue:,.0f}")
k2.metric("Gross Profit", f"€{gross_profit:,.0f}")
k3.metric("Net Profit", f"€{net_profit:,.0f}")

k4, k5, k6 = st.columns(3)
k4.metric("Profit Margin", f"{profit_margin:.1f}%")
k5.metric("Adjusted Price", f"€{adjusted_price:,.2f}")
k6.metric("Adjusted Volume", f"{adjusted_volume:,}")

if break_even_units is not None:
    st.info(f"Break-even volume: {break_even_units:,.0f} units")
else:
    st.warning("Break-even cannot be calculated because contribution per unit is zero or negative.")

# ----------------------------
# Business insight
# ----------------------------
st.subheader("Decision Guidance")

if profit_margin >= 25:
    st.success("Healthy commercial position. This scenario supports growth, reinvestment, or expansion decisions.")
elif profit_margin >= 10:
    st.warning("Profitable but moderate. This scenario may work, though pricing discipline or cost control would improve resilience.")
else:
    st.error("Commercially weak scenario. Revisit price, variable cost, discounting, or expected demand before committing.")

# ----------------------------
# Scenario snapshot table
# ----------------------------
st.subheader("Scenario Snapshot")

snapshot = pd.DataFrame([{
    "Scenario": scenario_name,
    "Base Price (€)": price,
    "Discount (%)": discount,
    "Adjusted Price (€)": adjusted_price,
    "Base Volume": volume,
    "Adjusted Volume": adjusted_volume,
    "Variable Cost per Unit (€)": variable_cost,
    "Fixed Cost (€)": fixed_cost,
    "Marketing Spend (€)": marketing_spend,
    "Revenue (€)": revenue,
    "Gross Profit (€)": gross_profit,
    "Net Profit (€)": net_profit,
    "Profit Margin (%)": profit_margin,
    "Break-even Units": break_even_units if break_even_units is not None else "N/A"
}])

st.dataframe(snapshot, use_container_width=True)

# ----------------------------
# Price sensitivity analysis
# ----------------------------
st.subheader("Net Profit by Price")

price_range = list(range(max(1, int(price * 0.6)), int(price * 1.4) + 1, 2))
profit_values = []

for p in price_range:
    test_adjusted_price = p * (1 - discount / 100)
    test_revenue = test_adjusted_price * adjusted_volume
    test_total_variable_cost = variable_cost * adjusted_volume
    test_total_cost = test_total_variable_cost + fixed_cost + marketing_spend
    test_profit = test_revenue - test_total_cost
    profit_values.append(test_profit)

price_df = pd.DataFrame({
    "Price": price_range,
    "Net Profit": profit_values
})

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(price_df["Price"], price_df["Net Profit"], marker="o")
ax1.set_xlabel("Base Price (€)")
ax1.set_ylabel("Net Profit (€)")
ax1.set_title("Net Profit vs Price")
ax1.grid(True)
st.pyplot(fig1)

# ----------------------------
# Volume sensitivity analysis
# ----------------------------
st.subheader("Revenue and Net Profit by Volume")

step_size = max(100, int(volume * 0.05)) if volume > 0 else 100
volume_range = list(range(max(100, int(volume * 0.5)), int(volume * 1.5) + 1, step_size))

revenue_values = []
profit_by_volume = []

for v in volume_range:
    test_adjusted_volume = int(v * (1 + growth / 100))
    test_revenue = adjusted_price * test_adjusted_volume
    test_total_variable_cost = variable_cost * test_adjusted_volume
    test_total_cost = test_total_variable_cost + fixed_cost + marketing_spend
    test_profit = test_revenue - test_total_cost

    revenue_values.append(test_revenue)
    profit_by_volume.append(test_profit)

volume_df = pd.DataFrame({
    "Volume": volume_range,
    "Revenue": revenue_values,
    "Net Profit": profit_by_volume
})

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(volume_df["Volume"], volume_df["Revenue"], marker="o", label="Revenue")
ax2.plot(volume_df["Volume"], volume_df["Net Profit"], marker="o", label="Net Profit")
ax2.set_xlabel("Base Volume")
ax2.set_ylabel("€")
ax2.set_title("Revenue and Net Profit by Volume")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

# ----------------------------
# Scenario comparison
# ----------------------------
st.subheader("Scenario Comparison")

base_price = adjusted_price
base_volume = adjusted_volume
base_revenue = revenue
base_profit = net_profit
base_margin = profit_margin

best_price = price * 1.05
best_volume = int(volume * 1.15)
best_revenue = best_price * best_volume
best_profit = best_revenue - (variable_cost * best_volume + fixed_cost + marketing_spend)
best_margin = (best_profit / best_revenue * 100) if best_revenue > 0 else 0.0

worst_price = price * 0.90
worst_volume = int(volume * 0.80)
worst_revenue = worst_price * worst_volume
worst_profit = worst_revenue - (variable_cost * worst_volume + fixed_cost + marketing_spend)
worst_margin = (worst_profit / worst_revenue * 100) if worst_revenue > 0 else 0.0

scenario_df = pd.DataFrame([
    {
        "Scenario": "Current Scenario",
        "Price (€)": base_price,
        "Volume": base_volume,
        "Revenue (€)": base_revenue,
        "Net Profit (€)": base_profit,
        "Margin (%)": base_margin
    },
    {
        "Scenario": "Best Case",
        "Price (€)": best_price,
        "Volume": best_volume,
        "Revenue (€)": best_revenue,
        "Net Profit (€)": best_profit,
        "Margin (%)": best_margin
    },
    {
        "Scenario": "Worst Case",
        "Price (€)": worst_price,
        "Volume": worst_volume,
        "Revenue (€)": worst_revenue,
        "Net Profit (€)": worst_profit,
        "Margin (%)": worst_margin
    }
])

st.dataframe(scenario_df, use_container_width=True)

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.bar(scenario_df["Scenario"], scenario_df["Net Profit (€)"])
ax3.set_title("Net Profit by Scenario")
ax3.set_ylabel("€")
st.pyplot(fig3)

# ----------------------------
# Download results
# ----------------------------
st.subheader("Export")

csv_data = scenario_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Scenario Comparison CSV",
    data=csv_data,
    file_name="scenario_comparison.csv",
    mime="text/csv"
)