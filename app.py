import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Basic Amenities Dashboard", layout="wide")

st.title("Malaysia Basic Amenities Access")
st.write("Visualizing access to piped water, sanitation, and electricity by state.")

# 1. Load Data safely
@st.cache_data
def load_data():
    df = pd.read_csv("StateAmenities.csv")
    # Clean up column names just in case of whitespace
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading StateAmenities.csv: {e}")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")

# State Selection (Multi-select)
all_states = sorted(df["state"].unique())
state_sel = st.sidebar.multiselect(
    "Select States to Display:", 
    options=all_states, 
    default=["W.P. Kuala Lumpur", "Selangor", "Sabah", "Kelantan"]
)

# Metric Selection
metrics = {
    "Overall Index (Mean)": "mean_amenities",
    "Piped Water": "piped_water",
    "Sanitation": "sanitation",
    "Electricity": "electricity"
}
metric_display = st.sidebar.selectbox("Select Metric to Visualize:", list(metrics.keys()))
chosen_metric_col = metrics[metric_display]

# Filter dataset based on selection
df_filtered = df[df["state"].isin(state_sel)]

# --- MAIN DASHBOARD LAYOUT ---

if df_filtered.empty:
    st.warning("Please select at least one state in the sidebar to view the visualizations.")
else:
    # Row 1: Key Metrics (Latest Year 2022)
    st.subheader(f"Latest 2022 Overview: {metric_display}")
    df_2022 = df_filtered[df_filtered["year"] == 2022]
    
    if not df_2022.empty:
        cols = st.columns(min(len(df_2022), 4))
        for idx, row in enumerate(df_2022.itertuples()):
            col_pos = idx % 4
            with cols[col_pos]:
                st.metric(
                    label=f"{row.state} ({row.cluster_label})", 
                    value=f"{getattr(row, chosen_metric_col):.2f}%"
                )
    
    st.markdown("---")
    
    # Row 2: Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader(f"Trend Analysis (2016 - 2022)")
        
        # Using go.Scatter safely here to fix your specific bug
        fig_line = go.Figure()
        
        for state in state_sel:
            df_state = df_filtered[df_filtered["state"] == state].sort_values("year")
            if not df_state.empty:
                fig_line.add_trace(go.Scatter(
                    x=df_state["year"],               # Uses correct lowercase 'year'
                    y=df_state[chosen_metric_col],     # Uses dynamic valid metric column
                    mode="lines+markers",
                    name=state,
                    line=dict(width=3),
                    marker=dict(size=8)
                    # Removed ambiguous fill or color properties causing the crash
                ))
                
        fig_line.update_layout(
            xaxis_title="Year",
            yaxis_title="Percentage (%)",
            xaxis=dict(tickmode='array', tickvals=[2016, 2019, 2022]),
            margin=dict(l=40, r=40, t=20, b=40),
            hovermode="x unified"
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col_chart2:
        st.subheader("2022 Comparison Bar Chart")
        # Interactive Plotly Express bar chart
        fig_bar = px.bar(
            df_2022, 
            x="state", 
            y=chosen_metric_col,
            color="cluster_label",
            labels={chosen_metric_col: "Percentage (%)", "state": "State", "cluster_label": "Access Cluster"},
            category_orders={"cluster_label": ["High Amenities Access", "Moderate Amenities Access", "Lower Amenities Access"]}
        )
        fig_bar.update_layout(margin=dict(l=40, r=40, t=20, b=40))
        st.plotly_chart(fig_bar, use_container_width=True)

    # Row 3: Raw Data View
    st.markdown("---")
    st.subheader("Filtered Data View")
    st.dataframe(df_filtered.sort_values(by=["state", "year"]), use_container_width=True)
