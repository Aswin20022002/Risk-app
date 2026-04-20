import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import requests
import json

st.set_page_config(page_title="India Physical Risk Explorer", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
body { background-color: #ffffff; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1.5rem 4rem; max-width: 860px; }
.hero { background: #01244a; border-radius: 10px; padding: 1.75rem 1.5rem; margin-bottom: 1.5rem; }
.hero h1 { color: #f0f9ff; font-size: 1.7rem; font-weight: 700; margin: 0 0 0.3rem; letter-spacing: -0.02em; }
.hero p  { color: #94a3b8; font-size: 0.9rem; margin: 0; }
.stTextInput > div > div > input { border-radius: 6px !important; border: 1px solid #dee7f0 !important; font-size: 1rem !important; }
.stButton>button { background-color: #01244a; color: white; border-radius: 8px; border: none; font-weight: 600; }
.stButton>button:hover { background-color: #0085ca; color: white; }
.location-pill { display: inline-flex; align-items: center; gap: 0.4rem; background: #dee7f0; border: 1px solid #5c8bb4; border-radius: 20px; padding: 0.35rem 0.9rem; font-size: 0.82rem; color: #01244a; font-weight: 500; margin-bottom: 1rem; }
.hazard-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.85rem; margin-bottom: 0.85rem; }
.hazard-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 0.85rem; margin-bottom: 1rem; }
.hazard-card { border-radius: 12px; padding: 1rem 1.1rem; border: 1px solid; }
.hazard-card.very-high { background:#fff5f5; border-color:#fca5a5; }
.hazard-card.high      { background:#fff7ed; border-color:#fdba74; }
.hazard-card.moderate  { background:#fefce8; border-color:#fde047; }
.hazard-card.low       { background:#f0fdf4; border-color:#86efac; }
.hazard-card.very-low  { background:#f0f9ff; border-color:#7dd3fc; }
.hc-top { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 0.45rem; }
.hc-score { font-size: 1.9rem; font-weight: 700; letter-spacing: -0.04em; line-height: 1; }
.hc-label { font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.07em; color: #64748b; margin-top: 0.15rem; }
.hc-badge { font-size: 0.7rem; font-weight: 600; padding: 0.18rem 0.55rem; border-radius: 12px; white-space: nowrap; margin-top: 0.1rem; }
.badge-very-high { background:#fee2e2; color:#b91c1c; }
.badge-high      { background:#ffedd5; color:#c2410c; }
.badge-moderate  { background:#fef9c3; color:#a16207; }
.badge-low       { background:#dcfce7; color:#15803d; }
.badge-very-low  { background:#e0f2fe; color:#0369a1; }
.bar-wrap { background:#e2e8f0; border-radius:4px; height:5px; margin:0.45rem 0 0.55rem; overflow:hidden; }
.bar-fill { height:100%; border-radius:4px; }
.bar-very-high { background:linear-gradient(90deg,#f87171,#dc2626); }
.bar-high      { background:linear-gradient(90deg,#fb923c,#ea580c); }
.bar-moderate  { background:linear-gradient(90deg,#facc15,#ca8a04); }
.bar-low       { background:linear-gradient(90deg,#4ade80,#16a34a); }
.bar-very-low  { background:linear-gradient(90deg,#38bdf8,#0284c7); }
.hc-expl { font-size: 0.76rem; color: #475569; line-height: 1.5; }
.detail-panel { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.2rem 1.4rem; margin-top: 0.5rem; }
.detail-panel h4 { font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #64748b; margin: 0 0 0.75rem; }
.ind-row { display: flex; align-items: center; justify-content: space-between; padding: 0.42rem 0; border-bottom: 1px solid #f1f5f9; font-size: 0.83rem; }
.ind-row:last-child { border-bottom: none; }
.ind-name  { color: #334155; font-weight: 500; flex: 1; }
.ind-raw   { color: #64748b; font-size: 0.79rem; text-align: right; margin-right: 0.9rem; }
.ind-norm  { background: #01244a; color: white; border-radius: 10px; padding: 0.1rem 0.5rem; font-size: 0.71rem; font-weight: 600; min-width: 38px; text-align: center; }
.method-box { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.1rem 1.4rem; margin-top: 0.5rem; }
.method-box h4 { font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #64748b; margin: 0 0 0.7rem; }
.method-row { display: flex; justify-content: space-between; align-items: center; padding: 0.42rem 0; border-bottom: 1px solid #e2e8f0; font-size: 0.83rem; }
.method-row:last-child { border-bottom: none; }
.method-name { color: #334155; font-weight: 500; }
.method-weight { background: #01244a; color: white; border-radius: 12px; padding: 0.12rem 0.55rem; font-size: 0.74rem; font-weight: 600; }
.error-box { background: #fef2f2; border: 1px solid #fecaca; border-radius: 10px; padding: 1rem 1.2rem; color: #991b1b; font-size: 0.87rem; }
.unavail-card { background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 12px; padding: 1rem 1.1rem; display: flex; align-items: center; gap: 0.65rem; color: #94a3b8; font-size: 0.82rem; min-height: 130px; }
.footer { text-align: center; color: #94a3b8; font-size: 0.77rem; margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #e2e8f0; line-height: 1.8; }
.footer a { color: #0085ca; text-decoration: none; }
.map-section { border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; margin-bottom: 1.25rem; }
.map-label { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #64748b; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)


# ── LOAD SCORE DATA ───────────────────────────────────────────────────────────
@st.cache_data
def load_csv(filename):
    try:
        df = pd.read_csv(filename)
        df["pincode"] = df["pincode"].astype(str).str.strip().str.zfill(6)
        return df
    except FileNotFoundError:
        return None

df_cyclone  = load_csv("precomputed_cyclone_scores.csv")
df_heat     = load_csv("precomputed_heat_scores.csv")
df_drought  = load_csv("precomputed_drought_scores.csv")
df_flood    = load_csv("precomputed_flood_scores.csv")
df_rainfall = load_csv("precomputed_rainfall_scores.csv")


# ── LOAD DISTRICT GEOJSON (cached, fetched once from GitHub) ──────────────────
@st.cache_data(show_spinner=False)
def load_district_geojson():
    """
    Loads India district boundaries from datta07/INDIAN-SHAPEFILES on GitHub.
    Free, no login, ~39MB. Cached after first load.
    Returns a dict: { "DISTRICT_NAME|STATE_NAME": geojson_feature }
    """
    url = "https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/INDIA/INDIA_DISTRICTS.geojson"
    try:
        resp = requests.get(url, timeout=30)
        gj   = resp.json()
        # Build lookup dict — keys are "DISTRICT|STATE" uppercased
        lookup = {}
        for feature in gj["features"]:
            props = feature.get("properties", {})
            # Try common property name variants in this GeoJSON
            dist  = (props.get("DISTRICT")  or props.get("district")  or
                     props.get("NAME_2")     or props.get("Dist_Name") or "").upper().strip()
            state = (props.get("ST_NM")      or props.get("state")     or
                     props.get("NAME_1")     or props.get("State_Name") or "").upper().strip()
            if dist:
                lookup[f"{dist}|{state}"] = feature
                lookup[dist] = feature          # fallback without state
        return lookup, gj
    except Exception as e:
        return {}, None

with st.spinner("Loading district boundaries..."):
    district_lookup, full_geojson = load_district_geojson()


# ── RISK COLOUR MAP ───────────────────────────────────────────────────────────
RISK_COLOURS = {
    "Very High": "#dc2626",
    "High":      "#ea580c",
    "Moderate":  "#ca8a04",
    "Low":       "#16a34a",
    "Very Low":  "#0284c7",
}

def risk_fill(level):
    return RISK_COLOURS.get(level, "#94a3b8")


# ── BUILD FOLIUM MAP ──────────────────────────────────────────────────────────
def build_map(lat, lon, district, state, cyclone_level):
    """
    Returns a folium.Map with:
      - District boundary polygon highlighted
      - PIN centroid marker with circle
    """
    m = folium.Map(
        location=[lat, lon],
        zoom_start=9,
        tiles="CartoDB positron",
        zoom_control=True,
        scrollWheelZoom=False,
    )

    # ── Try to find and draw district boundary ────────────────────────────────
    dist_upper  = district.upper().strip()
    state_upper = state.upper().strip()
    feature     = (district_lookup.get(f"{dist_upper}|{state_upper}") or
                   district_lookup.get(dist_upper))

    fill_color = risk_fill(cyclone_level)

    if feature:
        folium.GeoJson(
            data=feature,
            name="District boundary",
            style_function=lambda x, fc=fill_color: {
                "fillColor":   fc,
                "color":       fc,
                "weight":      2.5,
                "fillOpacity": 0.15,
                "dashArray":   "4 2",
            },
            tooltip=folium.Tooltip(f"{district.title()}, {state.title()}",
                                   sticky=False),
        ).add_to(m)

        # Fit map to district bounds
        try:
            coords = feature["geometry"]["coordinates"]
            geom_type = feature["geometry"]["type"]
            all_pts = []
            if geom_type == "Polygon":
                all_pts = coords[0]
            elif geom_type == "MultiPolygon":
                for poly in coords:
                    all_pts.extend(poly[0])
            if all_pts:
                lons = [p[0] for p in all_pts]
                lats = [p[1] for p in all_pts]
                m.fit_bounds([[min(lats), min(lons)], [max(lats), max(lons)]])
        except Exception:
            pass
    else:
        # No boundary found — just centre on the point
        m.location = [lat, lon]

    # ── 10 km analysis radius circle ─────────────────────────────────────────
    folium.Circle(
        location=[lat, lon],
        radius=10000,
        color=fill_color,
        weight=1.5,
        fill=True,
        fill_color=fill_color,
        fill_opacity=0.08,
        tooltip="10 km analysis radius",
    ).add_to(m)

    # ── PIN centroid marker ───────────────────────────────────────────────────
    folium.CircleMarker(
        location=[lat, lon],
        radius=7,
        color="white",
        weight=2.5,
        fill=True,
        fill_color=fill_color,
        fill_opacity=1.0,
        tooltip=f"PIN centroid",
    ).add_to(m)

    return m


# ── HELPERS ───────────────────────────────────────────────────────────────────
def rc(level): return level.lower().replace(" ", "-")

def hazard_card(icon, title, score, level, explanation):
    css = rc(level)
    return f"""<div class="hazard-card {css}">
        <div class="hc-top">
            <div><div style="font-size:1.25rem">{icon}</div><div class="hc-label">{title}</div></div>
            <div style="text-align:right">
                <div class="hc-score">{score:.1f}</div>
                <span class="hc-badge badge-{css}">{level}</span>
            </div>
        </div>
        <div class="bar-wrap"><div class="bar-fill bar-{css}" style="width:{score}%"></div></div>
        <div class="hc-expl">{explanation}</div>
    </div>"""

def unavail_card(icon, title):
    return f"""<div class="unavail-card">
        <span style="font-size:1.3rem">{icon}</span>
        <div><strong style="color:#64748b;font-size:0.83rem">{title}</strong><br>
        Data not yet loaded — run the precomputation script to enable.</div>
    </div>"""

def ind_row(name, raw_val, norm_val):
    return f"""<div class="ind-row">
        <span class="ind-name">{name}</span>
        <span class="ind-raw">{raw_val}</span>
        <span class="ind-norm">{norm_val:.0f}</span>
    </div>"""

def lookup(df, pin_str):
    if df is None: return None
    rows = df[df["pincode"] == pin_str]
    return rows.iloc[0] if not rows.empty else None


# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>India Physical Risk Explorer</h1>
    <p>PIN code–level climate hazard scores · Cyclone · Heat · Drought · Flood · Extreme Rainfall</p>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    pin_input = st.text_input("PIN code", placeholder="Enter a 6-digit PIN code (e.g. 751001)",
                               label_visibility="collapsed", max_chars=6)
with col2:
    search = st.button("Search →", use_container_width=True, type="primary")


# ── RENDER ─────────────────────────────────────────────────────────────────────
def render_all(pin):
    pin_str = str(pin).strip().zfill(6)
    c = lookup(df_cyclone, pin_str)
    if c is None:
        st.markdown('<div class="error-box">⚠️ PIN code not found. Please check and try again.</div>',
                    unsafe_allow_html=True)
        return

    lat      = float(c["latitude"])
    lon      = float(c["longitude"])
    state    = str(c["statename"]).title()
    district = str(c["district"]).title()

    # Location pill
    st.markdown(f'<div class="location-pill">📍 {district}, {state} &nbsp;·&nbsp; PIN {pin_str}</div>',
                unsafe_allow_html=True)

    # ── MAP ───────────────────────────────────────────────────────────────────
    st.markdown('<div class="map-label">📍 Location Map</div>', unsafe_allow_html=True)
    m = build_map(lat, lon, district, state, str(c["risk_level"]))
    with st.container():
        st_folium(m, width="100%", height=320, returned_objects=[])

    st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)

    # ── HAZARD CARDS ──────────────────────────────────────────────────────────
    h  = lookup(df_heat,     pin_str)
    d  = lookup(df_drought,  pin_str)
    fl = lookup(df_flood,    pin_str)
    r  = lookup(df_rainfall, pin_str)

    # Row 1: Cyclone · Heat · Drought
    c_html  = hazard_card("🌀","Cyclone", float(c["cyclone_score"]), str(c["risk_level"]), str(c["cyclone_explanation"]))
    h_html  = hazard_card("🌡️","Heat",   float(h["heat_score"]),   str(h["risk_level"]), str(h["heat_explanation"]))    if h  else unavail_card("🌡️","Heat")
    d_html  = hazard_card("🏜️","Drought",float(d["drought_score"]),str(d["risk_level"]), str(d["drought_explanation"])) if d  else unavail_card("🏜️","Drought")
    st.markdown(f'<div class="hazard-row-3">{c_html}{h_html}{d_html}</div>', unsafe_allow_html=True)

    # Row 2: Flood · Extreme Rainfall
    fl_html = hazard_card("🌊","Flood",           float(fl["flood_score"]),   str(fl["risk_level"]), str(fl["flood_explanation"]))    if fl else unavail_card("🌊","Flood")
    r_html  = hazard_card("🌧️","Extreme Rainfall",float(r["rainfall_score"]), str(r["risk_level"]), str(r["rainfall_explanation"]))  if r  else unavail_card("🌧️","Extreme Rainfall")
    st.markdown(f'<div class="hazard-row-2">{fl_html}{r_html}</div>', unsafe_allow_html=True)

    # ── SUB-INDICATOR TABS ────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### Sub-indicators")
    tabs = st.tabs(["🌀 Cyclone", "🌡️ Heat", "🏜️ Drought", "🌊 Flood", "🌧️ Rainfall"])

    with tabs[0]:
        st.markdown(f"""<div class="detail-panel">
            <h4>Cyclone &nbsp;<span style="color:#0f172a;font-weight:700">{float(c["cyclone_score"]):.1f} / 100</span></h4>
            {ind_row("Track density (storm track points within 300 km)", f"{int(c['track_count']):,} pts", float(c['track_norm']))}
            {ind_row("Max wind exposure (1-min sustained wind)", f"{float(c['max_wind']):.0f} kt", float(c['wind_norm']))}
            {ind_row("Distance-decayed exposure (wind / dist²)", f"{float(c['decay_score']):.4f}", float(c['decay_norm']))}
        </div>""", unsafe_allow_html=True)
        st.caption("NOAA IBTrACS v04r00 NI basin (1842–2024) · Consistent data from 1980")

    with tabs[1]:
        if h is not None:
            st.markdown(f"""<div class="detail-panel">
                <h4>Heat &nbsp;<span style="color:#0f172a;font-weight:700">{float(h["heat_score"]):.1f} / 100</span></h4>
                {ind_row("Hot days frequency (% days Tmax > 35°C)", f"{float(h['hot_days_pct']):.1f}%", float(h['hot_days_norm']))}
                {ind_row("Warm nights frequency (% nights Tmin > 25°C)", f"{float(h['warm_nights_pct']):.1f}%", float(h['warm_nights_norm']))}
                {ind_row("Recent heat trend (°C per decade)", f"{float(h['heat_trend_decade']):+.2f}°C", float(h['heat_trend_norm']))}
            </div>""", unsafe_allow_html=True)
            st.caption("ERA5-Land 2m temperature · 1990–2024")
        else:
            st.info("Run `compute_heat_score.py` to generate heat scores.")

    with tabs[2]:
        if d is not None:
            st.markdown(f"""<div class="detail-panel">
                <h4>Drought &nbsp;<span style="color:#0f172a;font-weight:700">{float(d["drought_score"]):.1f} / 100</span></h4>
                {ind_row("Longest dry spell (90th pct, consecutive dry months)", f"{float(d['dry_spell_months']):.1f} months", float(d['dry_spell_norm']))}
                {ind_row("Monsoon rainfall variability (CV, Jun–Sep)", f"{float(d['monsoon_cv']):.3f}", float(d['monsoon_cv_norm']))}
                {ind_row("Rainfall deficit frequency (% years < 80% of mean)", f"{float(d['deficit_freq_pct']):.1f}%", float(d['deficit_norm']))}
            </div>""", unsafe_allow_html=True)
            st.caption("CHIRPS monthly · 1991–2024")
        else:
            st.info("Run `compute_drought_score.py` to generate drought scores.")

    with tabs[3]:
        if fl is not None:
            st.markdown(f"""<div class="detail-panel">
                <h4>Flood &nbsp;<span style="color:#0f172a;font-weight:700">{float(fl["flood_score"]):.1f} / 100</span></h4>
                {ind_row("Flood hazard area share (JRC, any return period)", f"{float(fl['flood_hazard_pct']):.1f}%", float(fl['flood_hazard_norm']))}
                {ind_row("Low elevation share (below 10m, SRTM)", f"{float(fl['low_elev_pct']):.1f}%", float(fl['low_elev_norm']))}
                {ind_row("Surface water proximity (within 2 km, JRC GSW)", f"{float(fl['water_prox_pct']):.1f}%", float(fl['water_prox_norm']))}
                {ind_row("Heavy rainfall contribution", f"{float(fl['rain_contribution']):.1f}", float(fl['rain_norm']))}
            </div>""", unsafe_allow_html=True)
            st.caption("JRC CEMS-GloFAS Flood Hazard v2.1 · USGS SRTM · JRC GSW 1.4")
        else:
            st.info("Complete the GEE export and run `compute_flood_score_v2.py`.")

    with tabs[4]:
        if r is not None:
            st.markdown(f"""<div class="detail-panel">
                <h4>Extreme Rainfall &nbsp;<span style="color:#0f172a;font-weight:700">{float(r["rainfall_score"]):.1f} / 100</span></h4>
                {ind_row("Rx1day — 90th pct annual max 1-day rainfall", f"{float(r['rx1day_p90']):.1f} mm", float(r['rx1day_norm']))}
                {ind_row("Rx5day — 90th pct annual max 5-day rainfall", f"{float(r['rx5day_p90']):.1f} mm", float(r['rx5day_norm']))}
                {ind_row("Heavy rain days trend (>50 mm/day, per decade)", f"{float(r['heavy_rain_trend']):+.2f} days", float(r['heavy_trend_norm']))}
            </div>""", unsafe_allow_html=True)
            st.caption("CHIRPS daily v2.0 · 1981–2024 · ETCCDI indices")
        else:
            st.info("Run `compute_rainfall_score.py` to generate extreme rainfall scores.")


# ── RUN ────────────────────────────────────────────────────────────────────────
if pin_input and (search or len(pin_input) == 6):
    if not pin_input.isdigit() or len(pin_input) != 6:
        st.markdown('<div class="error-box">⚠️ Please enter a valid 6-digit PIN code (numbers only).</div>',
                    unsafe_allow_html=True)
    else:
        render_all(pin_input)


# ── METHODOLOGY ───────────────────────────────────────────────────────────────
with st.expander("📐 Scoring methodology"):
    st.markdown("""
    <div class="method-box">
        <h4>🌀 Cyclone &nbsp;<span style="font-size:0.73rem;font-weight:400;color:#94a3b8">NOAA IBTrACS v04r00 NI basin · 1842–2024</span></h4>
        <div class="method-row"><span class="method-name">Track density — storm track points within 300 km</span><span class="method-weight">40%</span></div>
        <div class="method-row"><span class="method-name">Maximum wind exposure — highest 1-min wind within 200 km</span><span class="method-weight">35%</span></div>
        <div class="method-row"><span class="method-name">Distance-decayed exposure — wind / dist² summed, log-scaled</span><span class="method-weight">25%</span></div>
    </div><br>
    <div class="method-box">
        <h4>🌡️ Heat &nbsp;<span style="font-size:0.73rem;font-weight:400;color:#94a3b8">ERA5-Land 2m temperature · 1990–2024</span></h4>
        <div class="method-row"><span class="method-name">Hot days frequency — % days with Tmax > 35°C</span><span class="method-weight">40%</span></div>
        <div class="method-row"><span class="method-name">Warm nights frequency — % nights with Tmin > 25°C</span><span class="method-weight">35%</span></div>
        <div class="method-row"><span class="method-name">Recent heat trend — °C per decade (linear regression)</span><span class="method-weight">25%</span></div>
    </div><br>
    <div class="method-box">
        <h4>🏜️ Drought &nbsp;<span style="font-size:0.73rem;font-weight:400;color:#94a3b8">CHIRPS monthly · 1991–2024</span></h4>
        <div class="method-row"><span class="method-name">Longest dry spell — 90th pct annual max consecutive dry months</span><span class="method-weight">35%</span></div>
        <div class="method-row"><span class="method-name">Monsoon variability — CV of Jun–Sep rainfall (1991–2020)</span><span class="method-weight">30%</span></div>
        <div class="method-row"><span class="method-name">Rainfall deficit frequency — % years with rainfall &lt; 80% of mean</span><span class="method-weight">30%</span></div>
    </div><br>
    <div class="method-box">
        <h4>🌊 Flood &nbsp;<span style="font-size:0.73rem;font-weight:400;color:#94a3b8">JRC Flood Hazard v2.1 · SRTM · JRC GSW</span></h4>
        <div class="method-row"><span class="method-name">Flood hazard area share — % area in JRC flood zones (any return period)</span><span class="method-weight">40%</span></div>
        <div class="method-row"><span class="method-name">Low elevation share — % area below 10m (SRTM)</span><span class="method-weight">25%</span></div>
        <div class="method-row"><span class="method-name">Surface water proximity — % area within 2 km of surface water</span><span class="method-weight">20%</span></div>
        <div class="method-row"><span class="method-name">Heavy rainfall contribution — from extreme rainfall score</span><span class="method-weight">15%</span></div>
    </div><br>
    <div class="method-box">
        <h4>🌧️ Extreme Rainfall &nbsp;<span style="font-size:0.73rem;font-weight:400;color:#94a3b8">CHIRPS daily · 1981–2024 · ETCCDI indices</span></h4>
        <div class="method-row"><span class="method-name">Rx1day — 90th pct of annual maximum 1-day rainfall</span><span class="method-weight">40%</span></div>
        <div class="method-row"><span class="method-name">Rx5day — 90th pct of annual maximum 5-day rolling rainfall</span><span class="method-weight">35%</span></div>
        <div class="method-row"><span class="method-name">Heavy rain trend — days/year with rain > 50 mm (linear trend)</span><span class="method-weight">25%</span></div>
    </div><br>
    <p style="font-size:0.79rem;color:#64748b;margin:0">All sub-indicators are min-max normalised (0–100) across all ~19,550 India PIN codes, then combined as a weighted sum. Risk levels: Very Low (0–20) · Low (20–40) · Moderate (40–60) · High (60–80) · Very High (80–100).</p>
    """, unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <strong>Data sources</strong><br>
    Cyclone: <a href="https://www.ncei.noaa.gov/products/international-best-track-archive" target="_blank">NOAA IBTrACS v04r00 NI basin</a> (1842–2024) · Public domain<br>
    Heat: <a href="https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land" target="_blank">ERA5-Land</a> via Copernicus CDS · Copernicus License<br>
    Drought + Rainfall: <a href="https://www.chc.ucsb.edu/data/chirps" target="_blank">CHIRPS v2.0</a> (1981–2024) · Public domain<br>
    Flood: <a href="https://developers.google.com/earth-engine/datasets/catalog/JRC_CEMS_GLOFAS_FloodHazard_v2_1" target="_blank">JRC CEMS-GloFAS Flood Hazard v2.1</a> ·
    <a href="https://global-surface-water.appspot.com/" target="_blank">JRC GSW 1.4</a> ·
    <a href="https://www.usgs.gov/centers/eros/science/usgs-eros-archive-digital-elevation-shuttle-radar-topography-mission-srtm" target="_blank">USGS SRTM</a><br>
    District boundaries: <a href="https://github.com/datta07/INDIAN-SHAPEFILES" target="_blank">datta07/INDIAN-SHAPEFILES</a> · Open data<br>
    PIN code coordinates: India Post via Open Government Data Platform India · GOI Open Data License<br><br>
    Scores are historical hazard estimates only and do not constitute official risk assessments.
</div>""", unsafe_allow_html=True)
