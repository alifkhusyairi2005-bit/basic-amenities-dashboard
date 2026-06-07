import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Malaysia Basic Amenities Access Index",
    page_icon="🇲🇾",
    layout="wide",
)

# ── Data ─────────────────────────────────────────────────────────────────────
YEARS = [2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]

RAW = {
    "Kelantan":          [80.7, 79.4, 78.1, 76.7, 75.4, 74.1, 72.8, 71.5],
    "Sabah":             [91.5, 91.2, 91.0, 90.7, 90.4, 90.0, 89.6, 89.2],
    "Sarawak":           [93.5, 93.2, 92.9, 92.6, 92.3, 92.0, 91.7, 91.4],
    "Pahang":            [98.7, 98.6, 98.6, 98.5, 98.4, 98.3, 98.2, 98.2],
    "Terengganu":        [99.0, 99.1, 99.1, 99.2, 99.2, 99.1, 99.0, 99.0],
    "Perak":             [99.5, 99.4, 99.4, 99.3, 99.3, 99.2, 99.2, 99.1],
    "Johor":             [99.7, 99.7, 99.7, 99.6, 99.6, 99.5, 99.5, 99.5],
    "Kedah":             [99.8, 99.8, 99.8, 99.8, 99.8, 99.8, 99.7, 99.7],
    "Negeri Sembilan":   [99.9, 99.9, 99.8, 99.8, 99.8, 99.8, 99.8, 99.8],
    "Pulau Pinang":      [100,  100,  100,  100,  100,  100,  100,  100 ],
    "Perlis":            [100,  100,  100,  100,  100,  100,  100,  100 ],
    "Melaka":            [100,  100,  100,  100,  100,  100,  100,  100 ],
    "Selangor":          [100,  100,  100,  100,  100,  100,  100,  100 ],
    "W.P. Kuala Lumpur": [100,  100,  100,  100,  100,  100,  100,  100 ],
    "W.P. Labuan":       [100,  100,  100,  100,  100,  100,  100,  100 ],
    "W.P. Putrajaya":    [100,  100,  100,  100,  100,  100,  100,  100 ],
}

df = pd.DataFrame(RAW, index=YEARS).T
df.index.name = "State"
df.columns = [str(y) for y in YEARS]
df_long = df.reset_index().melt(id_vars="State", var_name="Year", value_name="Index")
df_long["Year"] = df_long["Year"].astype(int)


def tier(val):
    if val >= 100: return "100% (Full)"
    if val >= 95:  return "95–99%"
    if val >= 90:  return "90–95%"
    return "Below 90%"

