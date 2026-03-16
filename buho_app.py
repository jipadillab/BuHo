"""
╔══════════════════════════════════════════════════════════════╗
║   BuHo — Business with Horses                                ║
║   Plataforma de Analítica Equina Avanzada                    ║
║   Desarrollado por: Jorge Iván Padilla Buritica              ║
║   ORCAS Analítica de Datos                                   ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import random
from datetime import datetime, timedelta
import json
import io

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="BuHo — Business with Horses",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS — Dark Luxury Equestrian Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg-dark:      #0a0c0f;
    --bg-card:      #111418;
    --bg-panel:     #161b22;
    --gold:         #c9a84c;
    --gold-light:   #e8c97a;
    --gold-dim:     #7a6230;
    --teal:         #2dd4bf;
    --teal-dim:     #0d9488;
    --red-accent:   #f43f5e;
    --text-primary: #f0ece0;
    --text-muted:   #8b8680;
    --border:       rgba(201,168,76,0.2);
    --shadow:       0 8px 32px rgba(0,0,0,0.6);
}

/* ── Global ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-dark) !important;
    color: var(--text-primary);
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── Typography ── */
h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: var(--gold) !important; }
.stMarkdown p { color: var(--text-primary); }
label, .stSelectbox label, .stSlider label { color: var(--text-muted) !important; font-size: 0.78rem !important; letter-spacing: 0.08em; text-transform: uppercase; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 22px;
    box-shadow: var(--shadow);
}
[data-testid="metric-container"] label { color: var(--text-muted) !important; font-size: 0.72rem !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--gold-light) !important; font-family: 'Space Mono', monospace; font-size: 1.6rem; }
[data-testid="metric-container"] [data-testid="stMetricDelta"] svg { fill: var(--teal); }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--gold-dim), var(--gold)) !important;
    color: #0a0c0f !important;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    border: none !important;
    border-radius: 8px;
    letter-spacing: 0.05em;
    transition: all 0.25s ease;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--gold), var(--gold-light)) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(201,168,76,0.35);
}

/* ── Selectbox / slider ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
.stSlider [data-baseweb="slider"] div[role="slider"] { background: var(--gold) !important; }
.stSlider div[data-testid="stSliderTrack"] { background: var(--bg-panel) !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tab"] {
    color: var(--text-muted) !important;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.88rem;
    letter-spacing: 0.04em;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom: 2px solid var(--gold) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }

/* ── Section dividers ── */
hr { border-color: var(--border); }

/* ── Upload area ── */
[data-testid="stFileUploader"] {
    border: 1px dashed var(--gold-dim) !important;
    border-radius: 10px;
    background: var(--bg-panel) !important;
}

/* ── Hero header ── */
.buho-hero {
    background: linear-gradient(135deg, #0f1218 0%, #1a1208 50%, #0a0c0f 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.buho-hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(201,168,76,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.buho-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    color: var(--gold);
    letter-spacing: -0.01em;
    line-height: 1.1;
    margin: 0;
}
.buho-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    color: var(--text-muted);
    margin-top: 6px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.buho-badge {
    display: inline-block;
    background: rgba(201,168,76,0.12);
    border: 1px solid var(--gold-dim);
    color: var(--gold-light);
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    padding: 4px 10px;
    border-radius: 4px;
    letter-spacing: 0.1em;
    margin-top: 12px;
}

/* ── Sidebar brand ── */
.sidebar-brand {
    text-align: center;
    padding: 20px 10px 10px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 16px;
}
.sidebar-logo {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    color: var(--gold);
    line-height: 1;
}
.sidebar-tagline {
    font-size: 0.68rem;
    color: var(--text-muted);
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-top: 4px;
}
.sidebar-author {
    font-size: 0.62rem;
    color: var(--gold-dim);
    margin-top: 8px;
}

/* ── Status pill ── */
.status-ok   { color: #22c55e; background: rgba(34,197,94,0.1); padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; border: 1px solid rgba(34,197,94,0.3); }
.status-warn { color: #f59e0b; background: rgba(245,158,11,0.1); padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; border: 1px solid rgba(245,158,11,0.3); }
.status-bad  { color: #f43f5e; background: rgba(244,63,94,0.1);  padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; border: 1px solid rgba(244,63,94,0.3); }

/* ── Info box ── */
.info-box {
    background: var(--bg-panel);
    border-left: 3px solid var(--teal);
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.88rem;
    color: var(--text-primary);
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#   SYNTHETIC DATA GENERATOR
# ══════════════════════════════════════════════

RAZAS = [
    "Criollo Colombiano", "Criollo Colombiano", "Criollo Colombiano",  # oversampled
    "Paso Fino", "Paso Fino",
    "Pura Sangre Inglés", "Cuarto de Milla",
    "Andaluz", "Lusitano", "Árabe",
    "Warmblood Holandés", "Hanoverian",
    "Appaloosa", "Morgan", "Mangalarga Marchador",
]

CABALLOS = [
    "Relámpago", "Viento del Norte", "Aguila Real", "Cafetero", "Mariposa",
    "Centella", "El Zorro", "Palmero", "Serrano", "Cimarrón",
    "Trueno", "Luna Llena", "Vendaval", "Conquistador", "Brisa Fina",
    "Estrella", "Gavilán", "Pampero", "Araucano", "Tambo",
]

PROPIETARIOS = [
    "Hacienda La Esperanza", "Rancho El Roble", "Finca Los Pinos",
    "Establo San Marcos", "Ganadería El Cóndor", "Rancho Andino",
    "Hacienda Bonita", "Establo Real", "Ganadería La Palma", "Finca El Encanto",
]

SEXO = ["Macho", "Hembra", "Macho castrado"]
COLORES = ["Alazán", "Morcillo", "Ruano", "Tordillo", "Bayo", "Pinto", "Palomino"]


@st.cache_data
def generar_datos_equinos(n=120, seed=42):
    rng = np.random.default_rng(seed)

    nombres = rng.choice(CABALLOS + [f"Caballo_{i}" for i in range(50)], n, replace=True)
    razas   = rng.choice(RAZAS, n)
    edades  = rng.integers(2, 18, n)
    pesos   = rng.normal(490, 60, n).clip(280, 700)

    # ── Biomecánica ──────────────────────────
    vel_max   = rng.normal(58, 12, n).clip(25, 90)    # km/h
    vel_trote = rng.normal(18,  4, n).clip(8, 32)
    vel_paso  = rng.normal(10,  2, n).clip(4, 18)

    zancada_m = rng.normal(2.8, 0.4, n).clip(1.5, 4.5)
    cadencia  = rng.normal(148, 18, n).clip(80, 220)  # pasos/min

    # ── Ángulos geométricos (grados) ─────────
    ang_hombro   = rng.normal(52, 6, n).clip(35, 70)
    ang_cadera   = rng.normal(58, 7, n).clip(40, 75)
    ang_rodilla_a = rng.normal(145, 10, n).clip(115, 165)
    ang_rodilla_p = rng.normal(148, 10, n).clip(115, 165)
    ang_menudillo = rng.normal(55, 8, n).clip(35, 80)
    ang_casco     = rng.normal(50, 5, n).clip(38, 65)

    # ── Compensación entre extremidades ──────
    comp_anterior = rng.normal(0, 3.5, n)   # % asimetría
    comp_posterior = rng.normal(0, 3.5, n)
    comp_lateral   = rng.normal(0, 2.5, n)
    indice_simetria = 100 - (np.abs(comp_anterior) + np.abs(comp_posterior)) / 2

    # ── Desplazamiento ────────────────────────
    desp_total_km = rng.uniform(2, 45, n)
    desp_dia_m    = desp_total_km * 1000 / rng.uniform(4, 10, n)

    # ── Fuerza / presión ─────────────────────
    fuerza_ia   = rng.normal(800, 120, n).clip(400, 1200)   # N
    fuerza_ip   = rng.normal(780, 115, n).clip(400, 1200)
    fuerza_da   = rng.normal(810, 125, n).clip(400, 1200)
    fuerza_dp   = rng.normal(795, 118, n).clip(400, 1200)

    # ── Scores compuestos ────────────────────
    score_biomec = (
        0.3 * (indice_simetria / 100) +
        0.25 * (vel_max / 90) +
        0.25 * (zancada_m / 4.5) +
        0.2 * (1 - np.abs(comp_lateral) / 10)
    ) * 100

    # Fechas
    fechas = [datetime(2024, 1, 1) + timedelta(days=int(x))
              for x in rng.integers(0, 365, n)]

    df = pd.DataFrame({
        "Nombre":         nombres,
        "Raza":           razas,
        "Edad (años)":    edades,
        "Sexo":           rng.choice(SEXO, n),
        "Color":          rng.choice(COLORES, n),
        "Peso (kg)":      pesos.round(1),
        "Propietario":    rng.choice(PROPIETARIOS, n),
        "Fecha Evaluación": fechas,

        # Velocidades
        "Vel. Máx (km/h)":   vel_max.round(2),
        "Vel. Trote (km/h)": vel_trote.round(2),
        "Vel. Paso (km/h)":  vel_paso.round(2),

        # Biomecánica
        "Zancada (m)":       zancada_m.round(3),
        "Cadencia (p/min)":  cadencia.round(1),

        # Ángulos
        "Áng. Hombro (°)":   ang_hombro.round(1),
        "Áng. Cadera (°)":   ang_cadera.round(1),
        "Áng. Rod. Ant (°)": ang_rodilla_a.round(1),
        "Áng. Rod. Post (°)":ang_rodilla_p.round(1),
        "Áng. Menudillo (°)":ang_menudillo.round(1),
        "Áng. Casco (°)":    ang_casco.round(1),

        # Compensación
        "Comp. Anterior (%)":  comp_anterior.round(2),
        "Comp. Posterior (%)": comp_posterior.round(2),
        "Comp. Lateral (%)":   comp_lateral.round(2),
        "Índice Simetría (%)": indice_simetria.round(2),

        # Fuerzas
        "Fuerza IE Ant (N)":  fuerza_ia.round(1),
        "Fuerza DE Ant (N)":  fuerza_da.round(1),
        "Fuerza IE Post (N)": fuerza_ip.round(1),
        "Fuerza DE Post (N)": fuerza_dp.round(1),

        # Desplazamiento
        "Desp. Total (km)":   desp_total_km.round(3),
        "Desp. Día (m)":      desp_dia_m.round(1),

        # Score
        "Score Biomecánico":  score_biomec.clip(0, 100).round(2),
    })
    return df


@st.cache_data
def generar_serie_tiempo(caballo_nombre, seed=0):
    rng = np.random.default_rng(seed)
    dias = 90
    fechas = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(dias)]
    base_vel = rng.uniform(45, 70)
    tendencia = np.linspace(0, rng.uniform(-2, 5), dias)
    vel = base_vel + tendencia + rng.normal(0, 2, dias)
    sim_ant = rng.normal(0, 2, dias)
    sim_post = rng.normal(0, 2, dias)
    return pd.DataFrame({
        "Fecha": fechas,
        "Velocidad (km/h)": vel.clip(20, 90),
        "Comp. Anterior (%)": sim_ant,
        "Comp. Posterior (%)": sim_post,
        "Score Biomecánico": (80 + tendencia / 2 + rng.normal(0, 3, dias)).clip(40, 100),
    })


@st.cache_data
def simular_tracker_yolo(n_frames=300, seed=7):
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 10, n_frames)
    # Articulaciones simuladas
    partes = ["Cabeza", "Cuello", "Hombro_I", "Hombro_D", "Codo_I", "Codo_D",
              "Rodilla_I", "Rodilla_D", "Casco_I", "Casco_D", "Cadera", "Cola"]
    data = {"Frame": np.arange(n_frames)}
    for p in partes:
        freq = rng.uniform(0.8, 2.5)
        fase = rng.uniform(0, 2 * np.pi)
        amp  = rng.uniform(10, 60)
        noise = rng.normal(0, 3, n_frames)
        data[f"{p}_x"] = 320 + amp * 3 * t / 10 * n_frames / 300 + noise
        data[f"{p}_y"] = 240 + amp * np.sin(2 * np.pi * freq * t + fase) + noise
    data["Confianza_YOLO"] = rng.uniform(0.72, 0.99, n_frames)
    return pd.DataFrame(data), partes


# ══════════════════════════════════════════════
#   PLOTLY THEME DEFAULTS
# ══════════════════════════════════════════════

PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(22,27,34,0.6)",
        font=dict(color="#f0ece0", family="DM Sans"),
        title_font=dict(color="#c9a84c", family="Playfair Display"),
        xaxis=dict(gridcolor="rgba(201,168,76,0.08)", linecolor="rgba(201,168,76,0.2)"),
        yaxis=dict(gridcolor="rgba(201,168,76,0.08)", linecolor="rgba(201,168,76,0.2)"),
        colorway=["#c9a84c","#2dd4bf","#f43f5e","#818cf8","#fb923c","#34d399","#e8c97a","#67e8f9"],
        legend=dict(bgcolor="rgba(17,20,24,0.8)", bordercolor="rgba(201,168,76,0.2)", borderwidth=1),
    )
)

def apply_theme(fig, title=""):
    fig.update_layout(**PLOTLY_TEMPLATE["layout"])
    if title:
        fig.update_layout(title_text=title, title_font_size=16)
    return fig


# ══════════════════════════════════════════════
#   SIDEBAR
# ══════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div class='sidebar-brand'>
        <div class='sidebar-logo'>🦉 BuHo</div>
        <div class='sidebar-tagline'>Business with Horses</div>
        <div class='sidebar-author'>Jorge Iván Padilla Buritica<br>ORCAS Analítica de Datos</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎛️ Configuración")

    n_caballos = st.slider("Número de registros", 30, 300, 120, 10)
    seed_val   = st.slider("Semilla aleatoria", 1, 100, 42)

    st.markdown("---")
    st.markdown("### 🐴 Filtros Globales")

    df_full = generar_datos_equinos(n_caballos, seed_val)
    razas_disp = ["Todas"] + sorted(df_full["Raza"].unique().tolist())
    raza_sel   = st.selectbox("Raza", razas_disp)

    sexo_sel  = st.multiselect("Sexo", df_full["Sexo"].unique().tolist(), default=df_full["Sexo"].unique().tolist())
    edad_rng  = st.slider("Rango de edad (años)", 2, 18, (2, 18))

    df = df_full.copy()
    if raza_sel != "Todas":
        df = df[df["Raza"] == raza_sel]
    df = df[df["Sexo"].isin(sexo_sel)]
    df = df[(df["Edad (años)"] >= edad_rng[0]) & (df["Edad (años)"] <= edad_rng[1])]

    st.markdown("---")
    st.markdown(f"**Registros activos:** `{len(df)}`")
    st.markdown(f"**Razas en vista:** `{df['Raza'].nunique()}`")

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.65rem; color:#5a5550; text-align:center; padding:8px 0;'>
    v1.0 · 2024<br>Datos sintéticos para demostración<br>
    <span style='color:#7a6230'>ORCAS Analítica de Datos</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#   HERO HEADER
# ══════════════════════════════════════════════

st.markdown("""
<div class='buho-hero'>
    <div class='buho-title'>🦉 BuHo</div>
    <div class='buho-subtitle'>Business with Horses — Plataforma de Analítica Equina</div>
    <div class='buho-badge'>🔬 BIOMECÁNICA · VELOCIDAD · COMPENSACIÓN · ÁNGULOS · YOLO TRACKER</div>
    <div style='margin-top:14px; font-size:0.75rem; color:#7a6230;'>
        Desarrollado por <strong style='color:#c9a84c;'>Jorge Iván Padilla Buritica</strong> &nbsp;·&nbsp; ORCAS Analítica de Datos
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#   TABS PRINCIPALES
# ══════════════════════════════════════════════

