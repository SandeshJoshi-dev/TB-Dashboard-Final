

import streamlit as st
import pandas as pd
import plotly.graph_objects as go



#  PAGE 
st.set_page_config(
    page_title="Global TB Statistics Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

#  COLORS 
BG      = "#f8fafc"
SURFACE = "#ffffff"
BORDER  = "#e2e8f0"
TEXT    = "#000000"
MUTED   = "#000000"
GRID    = "#f1f5f9"
BLACK   = "#000000"

PIE_COLORS = {
    "AFR": "#ef4444", "AMR": "#fb923c", "EMR": "#fbbf24",
    "EUR": "#86efac", "SEA": "#60a5fa", "WPR": "#c4b5fd",
}
SCATTER_COLORS = {
    "EMR": "#3b82f6", "EUR": "#f97316", "AFR": "#22c55e",
    "WPR": "#ef4444", "AMR": "#8b5cf6", "SEA": "#eab308",
}
DET_COLORS = {
    "EUR": "#166534", "AMR": "#15803d", "WPR": "#16a34a",
    "EMR": "#22c55e", "SEA": "#86efac", "AFR": "#bbf7d0",
}
RNAMES = {
    "AFR": "Africa",  "AMR": "Americas", "EMR": "E. Med.",
    "EUR": "Europe",  "SEA": "SE Asia",  "WPR": "W. Pacific",
}

#  CSS 
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Inter', sans-serif !important;
    background-color: {BG} !important;
    color: {TEXT};
}}
.block-container {{ padding: 1.2rem 1.8rem 2rem !important; max-width: 100% !important; }}

/* Hide sidebar toggle button entirely */
[data-testid="collapsedControl"] {{ display: none !important; }}

.dash-title {{
    text-align: center; font-size: clamp(18px,2.5vw,28px); font-weight: 800;
    color: {BLACK}; padding: 14px 0 10px; letter-spacing: -0.5px;
}}

/* Filter bar */
.filter-bar {{
    display: flex; align-items: center; gap: 24px; flex-wrap: wrap;
    background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 10px;
    padding: 12px 20px; margin-bottom: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}}
.filter-label {{
    font-size: 10px; font-weight: 700; letter-spacing: 1.5px;
    text-transform: uppercase; color: {BLACK}; margin-bottom: 2px;
}}

/* Streamlit widget overrides inside filter bar */
div[data-testid="stSlider"] > label,
div[data-testid="stMultiSelect"] > label {{
    font-size: 10px !important; font-weight: 700 !important;
    letter-spacing: 1.5px !important; text-transform: uppercase !important;
    color: {BLACK} !important;
}}

.kpi-strip {{
    display: grid; grid-template-columns: repeat(5,1fr);
    background: {SURFACE}; border: 1px solid {BORDER};
    border-radius: 12px; margin-bottom: 22px; overflow: hidden;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}}
.kpi-item {{
    padding: 18px 16px 14px; text-align: center;
    border-right: 1px solid {BORDER};
}}
.kpi-item:last-child {{ border-right: none; }}
.kpi-val {{ font-size: 28px; font-weight: 800; line-height: 1; margin-bottom: 6px; }}
.kpi-lbl {{ font-size: 10px; color: {BLACK}; line-height: 1.5; }}

.card {{
    background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px;
    padding: 16px 18px 10px; box-shadow: 0 1px 6px rgba(0,0,0,0.05);
}}
.card-title {{
    font-size: 12.5px; font-weight: 700; color: {BLACK};
    text-align: center; margin-bottom: 8px;
}}

