import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="TB Dashboard", layout="wide")

# Simple CSS for colors and spacing
st.markdown("""
    <style>
        .block-container {padding-top: 1rem; padding-bottom: 0rem;}
        [data-testid="stMetric"] {background-color: #f0f2f6; padding: 10px; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load():
    df = pd.read_csv("clean_file.csv")
    df.columns = df.columns.str.strip()
    return df

df = load()

# Define Color Map for Regions
REGION_COLORS = {
    "AFR": "#ef4444", "AMR": "#f97316", "EMR": "#eab308",
    "EUR": "#22c55e", "SEA": "#06b6d4", "WPR": "#8b5cf6"
}

# Column Names
C_COUNTRY, C_REGION, C_YEAR = "Country or territory name", "Region", "Year"
C_CASES, C_DEATHS, C_DETECT = "Estimated number of incident cases (all forms)", "Estimated number of deaths from TB (all forms, excluding HIV)", "Case detection rate (all forms), percent"
C_DEATHS_HIV = "Estimated number of deaths from TB in people who are HIV-positive"
C_INC_RATE = "Estimated incidence (all forms) per 100 000 population"
C_PREV_RATE = "Estimated prevalence of TB (all forms) per 100 000 population"

# Sidebar
with st.sidebar:
    st.title("Global TB Statistics Dashboard")
    st.title("Filters")
    yr = st.slider("Year Range", 1990, 2013, (1990, 2013))
    all_regs = sorted(df[C_REGION].unique())
    regs = st.multiselect("Regions", all_regs, default=all_regs)
    top_n = st.slider("Top Countries", 5, 15, 8)

# Filter Data
dff = df[df[C_YEAR].between(yr[0], yr[1]) & df[C_REGION].isin(regs)]

st.markdown("")

# KPI Metrics Row 
k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("TB Deaths", dff[C_DEATHS].sum(), format="compact")
k2.metric("HIV+ Deaths", dff[C_DEATHS_HIV].sum(), format="compact")
k3.metric("Total Cases", dff[C_CASES].sum(), format="compact")
k4.metric("Avg Detection Rate", f"{dff[C_DETECT].mean():.1f}%")
k5.metric("Avg Incidence Rate Per 100K", dff[C_INC_RATE].mean(), format="compact")

# Layout - 2 Rows, 3 Columns
CH = 220 # Height to keep it non-scrollable

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

# ROW 1 
with col1:
    st.markdown("<b style='color:#3b82f6'>Incident Cases Trend</b>", unsafe_allow_html=True)
    trend = dff.groupby(C_YEAR)[C_CASES].sum()
    fig = go.Figure(go.Scatter(x=trend.index, y=trend.values, fill='tozeroy', line=dict(color='#3b82f6')))
    fig.update_layout(height=CH, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("<b>Cases by Region</b>", unsafe_allow_html=True)
    pie = dff.groupby(C_REGION)[C_CASES].sum()
    fig = go.Figure(go.Pie(labels=pie.index, values=pie.values, hole=.4, 
                           marker=dict(colors=[REGION_COLORS.get(r) for r in pie.index])))
    fig.update_layout(height=CH, margin=dict(l=10, r=10, t=10, b=10), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.markdown(f"<b style='color:#ef4444'>Top {top_n} Countries (Deaths)</b>", unsafe_allow_html=True)
    top = dff.groupby(C_COUNTRY)[C_DEATHS].sum().nlargest(top_n).sort_values()
    fig = go.Figure(go.Bar(x=top.values, y=top.index, orientation='h', marker_color='#ef4444'))
    fig.update_layout(height=CH, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

# ROW 2 
with col4:
    st.markdown("<b>Prevalence vs Incidence (By Region)</b>", unsafe_allow_html=True)
    fig = go.Figure()
    for r in regs:
        sub = dff[dff[C_REGION] == r]
        fig.add_trace(go.Scatter(x=sub[C_PREV_RATE], y=sub[C_INC_RATE], mode='markers', name=r, 
                                 marker=dict(color=REGION_COLORS.get(r), size=5, opacity=0.6)))
    fig.update_layout(height=CH, margin=dict(l=10, r=10, t=10, b=10), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with col5:
    st.markdown("<b style='color:#22c55e'>Detection Rate (%) by Region</b>", unsafe_allow_html=True)
    det = dff.groupby(C_REGION)[C_DETECT].mean().sort_values(ascending=False)
    fig = go.Figure(go.Bar(x=det.index, y=det.values, marker_color=[REGION_COLORS.get(r) for r in det.index]))
    fig.update_layout(height=CH, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.markdown("<b>Mortality: <span style='color:#f87171'>HIV</span> vs <span style='color:#a855f7'>Non-HIV+</span></b>", unsafe_allow_html=True)
    mort = dff.groupby(C_YEAR)[[C_DEATHS, C_DEATHS_HIV]].sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mort.index, y=mort[C_DEATHS_HIV], name="HIV+", stackgroup='one', line=dict(color='#f87171')))
    fig.add_trace(go.Scatter(x=mort.index, y=mort[C_DEATHS], name="Non_HIV", stackgroup='one', line=dict(color='#a855f7')))
    fig.update_layout(height=CH, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
