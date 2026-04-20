import streamlit as st
import pandas as pd
import numpy as np

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Physical Risk Explorer",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body { background-color: #ffffff; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1.5rem 4rem; max-width: 800px; }

/* ── Hero ── */
.hero {
    background: #01244a;
    border-radius: 10px;
    padding: 1.75rem 1.5rem;
    margin-bottom: 1.5rem;
}
.hero h1 { color: #f0f9ff; font-size: 1.7rem; font-weight: 700; margin: 0 0 0.3rem; letter-spacing: -0.02em; }
.hero p  { color: #94a3b8; font-size: 0.9rem; margin: 0; }

/* ── Search ── */
.stTextInput > div > div > input {
    border-radius: 6px !important;
    border: 1px solid #dee7f0 !important;
    font-size: 1rem !important;
}
.stButton>button {
    background-color: #01244a;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 600;
}
.stButton>button:hover { background-color: #0085ca; color: white; }

/* ── Location pill ── */
.location-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #dee7f0;
    border: 1px solid #5c8bb4;
    border-radius: 20px;
    padding: 0.35rem 0.9rem;
    font-size: 0.82rem;
    color: #01244a;
    font-weight: 500;
    margin-bottom: 1rem;
}

/* ── Hazard grid (4 cards) ── */
.hazard-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.9rem;
    margin: 1.1rem 0;
}
.hazard-card {
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    border: 1px solid;
    cursor: default;
}
.hazard-card.very-high { background:#fff5f5; border-color:#fca5a5; }
.hazard-card.high      { background:#fff7ed; border-color:#fdba74; }
.hazard-card.moderate  { background:#fefce8; border-color:#fde047; }
.hazard-card.low       { background:#f0fdf4; border-color:#86efac; }
.hazard-card.very-low  { background:#f0f9ff; border-color:#7dd3fc; }

.hc-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}
.hc-icon   { font-size: 1.4rem; }
.hc-score  { font-size: 2rem; font-weight: 700; letter-spacing: -0.04em; line-height: 1; }
.hc-label  { font-size: 0.68rem; font-weight: 600; text-transform: uppercase;
             letter-spacing: 0.07em; color: #64748b; margin-top: 0.15rem; }
.hc-badge  { font-size: 0.72rem; font-weight: 600; padding: 0.2rem 0.6rem;
             border-radius: 12px; white-space: nowrap; }

.badge-very-high { background:#fee2e2; color:#b91c1c; }
.badge-high      { background:#ffedd5; color:#c2410c; }
.badge-moderate  { background:#fef9c3; color:#a16207; }
.badge-low       { background:#dcfce7; color:#15803d; }
.badge-very-low  { background:#e0f2fe; color:#0369a1; }

/* Bar */
.bar-wrap { background:#e2e8f0; border-radius:4px; height:5px; margin:0.5rem 0 0.6rem; overflow:hidden; }
.bar-fill  { height:100%; border-radius:4px; }
.bar-very-high { background:linear-gradient(90deg,#f87171,#dc2626); }
.bar-high      { background:linear-gradient(90deg,#fb923c,#ea580c); }
.bar-moderate  { background:linear-gradient(90deg,#facc15,#ca8a04); }
.bar-low       { background:linear-gradient(90deg,#4ade80,#16a34a); }
.bar-very-low  { background:linear-gradient(90deg,#38bdf8,#0284c7); }

.hc-expl {
    font-size: 0.78rem;
    color: #475569;
    line-height: 1.55;
}

/* ── Detail panel (shown on tab click) ── */
.detail-panel {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.3rem 1.5rem;
    margin-top: 0.5rem;
}
.detail-panel h4 {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    margin: 0 0 0.8rem;
}

/* ── Indicator row ── */
.ind-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.45rem 0;
    border-bottom: 1px solid #f1f5f9;
    font-size: 0.84rem;
}
.ind-row:last-child { border-bottom: none; }
.ind-name  { color: #334155; font-weight: 500; flex: 1; }
.ind-raw   { color: #64748b; font-size: 0.8rem; text-align: right; margin-right: 1rem; }
.ind-norm  {
    background: #01244a;
    color: white;
    border-radius: 10px;
    padding: 0.12rem 0.55rem;
    font-size: 0.72rem;
    font-weight: 600;
    min-width: 40px;
    text-align: center;
}

/* ── Methodology box ── */
.method-box {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-top: 2rem;
}
.method-box h4 {
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    margin: 0 0 0.75rem;
}
.method-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid #e2e8f0;
    font-size: 0.84rem;
}
.method-row:last-child { border-bottom: none; }
.method-name { color: #334155; font-weight: 500; }
.method-weight {
    background: #01244a;
    color: white;
    border-radius: 12px;
    padding: 0.15rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
}

/* ── Error ── */
.error-box {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    color: #991b1b;
    font-size: 0.88rem;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.78rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e2e8f0;
    line-height: 1.8;
}
.footer a { color: #0085ca; text-decoration: none; }

/* ── Unavailable card ── */
.unavail-card {
    background: #f8fafc;
    border: 1px dashed #cbd5e1;
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.7rem;
    color: #94a3b8;
    font-size: 0.84rem;
}
</style>
""", unsafe_allow_html=True)


# ── LOAD DATA ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_cyclone():
    df = pd.read_csv("precomputed_cyclone_scores.csv")
    df["pincode"] = df["pincode"].astype(str).str.strip().str.zfill(6)
    return df

@st.cache_data
def load_heat():
    try:
        df = pd.read_csv("precomputed_heat_scores.csv")
        df["pincode"] = df["pincode"].astype(str).str.strip().str.zfill(6)
        return df
    except FileNotFoundError:
        return None

@st.cache_data
def load_drought():
    try:
        df = pd.read_csv("precomputed_drought_scores.csv")
        df["pincode"] = df["pincode"].astype(str).str.strip().str.zfill(6)
        return df
    except FileNotFoundError:
        return None

@st.cache_data
def load_flood():
    try:
        df = pd.read_csv("precomputed_flood_scores.csv")
        df["pincode"] = df["pincode"].astype(str).str.strip().str.zfill(6)
        return df
    except FileNotFoundError:
        return None

df_cyclone = load_cyclone()
df_heat    = load_heat()
df_drought = load_drought()
df_flood   = load_flood()


# ── HELPERS ───────────────────────────────────────────────────────────────────
def rc(level):
    return level.lower().replace(" ", "-")

def hazard_card_html(icon, title, score, level, explanation, available=True):
    if not available:
        return f"""
        <div class="unavail-card">
            <span style="font-size:1.4rem">{icon}</span>
            <div>
                <strong style="color:#64748b">{title}</strong><br>
                Data not yet loaded — run the precomputation script to enable this hazard.
            </div>
        </div>
        """
    css = rc(level)
    return f"""
    <div class="hazard-card {css}">
        <div class="hc-top">
            <div>
                <div style="font-size:1.3rem">{icon}</div>
                <div class="hc-label">{title}</div>
            </div>
            <div style="text-align:right">
                <div class="hc-score">{score:.1f}</div>
                <span class="hc-badge badge-{css}">{level}</span>
            </div>
        </div>
        <div class="bar-wrap">
            <div class="bar-fill bar-{css}" style="width:{score}%"></div>
        </div>
        <div class="hc-expl">{explanation}</div>
    </div>
    """

def ind_row(name, raw_val, norm_val):
    return f"""
    <div class="ind-row">
        <span class="ind-name">{name}</span>
        <span class="ind-raw">{raw_val}</span>
        <span class="ind-norm">{norm_val:.0f}</span>
    </div>
    """


# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>India Physical Risk Explorer</h1>
    <p>PIN code–level climate hazard scores · Cyclone · Heat · Drought · Flood</p>
</div>
""", unsafe_allow_html=True)

# ── SEARCH ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    pin_input = st.text_input(
        label="PIN code",
        placeholder="Enter a 6-digit PIN code (e.g. 751001)",
        label_visibility="collapsed",
        max_chars=6,
    )
with col2:
    search = st.button("Search →", use_container_width=True, type="primary")


# ── RENDER RESULTS ─────────────────────────────────────────────────────────────
def render_all(pin):
    pin_str = str(pin).strip().zfill(6)

    # Cyclone — always required
    c_row = df_cyclone[df_cyclone["pincode"] == pin_str]
    if c_row.empty:
        st.markdown("""
        <div class="error-box">
            ⚠️ PIN code not found in database. Please check the number and try again.
        </div>""", unsafe_allow_html=True)
        return

    c = c_row.iloc[0]
    state    = str(c["statename"]).title()
    district = str(c["district"]).title()

    # Location pill
    st.markdown(f"""
    <div class="location-pill">📍 {district}, {state} &nbsp;·&nbsp; PIN {pin_str}</div>
    """, unsafe_allow_html=True)

    # ── Build 4 hazard cards ───────────────────────────────────────────────────

    # Cyclone
    c_score = float(c["cyclone_score"])
    c_level = str(c["risk_level"])
    c_expl  = str(c["cyclone_explanation"])

    # Heat
    h_available = df_heat is not None
    if h_available:
        h_row = df_heat[df_heat["pincode"] == pin_str]
        if not h_row.empty:
            h = h_row.iloc[0]
            h_score = float(h["heat_score"])
            h_level = str(h["risk_level"])
            h_expl  = str(h["heat_explanation"])
        else:
            h_available = False

    # Drought
    d_available = df_drought is not None
    if d_available:
        d_row = df_drought[df_drought["pincode"] == pin_str]
        if not d_row.empty:
            d = d_row.iloc[0]
            d_score = float(d["drought_score"])
            d_level = str(d["risk_level"])
            d_expl  = str(d["drought_explanation"])
        else:
            d_available = False

    # Flood
    fl_available = df_flood is not None
    if fl_available:
        fl_row = df_flood[df_flood["pincode"] == pin_str]
        if not fl_row.empty:
            fl = fl_row.iloc[0]
            fl_score = float(fl["flood_score"])
            fl_level = str(fl["risk_level"])
            fl_expl  = str(fl["flood_explanation"])
        else:
            fl_available = False

    # ── 2×2 grid ──────────────────────────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(hazard_card_html("🌀", "Cyclone", c_score, c_level, c_expl), unsafe_allow_html=True)
        st.markdown(
            hazard_card_html("🏜️", "Drought", d_score, d_level, d_expl) if d_available
            else hazard_card_html("🏜️", "Drought", 0, "N/A", "", available=False),
            unsafe_allow_html=True
        )

    with col_right:
        st.markdown(
            hazard_card_html("🌡️", "Heat", h_score, h_level, h_expl) if h_available
            else hazard_card_html("🌡️", "Heat", 0, "N/A", "", available=False),
            unsafe_allow_html=True
        )
        st.markdown(
            hazard_card_html("🌊", "Flood", fl_score, fl_level, fl_expl) if fl_available
            else hazard_card_html("🌊", "Flood", 0, "N/A", "", available=False),
            unsafe_allow_html=True
        )

    # ── Detail expandable sections ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### Sub-indicators")

    tab1, tab2, tab3, tab4 = st.tabs(["🌀 Cyclone", "🌡️ Heat", "🏜️ Drought", "🌊 Flood"])

    with tab1:
        st.markdown(f"""
        <div class="detail-panel">
            <h4>Cyclone Sub-indicators &nbsp;<span style="color:#0f172a;font-weight:700">{c_score:.1f} / 100</span></h4>
            {ind_row("Track density (storm track points within 200 km)", f"{int(c['track_count']):,} pts", float(c['track_norm']))}
            {ind_row("Max wind exposure (1-min sustained wind)", f"{float(c['max_wind']):.0f} kt", float(c['wind_norm']))}
            {ind_row("Distance-decayed exposure (wind/dist²)", f"{float(c['decay_score']):.4f}", float(c['decay_norm']))}
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        if h_available:
            st.markdown(f"""
            <div class="detail-panel">
                <h4>Heat Sub-indicators &nbsp;<span style="color:#0f172a;font-weight:700">{h_score:.1f} / 100</span></h4>
                {ind_row("Hot days frequency (% days Tmax > 35°C)", f"{float(h['hot_days_pct']):.1f}%", float(h['hot_days_norm']))}
                {ind_row("Warm nights frequency (% nights Tmin > 25°C)", f"{float(h['warm_nights_pct']):.1f}%", float(h['warm_nights_norm']))}
                {ind_row("Recent heat trend (°C per decade)", f"{float(h['heat_trend_decade']):+.2f}°C", float(h['heat_trend_norm']))}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Heat score data not yet available. Run `compute_heat_score.py` to generate it.")

    with tab3:
        if d_available:
            st.markdown(f"""
            <div class="detail-panel">
                <h4>Drought Sub-indicators &nbsp;<span style="color:#0f172a;font-weight:700">{d_score:.1f} / 100</span></h4>
                {ind_row("Longest dry spell (90th pct, consecutive dry months)", f"{float(d['dry_spell_months']):.1f} months", float(d['dry_spell_norm']))}
                {ind_row("Monsoon rainfall variability (CV, Jun–Sep)", f"{float(d['monsoon_cv']):.3f}", float(d['monsoon_cv_norm']))}
                {ind_row("Rainfall deficit frequency (% years < 80% of mean)", f"{float(d['deficit_freq_pct']):.1f}%", float(d['deficit_norm']))}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Drought score data not yet available. Run `compute_drought_score.py` to generate it.")

    with tab4:
        if fl_available:
            st.markdown(f"""
            <div class="detail-panel">
                <h4>Flood Sub-indicators &nbsp;<span style="color:#0f172a;font-weight:700">{fl_score:.1f} / 100</span></h4>
                {ind_row("Flood hazard area share (JRC flood zones)", f"{float(fl['flood_hazard_pct']):.1f}%", float(fl['flood_hazard_norm']))}
                {ind_row("Low elevation share (below 10m, Copernicus DEM)", f"{float(fl['low_elev_pct']):.1f}%", float(fl['low_elev_norm']))}
                {ind_row("Surface water proximity (within 2km, JRC GSW)", f"{float(fl['water_prox_pct']):.1f}%", float(fl['water_prox_norm']))}
                {ind_row("Heavy rainfall contribution (from drought score)", f"{float(fl['rain_contribution']):.1f}", float(fl['rain_norm']))}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Flood score data not yet available. Run `compute_flood_score.py` to generate it.")


# ── RUN LOOKUP ────────────────────────────────────────────────────────────────
if pin_input and (search or len(pin_input) == 6):
    if not pin_input.isdigit() or len(pin_input) != 6:
        st.markdown("""
        <div class="error-box">⚠️ Please enter a valid 6-digit PIN code containing only numbers.</div>
        """, unsafe_allow_html=True)
    else:
        render_all(pin_input)


# ── METHODOLOGY ───────────────────────────────────────────────────────────────
with st.expander("📐 Scoring methodology"):
    st.markdown("""
    <div class="method-box">
        <h4>🌀 Cyclone Score</h4>
        <div class="method-row"><span class="method-name">Track density (storm points within 200 km)</span><span class="method-weight">40%</span></div>
        <div class="method-row"><span class="method-name">Maximum wind exposure (1-min sustained)</span><span class="method-weight">35%</span></div>
        <div class="method-row"><span class="method-name">Distance-decayed exposure (wind / dist²)</span><span class="method-weight">25%</span></div>
    </div>
    <br>
    <div class="method-box">
        <h4>🌡️ Heat Score &nbsp;<span style="font-size:0.75rem;font-weight:400;color:#94a3b8">ERA5-Land 2m temperature · 1990–2024</span></h4>
        <div class="method-row"><span class="method-name">Hot days frequency (% days Tmax > 35°C)</span><span class="method-weight">40%</span></div>
        <div class="method-row"><span class="method-name">Warm nights frequency (% nights Tmin > 25°C)</span><span class="method-weight">35%</span></div>
        <div class="method-row"><span class="method-name">Recent heat trend (°C per decade, linear)</span><span class="method-weight">25%</span></div>
    </div>
    <br>
    <div class="method-box">
        <h4>🏜️ Drought Score &nbsp;<span style="font-size:0.75rem;font-weight:400;color:#94a3b8">CHIRPS monthly · 1991–2024</span></h4>
        <div class="method-row"><span class="method-name">Longest dry spell (90th pct, consecutive dry months)</span><span class="method-weight">35%</span></div>
        <div class="method-row"><span class="method-name">Monsoon rainfall variability (CV of Jun–Sep)</span><span class="method-weight">30%</span></div>
        <div class="method-row"><span class="method-name">Rainfall deficit frequency (% years &lt; 80% of mean)</span><span class="method-weight">30%</span></div>
    </div>
    <br>
    <div class="method-box">
        <h4>🌊 Flood Score &nbsp;<span style="font-size:0.75rem;font-weight:400;color:#94a3b8">JRC Flood Hazard · Copernicus DEM · JRC GSW</span></h4>
        <div class="method-row"><span class="method-name">Flood hazard area share (any JRC return period)</span><span class="method-weight">40%</span></div>
        <div class="method-row"><span class="method-name">Low elevation share (below 10m)</span><span class="method-weight">25%</span></div>
        <div class="method-row"><span class="method-name">Surface water proximity (within 2km)</span><span class="method-weight">20%</span></div>
        <div class="method-row"><span class="method-name">Heavy rainfall contribution</span><span class="method-weight">15%</span></div>
    </div>
    <br>
    <p style="font-size:0.8rem;color:#64748b">All sub-indicators are min-max normalised (0–100) across all 19,550 PIN codes in India, then combined as a weighted sum. Risk levels: Very Low (0–20) · Low (20–40) · Moderate (40–60) · High (60–80) · Very High (80–100).</p>
    """, unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <strong>Data sources:</strong><br>
    Cyclone: <a href="https://www.ncei.noaa.gov/products/international-best-track-archive" target="_blank">NOAA IBTrACS v04</a> (1842–2023) · Public domain<br>
    Heat: <a href="https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land" target="_blank">ERA5-Land</a> via Copernicus CDS · Copernicus License<br>
    Drought / Rainfall: <a href="https://www.chc.ucsb.edu/data/chirps" target="_blank">CHIRPS v2.0</a> (1981–2024) · Public domain<br>
    Flood: <a href="https://global-flood-database.cloudstats.ch/" target="_blank">JRC Global Flood Hazard</a> · <a href="https://global-surface-water.appspot.com/" target="_blank">JRC Surface Water</a> · <a href="https://portal.opentopography.org/" target="_blank">Copernicus DEM GLO-30</a><br>
    PIN code coordinates: India Post via Open Government Data Platform India · GOI Open Data License<br><br>
    Scores are historical hazard estimates only and do not constitute official risk assessments.
</div>
""", unsafe_allow_html=True)