::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: {BG}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 2px; }}
</style>
""", unsafe_allow_html=True)

#  DATA 
@st.cache_data
def load():
    df = pd.read_csv("clean_file.csv")
    df.columns = df.columns.str.strip()
    return df

df = load()

C_COUNTRY    = "Country or territory name"
C_REGION     = "Region"
C_YEAR       = "Year"
C_PREV_RATE  = "Estimated prevalence of TB (all forms) per 100 000 population"
C_MORT_RATE  = "Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 population"
C_DEATHS     = "Estimated number of deaths from TB (all forms, excluding HIV)"
C_HIV_RATE   = "Estimated mortality of TB cases who are HIV-positive, per 100 000 population"
C_DEATHS_HIV = "Estimated number of deaths from TB in people who are HIV-positive"
C_INC_RATE   = "Estimated incidence (all forms) per 100 000 population"
C_CASES      = "Estimated number of incident cases (all forms)"
C_DETECT     = "Case detection rate (all forms), percent"

all_years   = sorted(df[C_YEAR].unique())
all_regions = sorted(df[C_REGION].unique())

#  TITLE 
st.markdown('<div class="dash-title">Global Tuberculosis Statistics Dashboard</div>',
            unsafe_allow_html=True)

#  INLINE FILTER BAR 
fc1, fc2, fc3, fc4 = st.columns([1.4, 1.4, 0.8, 0.8])

with fc1:
    year_range = st.slider(
        "Year Range",
        min_value=int(min(all_years)),
        max_value=int(max(all_years)),
        value=(1990, 2013),
    )

with fc2:
    sel_regions = st.multiselect(
        "Regions",
        options=all_regions,
        default=all_regions,
        format_func=lambda x: f"{x} — {RNAMES.get(x, x)}",
    )

with fc3:
    top_n = st.slider("Top N Countries", 5, 20, 10)

with fc4:
    st.markdown(f"""
    <div style="font-size:11px;color:{BLACK};line-height:1.9;padding-top:6px;">
      <b>219</b> Countries &nbsp;|&nbsp;
      <b>1990–2013</b> &nbsp;|&nbsp;
      <b>5,120</b> Records
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

#  FILTER 
regions_use = sel_regions if sel_regions else all_regions
dff = df[
    df[C_YEAR].between(year_range[0], year_range[1]) &
    df[C_REGION].isin(regions_use)
].copy()

if dff.empty:
    st.warning("No data matches the current filters.")
    st.stop()

#  HELPERS 
def fmt_big(n):
    if n >= 1e9: return f"{n/1e9:.1f}B"
    if n >= 1e6: return f"{n/1e6:.1f}M"
    if n >= 1e3: return f"{n/1e3:.1f}K"
    return f"{n:.1f}"

HL = dict(bgcolor=SURFACE, bordercolor=BORDER,
          font=dict(color=BLACK, size=12, family="Inter"))

def xax(title_text, **extra):
    d = dict(
        gridcolor=SURFACE, linecolor=BORDER, tickcolor=BORDER,
        zeroline=False, showline=True,
        title=dict(text=title_text, font=dict(color=BLACK, size=11, family="Inter")),
        tickfont=dict(color=BLACK, size=10, family="Inter"),
    )
    d.update(extra)
    return d

def yax(title_text, **extra):
    d = dict(
        gridcolor=SURFACE, linecolor=BORDER, tickcolor=BORDER,
        zeroline=False, showline=True,
        title=dict(text=title_text, font=dict(color=BLACK, size=11, family="Inter")),
        tickfont=dict(color=BLACK, size=10, family="Inter"),
    )
    d.update(extra)
    return d

#  KPI STRIP 
st.markdown(f"""
<div class="kpi-strip">
  <div class="kpi-item">
    <div class="kpi-val" style="color:#ef4444;">{fmt_big(dff[C_DEATHS].sum())}</div>
    <div class="kpi-lbl">Total TB Deaths<br>(Excl. HIV)</div>
  </div>
  <div class="kpi-item">
    <div class="kpi-val" style="color:#8b5cf6;">{fmt_big(dff[C_DEATHS_HIV].sum())}</div>
    <div class="kpi-lbl">Total TB Deaths<br>(HIV-Positive)</div>
  </div>
  <div class="kpi-item">
    <div class="kpi-val" style="color:#3b82f6;">{fmt_big(dff[C_CASES].sum())}</div>
    <div class="kpi-lbl">Total Incident<br>Cases</div>
  </div>
  <div class="kpi-item">
    <div class="kpi-val" style="color:#22c55e;">{dff[C_DETECT].mean():.1f}%</div>
    <div class="kpi-lbl">Avg Case<br>Detection Rate</div>
  </div>
  <div class="kpi-item">
    <div class="kpi-val" style="color:#f97316;">{dff[C_INC_RATE].mean():.1f}</div>
    <div class="kpi-lbl">Avg Incidence<br>per 100k</div>
  </div>
</div>
""", unsafe_allow_html=True)