tabs = st.tabs([
    "📊 Dashboard General",
    "🐴 Perfil Individual",
    "📐 Biomecánica & Ángulos",
    "⚖️ Compensación",
    "🎯 YOLO Tracker",
    "📁 Datos & Carga",
    "📋 Reporte IA",
])


# ══════════════════════════════════════════════
#  TAB 1 — DASHBOARD GENERAL
# ══════════════════════════════════════════════

with tabs[0]:
    # KPI Row
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("🐴 Caballos Evaluados", len(df), f"+{len(df)-len(df_full)//2}")
    k2.metric("⚡ Vel. Máx Promedio", f"{df['Vel. Máx (km/h)'].mean():.1f} km/h")
    k3.metric("📐 Simetría Promedio", f"{df['Índice Simetría (%)'].mean():.1f}%")
    k4.metric("🏅 Score Bio Promedio", f"{df['Score Biomecánico'].mean():.1f}")
    k5.metric("🗓️ Razas", df["Raza"].nunique())

    st.markdown("---")
    col_a, col_b = st.columns([3, 2])

    with col_a:
        # Score por raza — boxplot
        fig_box = px.box(
            df, x="Raza", y="Score Biomecánico", color="Raza",
            points="all",
        )
        apply_theme(fig_box, "Score Biomecánico por Raza")
        fig_box.update_layout(xaxis_tickangle=-35, showlegend=False, height=400)
        st.plotly_chart(fig_box, use_container_width=True)

    with col_b:
        # Distribución de razas — donut
        cnt = df["Raza"].value_counts().reset_index()
        cnt.columns = ["Raza", "Count"]
        fig_pie = px.pie(cnt, names="Raza", values="Count", hole=0.55)
        apply_theme(fig_pie, "Distribución de Razas")
        fig_pie.update_traces(textposition="inside", textinfo="percent+label",
                               textfont_size=10)
        fig_pie.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        fig_sc = px.scatter(
            df, x="Vel. Máx (km/h)", y="Zancada (m)",
            color="Raza", size="Peso (kg)", size_max=18,
            hover_data=["Nombre", "Edad (años)", "Score Biomecánico"],
        )
        apply_theme(fig_sc, "Velocidad Máx. vs Longitud de Zancada")
        fig_sc.update_layout(height=380)
        st.plotly_chart(fig_sc, use_container_width=True)

    with col_d:
        fig_histo = px.histogram(
            df, x="Score Biomecánico", nbins=25,
            color="Raza", barmode="overlay", opacity=0.75,
        )
        apply_theme(fig_histo, "Distribución de Score Biomecánico")
        fig_histo.update_layout(height=380)
        st.plotly_chart(fig_histo, use_container_width=True)

    # Heatmap correlación
    st.markdown("#### 🔗 Mapa de Correlaciones")
    cols_num = ["Vel. Máx (km/h)", "Zancada (m)", "Cadencia (p/min)",
                "Áng. Hombro (°)", "Áng. Cadera (°)", "Índice Simetría (%)",
                "Peso (kg)", "Score Biomecánico", "Desp. Total (km)"]
    corr = df[cols_num].corr()
    fig_heat = px.imshow(
        corr, text_auto=".2f", aspect="auto",
        color_continuous_scale=["#f43f5e","#111418","#c9a84c"],
        zmin=-1, zmax=1,
    )
    apply_theme(fig_heat)
    fig_heat.update_layout(height=420)
    st.plotly_chart(fig_heat, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 2 — PERFIL INDIVIDUAL
# ══════════════════════════════════════════════

with tabs[1]:
    st.markdown("### 🐴 Análisis Individual")
    nombres_disp = df["Nombre"].unique().tolist()
    caballo_nombre = st.selectbox("Seleccionar caballo", nombres_disp)
    row = df[df["Nombre"] == caballo_nombre].iloc[0]

    col_info, col_radar = st.columns([2, 3])

    with col_info:
        st.markdown(f"""
        <div style='background:var(--bg-panel);border:1px solid var(--border);border-radius:14px;padding:24px;'>
            <div style='font-family:Playfair Display,serif;font-size:1.6rem;color:var(--gold);margin-bottom:4px;'>{caballo_nombre}</div>
            <div style='color:var(--text-muted);font-size:0.78rem;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:18px;'>{row['Raza']}</div>
            <table style='width:100%;font-size:0.85rem;color:var(--text-primary);'>
                <tr><td style='color:var(--text-muted);padding:4px 0;'>Edad</td><td style='text-align:right;color:var(--gold-light);'>{row['Edad (años)']} años</td></tr>
                <tr><td style='color:var(--text-muted);padding:4px 0;'>Sexo</td><td style='text-align:right;'>{row['Sexo']}</td></tr>
                <tr><td style='color:var(--text-muted);padding:4px 0;'>Color</td><td style='text-align:right;'>{row['Color']}</td></tr>
                <tr><td style='color:var(--text-muted);padding:4px 0;'>Peso</td><td style='text-align:right;'>{row['Peso (kg)']} kg</td></tr>
                <tr><td style='color:var(--text-muted);padding:4px 0;'>Propietario</td><td style='text-align:right;font-size:0.78rem;'>{row['Propietario']}</td></tr>
                <tr><td colspan=2><hr style='border-color:var(--border);margin:10px 0;'></td></tr>
                <tr><td style='color:var(--text-muted);'>Vel. Máx</td><td style='text-align:right;color:var(--teal);font-weight:600;'>{row['Vel. Máx (km/h)']} km/h</td></tr>
                <tr><td style='color:var(--text-muted);'>Zancada</td><td style='text-align:right;color:var(--teal);'>{row['Zancada (m)']} m</td></tr>
                <tr><td style='color:var(--text-muted);'>Simetría</td><td style='text-align:right;color:var(--teal);'>{row['Índice Simetría (%)']:.1f}%</td></tr>
                <tr><td style='color:var(--text-muted);'>Score Bio</td><td style='text-align:right;color:var(--gold);font-family:Space Mono,monospace;font-size:1rem;'>{row['Score Biomecánico']:.1f}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        score = row["Score Biomecánico"]
        if score >= 75:
            estado = "<span class='status-ok'>✅ Excelente condición</span>"
        elif score >= 55:
            estado = "<span class='status-warn'>⚠️ Condición aceptable</span>"
        else:
            estado = "<span class='status-bad'>❌ Requiere atención</span>"
        st.markdown(f"<div style='margin-top:12px;text-align:center;'>{estado}</div>", unsafe_allow_html=True)

    with col_radar:
        cats = ["Velocidad", "Zancada", "Cadencia", "Simetría", "Ángulo Hip.", "Score Bio"]
        vals = [
            row["Vel. Máx (km/h)"] / 90 * 100,
            row["Zancada (m)"] / 4.5 * 100,
            row["Cadencia (p/min)"] / 220 * 100,
            row["Índice Simetría (%)"],
            row["Áng. Cadera (°)"] / 75 * 100,
            row["Score Biomecánico"],
        ]
        raza_media = df_full[df_full["Raza"] == row["Raza"]]
        media_vals = [
            raza_media["Vel. Máx (km/h)"].mean() / 90 * 100,
            raza_media["Zancada (m)"].mean() / 4.5 * 100,
            raza_media["Cadencia (p/min)"].mean() / 220 * 100,
            raza_media["Índice Simetría (%)"].mean(),
            raza_media["Áng. Cadera (°)"].mean() / 75 * 100,
            raza_media["Score Biomecánico"].mean(),
        ]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=cats + [cats[0]],
            fill="toself", name=caballo_nombre,
            line_color="#c9a84c", fillcolor="rgba(201,168,76,0.2)",
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=media_vals + [media_vals[0]], theta=cats + [cats[0]],
            fill="toself", name=f"Media {row['Raza']}",
            line_color="#2dd4bf", fillcolor="rgba(45,212,191,0.1)",
            line_dash="dash",
        ))
        apply_theme(fig_radar, f"Perfil Biomecánico — {caballo_nombre}")
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0,100], gridcolor="rgba(201,168,76,0.1)", tickfont_color="#7a6230"),
                angularaxis=dict(gridcolor="rgba(201,168,76,0.15)"),
                bgcolor="rgba(17,20,24,0.4)",
            ),
            height=420,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Serie temporal del caballo
    st.markdown("#### 📈 Evolución Temporal (últimos 90 días)")
    serie = generar_serie_tiempo(caballo_nombre, seed=abs(hash(caballo_nombre)) % 999)

    fig_line = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.6, 0.4],
                              vertical_spacing=0.06)
    fig_line.add_trace(go.Scatter(x=serie["Fecha"], y=serie["Velocidad (km/h)"],
                                   name="Velocidad (km/h)", line_color="#c9a84c", line_width=2), row=1, col=1)
    fig_line.add_trace(go.Scatter(x=serie["Fecha"], y=serie["Score Biomecánico"],
                                   name="Score Bio", line_color="#2dd4bf", line_width=2,
                                   line_dash="dot"), row=1, col=1)
    fig_line.add_trace(go.Bar(x=serie["Fecha"], y=serie["Comp. Anterior (%)"],
                               name="Comp. Ant (%)", marker_color="#c9a84c", opacity=0.7), row=2, col=1)
    fig_line.add_trace(go.Bar(x=serie["Fecha"], y=serie["Comp. Posterior (%)"],
                               name="Comp. Post (%)", marker_color="#f43f5e", opacity=0.7), row=2, col=1)
    apply_theme(fig_line, f"Evolución — {caballo_nombre}")
    fig_line.update_layout(height=450, barmode="overlay")
    st.plotly_chart(fig_line, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 3 — BIOMECÁNICA & ÁNGULOS
# ══════════════════════════════════════════════

with tabs[2]:
    st.markdown("### 📐 Análisis Biomecánico y Ángulos Articulares")

    col_ang1, col_ang2 = st.columns(2)

    with col_ang1:
        ang_cols = ["Áng. Hombro (°)", "Áng. Cadera (°)", "Áng. Rod. Ant (°)",
                    "Áng. Rod. Post (°)", "Áng. Menudillo (°)", "Áng. Casco (°)"]
        df_melt = df[["Raza"] + ang_cols].melt(id_vars="Raza", var_name="Articulación", value_name="Ángulo (°)")
        fig_viol = px.violin(df_melt, x="Articulación", y="Ángulo (°)", color="Raza",
                              box=True, points=False, violinmode="overlay")
        apply_theme(fig_viol, "Distribución de Ángulos Articulares por Raza")
        fig_viol.update_layout(height=420, xaxis_tickangle=-25)
        st.plotly_chart(fig_viol, use_container_width=True)

    with col_ang2:
        media_ang = df.groupby("Raza")[ang_cols].mean().reset_index()
        fig_bar_ang = px.bar(
            media_ang.melt(id_vars="Raza", var_name="Articulación", value_name="Ángulo (°)"),
            x="Articulación", y="Ángulo (°)", color="Raza", barmode="group",
        )
        apply_theme(fig_bar_ang, "Ángulos Promedio por Raza")
        fig_bar_ang.update_layout(height=420, xaxis_tickangle=-25)
        st.plotly_chart(fig_bar_ang, use_container_width=True)

    # Scatter 3D velocidad-zancada-ángulo
    st.markdown("#### 🌐 Visualización 3D — Velocidad · Zancada · Ángulo Cadera")
    fig_3d = px.scatter_3d(
        df, x="Vel. Máx (km/h)", y="Zancada (m)", z="Áng. Cadera (°)",
        color="Score Biomecánico", symbol="Raza",
        size="Peso (kg)", size_max=10,
        color_continuous_scale=["#f43f5e","#c9a84c","#2dd4bf"],
        hover_data=["Nombre","Raza","Edad (años)"],
    )
    apply_theme(fig_3d)
    fig_3d.update_layout(height=520, scene=dict(
        paper_bgcolor="rgba(0,0,0,0)",
        bgcolor="rgba(17,20,24,0.8)",
        xaxis=dict(backgroundcolor="rgba(22,27,34,0.6)", gridcolor="rgba(201,168,76,0.1)"),
        yaxis=dict(backgroundcolor="rgba(22,27,34,0.6)", gridcolor="rgba(201,168,76,0.1)"),
        zaxis=dict(backgroundcolor="rgba(22,27,34,0.6)", gridcolor="rgba(201,168,76,0.1)"),
    ))
    st.plotly_chart(fig_3d, use_container_width=True)

    # Cadencia vs Velocidad
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        fig_cad = px.scatter(df, x="Cadencia (p/min)", y="Vel. Máx (km/h)",
                              color="Raza", trendline="ols", trendline_scope="overall",
                              hover_data=["Nombre"])
        apply_theme(fig_cad, "Cadencia vs Velocidad Máxima")
        fig_cad.update_layout(height=360)
        st.plotly_chart(fig_cad, use_container_width=True)

    with col_c2:
        fig_zan = px.scatter(df, x="Zancada (m)", y="Vel. Máx (km/h)",
                              color="Raza", trendline="ols", trendline_scope="overall",
                              hover_data=["Nombre", "Cadencia (p/min)"])
        apply_theme(fig_zan, "Zancada vs Velocidad Máxima")
        fig_zan.update_layout(height=360)
        st.plotly_chart(fig_zan, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 4 — COMPENSACIÓN
# ══════════════════════════════════════════════

with tabs[3]:
    st.markdown("### ⚖️ Análisis de Compensación entre Extremidades")

    info_html = """
    <div class='info-box'>
    <strong>¿Qué es la compensación equina?</strong> Cuando un caballo experimenta dolor, debilidad o restricción en un miembro,
    redistribuye la carga hacia otras extremidades generando patrones de compensación que, si no se tratan, 
    pueden derivar en lesiones secundarias. BuHo cuantifica este fenómeno en tiempo real.
    </div>
    """
    st.markdown(info_html, unsafe_allow_html=True)

    comp_cols = ["Comp. Anterior (%)", "Comp. Posterior (%)", "Comp. Lateral (%)"]

    col_comp1, col_comp2 = st.columns(2)

    with col_comp1:
        # Bubble chart compensación
        fig_bub = px.scatter(
            df,
            x="Comp. Anterior (%)", y="Comp. Posterior (%)",
            size=np.abs(df["Comp. Lateral (%)"]) + 1,
            color="Índice Simetría (%)",
            color_continuous_scale=["#f43f5e","#f59e0b","#22c55e"],
            hover_data=["Nombre","Raza","Score Biomecánico"],
            size_max=22,
        )
        apply_theme(fig_bub, "Mapa de Compensación Anterior vs Posterior")
        fig_bub.add_hline(y=0, line_dash="dot", line_color="rgba(201,168,76,0.4)")
        fig_bub.add_vline(x=0, line_dash="dot", line_color="rgba(201,168,76,0.4)")
        fig_bub.update_layout(height=400)
        st.plotly_chart(fig_bub, use_container_width=True)

    with col_comp2:
        # Fuerza por extremidad — grouped bar
        fuerzas_med = df.groupby("Raza")[["Fuerza IE Ant (N)","Fuerza DE Ant (N)",
                                          "Fuerza IE Post (N)","Fuerza DE Post (N)"]].mean().reset_index()
        f_melt = fuerzas_med.melt(id_vars="Raza", var_name="Extremidad", value_name="Fuerza (N)")
        fig_fuerza = px.bar(f_melt, x="Raza", y="Fuerza (N)", color="Extremidad", barmode="group")
        apply_theme(fig_fuerza, "Fuerza Promedio por Extremidad y Raza")
        fig_fuerza.update_layout(xaxis_tickangle=-30, height=400)
        st.plotly_chart(fig_fuerza, use_container_width=True)

    # Índice de simetría por raza
    st.markdown("#### 📊 Índice de Simetría por Raza")
    sim_raza = df.groupby("Raza")["Índice Simetría (%)"].agg(["mean","std"]).reset_index()
    sim_raza.columns = ["Raza","Media","Std"]
    fig_sym = go.Figure()
    fig_sym.add_trace(go.Bar(
        x=sim_raza["Raza"], y=sim_raza["Media"],
        error_y=dict(type="data", array=sim_raza["Std"], visible=True, color="#c9a84c"),
        marker_color=["#c9a84c" if r == "Criollo Colombiano" else "#2dd4bf" for r in sim_raza["Raza"]],
        name="Índice Simetría",
    ))
    apply_theme(fig_sym, "Índice de Simetría Promedio (±SD) por Raza")
    fig_sym.add_hline(y=95, line_dash="dash", line_color="#22c55e",
                       annotation_text="Umbral óptimo", annotation_position="top right")
    fig_sym.update_layout(xaxis_tickangle=-30, height=380, yaxis_range=[80,102])
    st.plotly_chart(fig_sym, use_container_width=True)

    # Tabla de caballos con mayor compensación
    st.markdown("#### 🚨 Caballos con Mayor Asimetría (Top 10)")
    df_asim = df[["Nombre","Raza","Comp. Anterior (%)","Comp. Posterior (%)","Comp. Lateral (%)","Índice Simetría (%)","Score Biomecánico"]].copy()
    df_asim["Asimetría Total"] = (df_asim["Comp. Anterior (%)"].abs() +
                                   df_asim["Comp. Posterior (%)"].abs() +
                                   df_asim["Comp. Lateral (%)"].abs())
    top10 = df_asim.nlargest(10, "Asimetría Total").reset_index(drop=True)
    st.dataframe(
        top10.style
            .background_gradient(subset=["Asimetría Total"], cmap="Reds")
            .background_gradient(subset=["Score Biomecánico"], cmap="RdYlGn")
            .format({c: "{:.2f}" for c in top10.select_dtypes("float").columns}),
        use_container_width=True, height=350,
    )


# ══════════════════════════════════════════════
#  TAB 5 — YOLO TRACKER
# ══════════════════════════════════════════════

with tabs[4]:
    st.markdown("### 🎯 YOLO Motion Tracker — Análisis Cinemático por Video")

    st.markdown("""
    <div class='info-box'>
    <strong>YOLO Equine Tracker:</strong> Simulación de datos de seguimiento de poses obtenidos 
    mediante modelos YOLOv8-Pose entrenados con datos equinos. Cada punto representa una articulación 
    clave del caballo rastreada frame a frame. En producción, este módulo se conecta directamente 
    al pipeline de inferencia en video (MP4, RTSP, etc.).
    </div>
    """, unsafe_allow_html=True)

    col_yolo_ctrl, col_yolo_main = st.columns([1, 3])

    with col_yolo_ctrl:
        st.markdown("**⚙️ Parámetros YOLO**")
        n_frames_yolo = st.slider("Frames a analizar", 50, 500, 300, 50)
        partes_sel    = st.multiselect(
            "Articulaciones visibles",
            ["Cabeza","Cuello","Hombro_I","Hombro_D","Codo_I","Codo_D",
             "Rodilla_I","Rodilla_D","Casco_I","Casco_D","Cadera","Cola"],
            default=["Hombro_I","Hombro_D","Rodilla_I","Rodilla_D","Casco_I","Casco_D"],
        )
        confianza_min = st.slider("Confianza mínima YOLO", 0.5, 1.0, 0.72, 0.01)
        animar_btn    = st.button("▶ Generar Análisis")

        st.markdown("---")
        st.markdown("**📤 Cargar video / CSV**")
        uploaded = st.file_uploader("Subir CSV de keypoints YOLO", type=["csv","txt"])

    with col_yolo_main:
        df_yolo, all_parts = simular_tracker_yolo(n_frames_yolo, seed=17)
        df_yolo = df_yolo[df_yolo["Confianza_YOLO"] >= confianza_min]

        if uploaded is not None:
            st.success(f"✅ Archivo cargado: `{uploaded.name}` — {len(df_yolo)} frames válidos")

        # Trayectorias
        fig_traj = go.Figure()
        palette = ["#c9a84c","#2dd4bf","#f43f5e","#818cf8","#fb923c","#34d399","#67e8f9","#e879f9","#fbbf24","#a3e635","#60a5fa","#f9a8d4"]
        for i, parte in enumerate(partes_sel or all_parts[:4]):
            if f"{parte}_x" in df_yolo.columns:
                fig_traj.add_trace(go.Scatter(
                    x=df_yolo["Frame"], y=df_yolo[f"{parte}_y"],
                    mode="lines", name=parte,
                    line=dict(color=palette[i % len(palette)], width=1.5),
                    opacity=0.85,
                ))
        apply_theme(fig_traj, "Trayectorias de Articulaciones (eje Y en píxeles)")
        fig_traj.update_layout(height=300, yaxis_title="Posición Y (px)", xaxis_title="Frame")
        st.plotly_chart(fig_traj, use_container_width=True)

        # Snapshot scatter — posición 2D
        frame_snap = st.slider("📍 Frame Snapshot", int(df_yolo["Frame"].min()),
                                int(df_yolo["Frame"].max()), int(df_yolo["Frame"].median()))
        snap_row = df_yolo[df_yolo["Frame"] == frame_snap]
        if snap_row.empty:
            snap_row = df_yolo.iloc[[len(df_yolo)//2]]

        fig_snap = go.Figure()
        xs, ys, labels = [], [], []
        for parte in (partes_sel or all_parts):
            if f"{parte}_x" in snap_row.columns:
                xs.append(float(snap_row[f"{parte}_x"].values[0]))
                ys.append(float(snap_row[f"{parte}_y"].values[0]))
                labels.append(parte)

        fig_snap.add_trace(go.Scatter(
            x=xs, y=ys, mode="markers+text", text=labels,
            textposition="top center", textfont=dict(size=10, color="#c9a84c"),
            marker=dict(size=14, color="#c9a84c", opacity=0.9,
                        line=dict(width=2, color="#e8c97a")),
            name="Keypoints",
        ))
        # Esqueleto básico conectando puntos
        conexiones = [("Cabeza","Cuello"),("Cuello","Hombro_I"),("Cuello","Hombro_D"),
                      ("Hombro_I","Codo_I"),("Codo_I","Rodilla_I"),("Rodilla_I","Casco_I"),
                      ("Hombro_D","Codo_D"),("Codo_D","Rodilla_D"),("Rodilla_D","Casco_D"),
                      ("Cadera","Hombro_I"),("Cadera","Hombro_D"),("Cadera","Cola")]
        idx = {l: i for i, l in enumerate(labels)}
        for a, b in conexiones:
            if a in idx and b in idx:
                fig_snap.add_trace(go.Scatter(
                    x=[xs[idx[a]], xs[idx[b]]], y=[ys[idx[a]], ys[idx[b]]],
                    mode="lines", line=dict(color="rgba(201,168,76,0.35)", width=2),
                    showlegend=False,
                ))
        apply_theme(fig_snap, f"Esqueleto 2D — Frame {frame_snap}")
        fig_snap.update_layout(height=320, xaxis_title="X (px)", yaxis_title="Y (px)",
                                yaxis_autorange="reversed")
        st.plotly_chart(fig_snap, use_container_width=True)

        # Confianza YOLO a lo largo del tiempo
        fig_conf = px.area(df_yolo, x="Frame", y="Confianza_YOLO",
                            color_discrete_sequence=["#2dd4bf"])
        apply_theme(fig_conf, "Confianza YOLO por Frame")
        fig_conf.update_layout(height=220)
        fig_conf.add_hline(y=confianza_min, line_dash="dash", line_color="#f43f5e",
                            annotation_text="Umbral mínimo")
        st.plotly_chart(fig_conf, use_container_width=True)


# ══════════════════════════════════════════════
#  TAB 6 — DATOS & CARGA
# ══════════════════════════════════════════════

with tabs[5]:
    st.markdown("### 📁 Gestión de Datos")

    sub1, sub2 = st.tabs(["📊 Datos sintéticos", "📤 Cargar datos"])

    with sub1:
        st.markdown(f"**Registros activos: `{len(df)}`** — Usa los filtros del panel lateral para modificar la vista.")
        col_ord, col_dir = st.columns([3, 1])
        sort_col = col_ord.selectbox("Ordenar por", df.select_dtypes("number").columns.tolist(), index=df.columns.get_loc("Score Biomecánico")-1)
        ascending = col_dir.selectbox("Dirección", ["Descendente","Ascendente"]) == "Ascendente"
        df_show = df.sort_values(sort_col, ascending=ascending).reset_index(drop=True)
        st.dataframe(df_show, use_container_width=True, height=450)

        col_dl1, col_dl2 = st.columns(2)
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        col_dl1.download_button("⬇ Descargar CSV", csv_bytes, "buho_datos.csv", "text/csv")
        excel_buf = io.BytesIO()
        df.to_excel(excel_buf, index=False, engine="openpyxl")
        col_dl2.download_button("⬇ Descargar Excel", excel_buf.getvalue(), "buho_datos.xlsx",
                                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with sub2:
        st.markdown("""
        <div class='info-box'>
        BuHo acepta múltiples fuentes de datos: <strong>CSV, Excel, texto libre, 
        descripciones clínicas y datos de tracker YOLO</strong>. 
        Los datos cargados se integran automáticamente con el motor de análisis.
        </div>
        """, unsafe_allow_html=True)

        up_file = st.file_uploader("Cargar archivo de datos equinos", type=["csv","xlsx","txt"])
        if up_file:
            try:
                if up_file.name.endswith(".csv"):
                    df_user = pd.read_csv(up_file)
                elif up_file.name.endswith(".xlsx"):
                    df_user = pd.read_excel(up_file)
                else:
                    content = up_file.read().decode("utf-8")
                    st.text_area("Contenido del archivo", content, height=200)
                    df_user = None
                if df_user is not None:
                    st.success(f"✅ Archivo cargado: {len(df_user)} filas, {len(df_user.columns)} columnas")
                    st.dataframe(df_user, use_container_width=True)
            except Exception as e:
                st.error(f"Error al procesar el archivo: {e}")

        st.markdown("---")
        st.markdown("#### 📝 Ingreso de texto / descripción clínica")
        texto_desc = st.text_area(
            "Descripción clínica o notas de campo",
            placeholder="Ej: Caballo macho, Criollo Colombiano, 8 años. Presenta leve cojera en extremidad anterior derecha. Velocidad reducida al trote (15 km/h). Ángulo de casco 48°. Compensación lateral estimada en +4.2%...",
            height=140,
        )
        if st.button("🔍 Analizar descripción"):
            if texto_desc.strip():
                st.markdown("""
                <div style='background:var(--bg-panel);border:1px solid var(--border);border-radius:10px;padding:16px;margin-top:8px;'>
                <span style='color:var(--gold);font-family:Playfair Display,serif;font-size:1rem;'>Análisis preliminar (simulado):</span><br><br>
                <span style='color:var(--text-primary);font-size:0.88rem;'>
                ⚠️ <strong>Hallazgo principal:</strong> Posible claudicación anterior derecha (grado 1–2 / 5).<br>
                📐 <strong>Ángulos:</strong> Ángulo de casco en rango normal-bajo (48°). Monitorear progresión.<br>
                ⚖️ <strong>Compensación:</strong> Asimetría lateral +4.2% → umbral de atención clínica superado.<br>
                🏃 <strong>Rendimiento:</strong> Velocidad de trote reducida en ~17% respecto a la media de la raza.<br>
                💡 <strong>Recomendación:</strong> Evaluación veterinaria especializada en locomoción. 
                Considerar terapia de compensación y ajuste de herraje.
                </span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Por favor ingresa una descripción.")


# ══════════════════════════════════════════════
#  TAB 7 — REPORTE IA
# ══════════════════════════════════════════════

with tabs[6]:
    st.markdown("### 📋 Reporte de Análisis — BuHo Intelligence")

    col_rep1, col_rep2 = st.columns([2, 1])

    with col_rep1:
        st.markdown("#### Seleccionar caballo para reporte completo")
        cab_rep = st.selectbox("Caballo", df["Nombre"].unique().tolist(), key="rep_cab")
        row_rep = df[df["Nombre"] == cab_rep].iloc[0]

        if st.button("📄 Generar Reporte"):
            score = row_rep["Score Biomecánico"]
            sim   = row_rep["Índice Simetría (%)"]
            comp_a = row_rep["Comp. Anterior (%)"]
            comp_p = row_rep["Comp. Posterior (%)"]

            if score >= 75:
                diagnostico = "✅ **Condición biomecánica óptima.** El animal presenta parámetros dentro de rangos deseables."
                color_diag = "#22c55e"
            elif score >= 55:
                diagnostico = "⚠️ **Condición biomecánica aceptable con áreas de mejora.** Se recomienda seguimiento periódico."
                color_diag = "#f59e0b"
            else:
                diagnostico = "❌ **Condición biomecánica deficiente.** Se requiere evaluación veterinaria urgente."
                color_diag = "#f43f5e"

            st.markdown(f"""
<div style='background:var(--bg-panel);border:1px solid var(--border);border-radius:14px;padding:28px;'>
<div style='font-family:Playfair Display,serif;font-size:1.5rem;color:var(--gold);margin-bottom:4px;'>
🦉 BuHo — Reporte Biomecánico</div>
<div style='color:var(--text-muted);font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:20px;'>
ORCAS Analítica de Datos · Jorge Iván Padilla Buritica · {datetime.now().strftime("%d/%m/%Y %H:%M")}</div>
<hr style='border-color:var(--border);'>

<table style='width:100%;font-size:0.88rem;margin:16px 0;'>
<tr><td style='color:var(--text-muted);width:40%;'>Nombre</td><td style='color:var(--gold-light);font-weight:600;'>{cab_rep}</td></tr>
<tr><td style='color:var(--text-muted);'>Raza</td><td>{row_rep['Raza']}</td></tr>
<tr><td style='color:var(--text-muted);'>Edad / Sexo / Color</td><td>{row_rep['Edad (años)']} años · {row_rep['Sexo']} · {row_rep['Color']}</td></tr>
<tr><td style='color:var(--text-muted);'>Propietario</td><td>{row_rep['Propietario']}</td></tr>
<tr><td style='color:var(--text-muted);'>Peso</td><td>{row_rep['Peso (kg)']} kg</td></tr>
</table>

<hr style='border-color:var(--border);'>
<div style='font-family:Playfair Display,serif;font-size:1rem;color:var(--gold);margin:14px 0 10px;'>📊 Parámetros Biomecánicos</div>

<table style='width:100%;font-size:0.85rem;'>
<tr><td style='color:var(--text-muted);'>Velocidad máxima</td><td style='text-align:right;color:var(--teal);'>{row_rep['Vel. Máx (km/h)']} km/h</td></tr>
<tr><td style='color:var(--text-muted);'>Longitud de zancada</td><td style='text-align:right;color:var(--teal);'>{row_rep['Zancada (m)']} m</td></tr>
<tr><td style='color:var(--text-muted);'>Cadencia</td><td style='text-align:right;'>{row_rep['Cadencia (p/min)']} p/min</td></tr>
<tr><td style='color:var(--text-muted);'>Desplazamiento total</td><td style='text-align:right;'>{row_rep['Desp. Total (km)']} km</td></tr>
<tr><td style='color:var(--text-muted);'>Ángulo hombro</td><td style='text-align:right;'>{row_rep['Áng. Hombro (°)']}°</td></tr>
<tr><td style='color:var(--text-muted);'>Ángulo cadera</td><td style='text-align:right;'>{row_rep['Áng. Cadera (°)']}°</td></tr>
<tr><td style='color:var(--text-muted);'>Ángulo casco</td><td style='text-align:right;'>{row_rep['Áng. Casco (°)']}°</td></tr>
</table>

<hr style='border-color:var(--border);'>
<div style='font-family:Playfair Display,serif;font-size:1rem;color:var(--gold);margin:14px 0 10px;'>⚖️ Compensación</div>

<table style='width:100%;font-size:0.85rem;'>
<tr><td style='color:var(--text-muted);'>Comp. Anterior</td><td style='text-align:right;color:{"#f43f5e" if abs(comp_a)>5 else "#22c55e"};'>{comp_a:+.2f}%</td></tr>
<tr><td style='color:var(--text-muted);'>Comp. Posterior</td><td style='text-align:right;color:{"#f43f5e" if abs(comp_p)>5 else "#22c55e"};'>{comp_p:+.2f}%</td></tr>
<tr><td style='color:var(--text-muted);'>Comp. Lateral</td><td style='text-align:right;'>{row_rep['Comp. Lateral (%)']:+.2f}%</td></tr>
<tr><td style='color:var(--text-muted);'>Índice de Simetría</td><td style='text-align:right;color:{"#22c55e" if sim>=95 else "#f59e0b"};'><strong>{sim:.1f}%</strong></td></tr>
</table>

<hr style='border-color:var(--border);'>
<div style='margin:16px 0;padding:14px;background:rgba(17,20,24,0.8);border-left:3px solid {color_diag};border-radius:0 8px 8px 0;'>
<div style='font-size:0.78rem;color:var(--text-muted);margin-bottom:4px;'>DIAGNÓSTICO BIOMECÁNICO</div>
<div style='font-size:0.9rem;color:var(--text-primary);'>{diagnostico}</div>
<div style='margin-top:10px;font-size:0.88rem;'>
<strong style='color:var(--gold);'>Score Biomecánico Global:</strong>
<span style='font-family:Space Mono,monospace;font-size:1.2rem;color:{color_diag};'> {score:.1f} / 100</span>
</div>
</div>

<div style='font-size:0.68rem;color:var(--text-muted);margin-top:16px;text-align:center;'>
Reporte generado automáticamente por BuHo v1.0 · ORCAS Analítica de Datos<br>
Este reporte es de carácter informativo. Consulte siempre con un veterinario especialista.
</div>
</div>
""", unsafe_allow_html=True)

    with col_rep2:
        st.markdown("#### 📈 Ranking General")
        top_rank = df[["Nombre","Raza","Score Biomecánico","Índice Simetría (%)"]]\
                     .sort_values("Score Biomecánico", ascending=False)\
                     .head(15).reset_index(drop=True)
        top_rank.index += 1
        fig_rank = px.bar(
            top_rank, x="Score Biomecánico", y="Nombre",
            orientation="h", color="Score Biomecánico",
            color_continuous_scale=["#f43f5e","#f59e0b","#22c55e"],
            hover_data=["Raza","Índice Simetría (%)"],
        )
        apply_theme(fig_rank, "Top 15 Caballos")
        fig_rank.update_layout(height=480, showlegend=False, yaxis_title="", coloraxis_showscale=False)
        st.plotly_chart(fig_rank, use_container_width=True)

        st.markdown("#### 🐎 Criollo Colombiano")
        df_cc = df[df["Raza"] == "Criollo Colombiano"]
        if len(df_cc):
            st.metric("Caballos evaluados", len(df_cc))
            st.metric("Score promedio", f"{df_cc['Score Biomecánico'].mean():.1f}")
            st.metric("Vel. máx promedio", f"{df_cc['Vel. Máx (km/h)'].mean():.1f} km/h")
            st.metric("Simetría promedio", f"{df_cc['Índice Simetría (%)'].mean():.1f}%")
        else:
            st.info("Sin datos de Criollo Colombiano en filtro actual.")


# ── Footer ──────────────────────────────────────────────────────
st.markdown("""
<hr style='border-color:rgba(201,168,76,0.15);margin-top:40px;'>
<div style='text-align:center;padding:16px 0 8px;'>
    <span style='font-family:Playfair Display,serif;font-size:1.2rem;color:#c9a84c;'>🦉 BuHo</span>
    <span style='color:#5a5550;font-size:0.75rem;margin:0 12px;'>·</span>
    <span style='color:#5a5550;font-size:0.75rem;'>Business with Horses</span>
    <span style='color:#5a5550;font-size:0.75rem;margin:0 12px;'>·</span>
    <span style='color:#5a5550;font-size:0.75rem;'>Jorge Iván Padilla Buritica</span>
    <span style='color:#5a5550;font-size:0.75rem;margin:0 12px;'>·</span>
    <span style='color:#7a6230;font-size:0.75rem;'>ORCAS Analítica de Datos</span>
    <span style='color:#5a5550;font-size:0.75rem;margin:0 12px;'>·</span>
    <span style='color:#5a5550;font-size:0.75rem;'>v1.0 · 2024</span>
</div>
""", unsafe_allow_html=True)