df_long["Tier"] = df_long["Index"].apply(tier)
TIER_COLORS = {"100% (Full)": "#3ecf8e", "95–99%": "#4a9eff", "90–95%": "#f5a623", "Below 90%": "#e74c3c"}

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono&display=swap');
  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
  .main { background: #0f1117; }
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
  h1 { font-size: 1.4rem !important; font-weight: 600 !important; letter-spacing: -0.02em !important; }
  .metric-box {
    background: #1a1d27;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    border-top: 2px solid;
  }
  .stMetric { background: #1a1d27; border-radius: 10px; padding: 0.75rem 1rem; }
  .alert-box {
    background: rgba(231,76,60,0.08);
    border: 1px solid rgba(231,76,60,0.3);
    border-left: 3px solid #e74c3c;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-size: 0.85rem;
    color: #f5a0a0;
    margin-bottom: 1rem;
  }
  .section-label {
    font-size: 0.7rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8b8fa8;
    margin-bottom: 0.5rem;
  }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🇲🇾 Malaysia Basic Amenities Access Index")
    st.caption("Forecasted Composite Access Index by State · 2023–2030 · WIE2003 Group Assignment")
with col_h2:
    st.markdown("""
    <div style='text-align:right;margin-top:0.5rem'>
      <span style='background:rgba(62,207,142,0.12);color:#3ecf8e;font-size:0.7rem;
             padding:4px 12px;border-radius:20px;border:1px solid rgba(62,207,142,0.3);
             font-family:monospace'>SDG 11 · Data as Insight</span>
    </div>""", unsafe_allow_html=True)

st.divider()

# ── Alert ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='alert-box'>
  ⚠️ <strong>Kelantan</strong> is the only state on a declining trajectory —
  projected to fall from <strong>80.7%</strong> in 2023 to <strong>71.5%</strong> by 2030.
  Urgent policy intervention is recommended.
</div>""", unsafe_allow_html=True)

# ── Metrics ───────────────────────────────────────────────────────────────────
vals_2023 = df["2023"]
vals_2030 = df["2030"]
avg23 = round(vals_2023.mean(), 1)
avg30 = round(vals_2030.mean(), 1)
full23 = int((vals_2023 >= 100).sum())
below90_30 = int((vals_2030 < 90).sum())

m1, m2, m3, m4 = st.columns(4)
m1.metric("National avg (2023)", f"{avg23}%", help="Mean composite access index across all 16 states")
m2.metric("National avg (2030)", f"{avg30}%", delta=f"{round(avg30-avg23,1)}%", help="Projected mean by 2030")
m3.metric("States at 100%", full23, help="States with full amenities coverage in 2023")
m4.metric("States below 90% (2030)", below90_30, delta=f"-{below90_30} states need attention", delta_color="inverse")

st.divider()

# ── Section 1: Bar chart ──────────────────────────────────────────────────────
st.markdown("<div class='section-label'>State ranking by access index</div>", unsafe_allow_html=True)

year_sel = st.select_slider("Select year", options=YEARS, value=2023)

df_year = df_long[df_long["Year"] == year_sel].sort_values("Index")
df_year["Color"] = df_year["Index"].apply(lambda v: TIER_COLORS[tier(v)])

fig_bar = px.bar(
    df_year, x="Index", y="State", orientation="h",
    color="Tier",
    color_discrete_map=TIER_COLORS,
    text="Index",
    range_x=[65, 101],
)
fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="inside", insidetextanchor="end")
fig_bar.update_layout(
    height=480,
    plot_bgcolor="#1a1d27", paper_bgcolor="#0f1117",
    font=dict(color="#e8eaf0", family="DM Sans"),
    xaxis=dict(title="Composite Access Index (%)", gridcolor="rgba(255,255,255,0.05)", ticksuffix="%"),
    yaxis=dict(title="", gridcolor="rgba(255,255,255,0.05)"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=0, r=20, t=10, b=40),
)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ── Section 2: Trend + Distribution ──────────────────────────────────────────
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='section-label'>Trend over time — select a state</div>", unsafe_allow_html=True)
    state_sel = st.selectbox("State", options=list(RAW.keys()), index=0, label_visibility="collapsed")
    df_state = df_long[df_long["State"] == state_sel]
    first_val = df_state["Index"].iloc[0]
    line_color = TIER_COLORS[tier(first_val)]

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_state["Year"], y=df_state["Index"],
        mode="lines+markers",
        line=dict(color=line_color, width=3),
        marker=dict(size=7, color=line_color),
        fill="tozeroy", fillcolor=line_color.replace(")", ",0.1)").replace("rgb", "rgba") if line_color.startswith("rgb") else line_color + "18",
        name=state_sel,
    ))
    fig_line.update_layout(
        height=300,
        plot_bgcolor="#1a1d27", paper_bgcolor="#0f1117",
        font=dict(color="#e8eaf0", family="DM Sans"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", dtick=1),
        yaxis=dict(title="Index (%)", gridcolor="rgba(255,255,255,0.05)",
                   range=[max(60, df_state["Index"].min()-3), 101]),
        showlegend=False,
        margin=dict(l=0, r=10, t=10, b=40),
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.markdown("<div class='section-label'>Distribution by tier · 2030 forecast</div>", unsafe_allow_html=True)
    tier_counts = df_long[df_long["Year"]==2030]["Tier"].value_counts().reindex(
        ["100% (Full)","95–99%","90–95%","Below 90%"], fill_value=0
    )
    fig_pie = px.bar(
        x=tier_counts.index, y=tier_counts.values,
        color=tier_counts.index,
        color_discrete_map=TIER_COLORS,
        text=tier_counts.values,
    )
    fig_pie.update_traces(texttemplate="%{text} states", textposition="outside")
    fig_pie.update_layout(
        height=300,
        plot_bgcolor="#1a1d27", paper_bgcolor="#0f1117",
        font=dict(color="#e8eaf0", family="DM Sans"),
        xaxis=dict(title="", gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(title="Number of states", gridcolor="rgba(255,255,255,0.05)"),
        showlegend=False,
        margin=dict(l=0, r=10, t=30, b=40),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# ── Section 3: Heatmap ────────────────────────────────────────────────────────
st.markdown("<div class='section-label'>Heatmap — all states · all years</div>", unsafe_allow_html=True)

fig_heat = go.Figure(data=go.Heatmap(
    z=df.values,
    x=df.columns.tolist(),
    y=df.index.tolist(),
    colorscale=[[0,"#e74c3c"],[0.3,"#f5a623"],[0.6,"#4a9eff"],[1.0,"#3ecf8e"]],
    zmin=70, zmax=100,
    text=[[f"{v:.1f}" for v in row] for row in df.values],
    texttemplate="%{text}",
    textfont=dict(size=11, color="white"),
    hovertemplate="<b>%{y}</b><br>Year: %{x}<br>Index: %{z:.1f}%<extra></extra>",
    colorbar=dict(
        title="Index (%)",
        tickcolor="#8b8fa8",
        tickfont=dict(color="#8b8fa8"),
        titlefont=dict(color="#8b8fa8"),
    )
))
fig_heat.update_layout(
    height=500,
    plot_bgcolor="#1a1d27", paper_bgcolor="#0f1117",
    font=dict(color="#e8eaf0", family="DM Sans"),
    xaxis=dict(title="Year", gridcolor="rgba(255,255,255,0.05)"),
    yaxis=dict(title="", autorange="reversed"),
    margin=dict(l=130, r=20, t=10, b=40),
)
st.plotly_chart(fig_heat, use_container_width=True)

st.divider()

# ── Section 4: Key Insights ───────────────────────────────────────────────────
st.markdown("<div class='section-label'>Key insights</div>", unsafe_allow_html=True)

i1, i2, i3, i4 = st.columns(4)
with i1:
    st.info("📉 **Kelantan declining**\n\nThe only state with a downward trend — losing 9.2 percentage points from 2023 to 2030.")
with i2:
    st.success("🏙️ **Urban full coverage**\n\nAll W.P. territories, Selangor, Melaka, and Perlis maintain 100% throughout the forecast.")
with i3:
    st.warning("🌿 **East Malaysia gap**\n\nSabah (89.2%) and Sarawak (91.4%) by 2030 show persistent rural access challenges.")
with i4:
    st.info("🎯 **SDG 11 alignment**\n\nClosing the amenities gap is critical for achieving Sustainable Cities & Communities.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.caption("WIE2003 Group Assignment · Basic Amenities IDS · Data as Insight · Built with Streamlit + Plotly")