#  ROW 1 
col1, col2, col3 = st.columns([1.3, 1.0, 1.3], gap="medium")

#  CHART 1: Trend Line 
with col1:
    st.markdown('<div class="card"><div class="card-title">Global Incident Cases Trend (1990–2013)</div>',
                unsafe_allow_html=True)
    trend = dff.groupby(C_YEAR)[C_CASES].sum().reset_index()
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=trend[C_YEAR], y=trend[C_CASES],
        mode="lines+markers",
        line=dict(color="#3b82f6", width=2.5),
        marker=dict(size=5, color="#3b82f6"),
        fill="tozeroy", fillcolor="rgba(59,130,246,0.09)",
        name="Cases",
        hovertemplate="<b>Year %{x}</b><br>Cases: <b>%{y:,.0f}</b><extra></extra>",
    ))
    fig1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=GRID,
        font=dict(family="Inter", color=BLACK, size=11),
        margin=dict(l=50, r=20, t=16, b=50),
        height=290, showlegend=False, hoverlabel=HL,
    )
    fig1.update_xaxes(**xax("Year"))
    fig1.update_yaxes(**yax("Incident Cases (Millions)", tickformat=".2s"))
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

#  CHART 2: Pie 
with col2:
    st.markdown('<div class="card"><div class="card-title">Incident Cases Share by Region</div>',
                unsafe_allow_html=True)
    pie_df = dff.groupby(C_REGION)[C_CASES].sum().reset_index()
    fig2 = go.Figure(go.Pie(
        labels=pie_df[C_REGION],
        values=pie_df[C_CASES],
        hole=0.0,
        marker=dict(
            colors=[PIE_COLORS.get(r, "#888") for r in pie_df[C_REGION]],
            line=dict(color=SURFACE, width=1.5),
        ),
        textinfo="label+percent",
        textfont=dict(size=9, color=BLACK),
        hovertemplate="<b>%{label}</b><br>Cases: %{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=BLACK, size=10),
        margin=dict(l=10, r=10, t=10, b=10),
        height=290, showlegend=False, hoverlabel=HL,
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

#  CHART 3: Top N Deaths Bar 
with col3:
    st.markdown(f'<div class="card"><div class="card-title">Top {top_n} Countries by TB Deaths (Non-HIV)</div>',
                unsafe_allow_html=True)
    top_df = (
        dff.groupby(C_COUNTRY)[C_DEATHS].sum().reset_index()
        .nlargest(top_n, C_DEATHS)
        .sort_values(C_DEATHS, ascending=True)
    )
    fig3 = go.Figure(go.Bar(
        x=top_df[C_DEATHS], y=top_df[C_COUNTRY],
        orientation="h",
        marker_color="#dc2626", marker_opacity=0.82, marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>Deaths: <b>%{x:,.0f}</b><extra></extra>",
    ))
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=GRID,
        font=dict(family="Inter", color=BLACK, size=11),
        margin=dict(l=170, r=20, t=16, b=40),
        height=290, showlegend=False, hoverlabel=HL,
    )
    fig3.update_xaxes(**xax("Total Deaths", tickformat=".2s"))
    fig3.update_yaxes(
        gridcolor="rgba(0,0,0,0)", linecolor=BORDER,
        tickcolor="rgba(0,0,0,0)", showline=False,
        tickfont=dict(size=9, color=BLACK, family="Inter"),
    )
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

#  ROW 2 
col4, col5, col6 = st.columns([1.3, 1.0, 1.3], gap="medium")

#  CHART 4: Prevalence vs Incidence Scatter 
with col4:
    st.markdown('<div class="card"><div class="card-title">Prevalence vs Incidence (per 100k)</div>',
                unsafe_allow_html=True)
    sdf = dff.dropna(subset=[C_PREV_RATE, C_INC_RATE]).copy()
    fig4 = go.Figure()
    for reg in regions_use:
        grp = sdf[sdf[C_REGION] == reg]
        if grp.empty:
            continue
        fig4.add_trace(go.Scatter(
            x=grp[C_PREV_RATE], y=grp[C_INC_RATE],
            mode="markers", name=reg,
            marker=dict(size=4, color=SCATTER_COLORS.get(reg, "#888"), opacity=0.65),
            text=grp[C_COUNTRY] + " (" + grp[C_YEAR].astype(str) + ")",
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Prevalence: %{x:.0f}/100k<br>"
                "Incidence: %{y:.0f}/100k<extra></extra>"
            ),
        ))
    fig4.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=GRID,
        font=dict(family="Inter", color=BLACK, size=11),
        margin=dict(l=50, r=20, t=16, b=50),
        height=290, hoverlabel=HL,
        legend=dict(
            title=dict(text="Region", font=dict(color=BLACK, size=10)),
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor=BORDER, borderwidth=1,
            font=dict(size=9, color=BLACK), x=0.01, y=0.99,
        ),
    )
    fig4.update_xaxes(**xax("Prevalence per 100k"))
    fig4.update_yaxes(**yax("Incidence per 100k"))
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

#  CHART 5: Detection Rate Bar 
with col5:
    st.markdown('<div class="card"><div class="card-title">Mean Case Detection Rate by Region (%)</div>',
                unsafe_allow_html=True)
    det_df = (
        dff.groupby(C_REGION)[C_DETECT].mean().reset_index()
        .sort_values(C_DETECT, ascending=False)
    )
    fig5 = go.Figure(go.Bar(
        x=det_df[C_REGION], y=det_df[C_DETECT],
        marker_color=[DET_COLORS.get(r, "#22c55e") for r in det_df[C_REGION]],
        marker_line_width=0,
        text=det_df[C_DETECT].round(1).astype(str) + "%",
        textposition="outside",
        textfont=dict(size=9, color=BLACK, family="Inter"),
        hovertemplate="<b>%{x}</b><br>Avg Detection: <b>%{y:.1f}%</b><extra></extra>",
    ))
    fig5.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=GRID,
        font=dict(family="Inter", color=BLACK, size=11),
        margin=dict(l=50, r=20, t=16, b=50),
        height=290, showlegend=False, hoverlabel=HL,
    )
    fig5.update_xaxes(
        gridcolor="rgba(0,0,0,0)", linecolor=BORDER,
        tickcolor="rgba(0,0,0,0)", showline=True,
        title=dict(text="Region", font=dict(color=BLACK, size=11, family="Inter")),
        tickfont=dict(color=BLACK, size=10, family="Inter"),
    )
    fig5.update_yaxes(**yax("Detection Rate (%)", range=[0, 105]))
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

#  CHART 6: Mortality Area 
with col6:
    st.markdown('<div class="card"><div class="card-title">TB Mortality Comparison (Excl. vs HIV+)</div>',
                unsafe_allow_html=True)
    mort = dff.groupby(C_YEAR).agg(
        non_hiv=(C_DEATHS,     "sum"),
        hiv_pos=(C_DEATHS_HIV, "sum"),
    ).reset_index()
    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(
        x=mort[C_YEAR], y=mort["non_hiv"],
        mode="lines", name="Non-HIV",
        line=dict(color="#f87171", width=0),
        fill="tozeroy", fillcolor="rgba(248,113,113,0.55)",
        hovertemplate="<b>Year %{x}</b><br>Non-HIV Deaths: <b>%{y:,.0f}</b><extra></extra>",
    ))
    fig6.add_trace(go.Scatter(
        x=mort[C_YEAR], y=mort["hiv_pos"],
        mode="lines", name="HIV+",
        line=dict(color="#c084fc", width=0),
        fill="tozeroy", fillcolor="rgba(192,132,252,0.6)",
        hovertemplate="<b>Year %{x}</b><br>HIV+ Deaths: <b>%{y:,.0f}</b><extra></extra>",
    ))
    fig6.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=GRID,
        font=dict(family="Inter", color=BLACK, size=11),
        margin=dict(l=50, r=20, t=16, b=50),
        height=290, hoverlabel=HL,
        legend=dict(
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor=BORDER, borderwidth=1,
            font=dict(size=10, color=BLACK), x=0.01, y=0.99,
        ),
    )
    fig6.update_xaxes(**xax("Year"))
    fig6.update_yaxes(**yax("Total Deaths", tickformat=".2s"))
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)


