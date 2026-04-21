import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import joblib
import time

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Diabetes Risk Analyzer | AI Clinical Lab",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# LOAD MODEL
# ===============================
@st.cache_resource
def load_model():
    return joblib.load("model_ab.pkl")

model = load_model()

# ===============================
# CUSTOM CSS — CLINICAL FUTURISTIC THEME
# ===============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─── GLOBAL ─── */
.stApp {
    background: #080A12;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
#MainMenu, footer, header, .stDeployButton { visibility: hidden; }
.block-container { padding-top: 1rem; max-width: 1100px; }

/* ─── ANIMATED BG ─── */
.stApp > div:first-child::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse 70% 50% at 15% 15%, rgba(56, 189, 248, 0.05) 0%, transparent 60%),
        radial-gradient(ellipse 50% 70% at 85% 85%, rgba(168, 85, 247, 0.04) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 50% 50%, rgba(251, 113, 133, 0.03) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
    animation: bgBreath 15s ease-in-out infinite alternate;
}
@keyframes bgBreath {
    0% { opacity: 0.5; }
    100% { opacity: 1; }
}

/* ─── NOISE ─── */
.stApp > div:first-child::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    opacity: 0.02;
    pointer-events: none;
    z-index: 1;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}

/* ─── TYPOGRAPHY ─── */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #E2E8F0 !important;
}
p, span, li, .stMarkdown p, label {
    color: #94A3B8 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ─── HERO ─── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
    z-index: 2;
    animation: heroSlide 0.9s ease-out;
}
@keyframes heroSlide {
    from { opacity: 0; transform: translateY(35px); }
    to { opacity: 1; transform: translateY(0); }
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #38BDF8;
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 100px;
    padding: 6px 18px;
    background: rgba(56, 189, 248, 0.06);
    margin-bottom: 1.25rem;
    font-family: 'JetBrains Mono', monospace;
}
.hero-badge .dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #38BDF8;
    animation: dotBlink 2s infinite;
}
@keyframes dotBlink {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(56,189,248,0.4); }
    50% { opacity: 0.5; box-shadow: 0 0 0 7px rgba(56,189,248,0); }
}
.hero-title {
    font-size: clamp(2.2rem, 5vw, 3.2rem);
    font-weight: 800;
    letter-spacing: -0.035em;
    line-height: 1.08;
    margin-bottom: 0.85rem;
    background: linear-gradient(135deg, #E2E8F0 0%, #38BDF8 45%, #A78BFA 75%, #FB7185 100%);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradShift 6s ease-in-out infinite;
}
@keyframes gradShift {
    0%, 100% { background-position: 0% center; }
    50% { background-position: 300% center; }
}
.hero-sub {
    font-size: 0.95rem;
    color: #64748B !important;
    font-weight: 300;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.75;
}
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 3rem;
    margin-top: 1.75rem;
    padding-top: 1.25rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    flex-wrap: wrap;
}
.hs-item { text-align: center; }
.hs-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.2rem;
    font-weight: 600;
    color: #E2E8F0 !important;
}
.hs-lbl {
    font-size: 0.65rem;
    color: #475569 !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 3px;
}
.divider {
    width: 50px; height: 2px;
    background: linear-gradient(90deg, transparent, #38BDF8, transparent);
    margin: 1.5rem auto;
}

/* ─── FORM SECTIONS ─── */
.form-section {
    background: rgba(15, 17, 28, 0.75);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.25rem;
    position: relative;
    z-index: 2;
    animation: sectionIn 0.7s ease-out both;
}
.form-section:nth-child(1) { animation-delay: 0.1s; }
.form-section:nth-child(2) { animation-delay: 0.2s; }
.form-section:nth-child(3) { animation-delay: 0.3s; }
.form-section:nth-child(4) { animation-delay: 0.4s; }
@keyframes sectionIn {
    from { opacity: 0; transform: translateY(25px); }
    to { opacity: 1; transform: translateY(0); }
}
.form-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.15), transparent);
    border-radius: 18px 18px 0 0;
}
.form-section-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
    padding-bottom: 0.85rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.fs-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.fs-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #E2E8F0 !important;
    letter-spacing: 0.01em;
}
.fs-sub {
    font-size: 0.7rem;
    color: #475569 !important;
    margin-top: 1px;
}

/* ─── STREAMLIT WIDGET OVERRIDES ─── */
/* Slider */
[data-testid="stSlider"] label {
    color: #94A3B8 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 400 !important;
}
[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #38BDF8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 500 !important;
}

/* Radio */
[data-testid="stRadio"] label {
    color: #94A3B8 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 14px !important;
}
[data-testid="stRadio"] div[role="radiogroup"] label {
    color: #CBD5E1 !important;
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    padding: 0.4rem 1rem !important;
    transition: all 0.3s ease !important;
}
[data-testid="stRadio"] div[role="radiogroup"] label:hover {
    border-color: rgba(56, 189, 248, 0.3) !important;
    background: rgba(56, 189, 248, 0.04) !important;
}

/* Number input */
[data-testid="stNumberInput"] label {
    color: #94A3B8 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 14px !important;
}
[data-testid="stNumberInput"] input {
    background: rgba(15, 23, 42, 0.9) !important;
    border: 1px solid rgba(56, 189, 248, 0.2) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    caret-color: #38BDF8 !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(56, 189, 248, 0.5) !important;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.12) !important;
    background: rgba(15, 23, 42, 1) !important;
}
[data-testid="stNumberInput"] input::placeholder {
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
}
/* Number input +/- buttons */
[data-testid="stNumberInput"] button {
    color: #38BDF8 !important;
    border-color: rgba(56, 189, 248, 0.15) !important;
    background: rgba(56, 189, 248, 0.05) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stNumberInput"] button:hover {
    background: rgba(56, 189, 248, 0.12) !important;
    border-color: rgba(56, 189, 248, 0.3) !important;
}
/* Slider track & thumb */
[data-testid="stSlider"] [data-testid="stTickBar"] { background: transparent !important; }
[data-testid="stSlider"] div[role="slider"] {
    background: #38BDF8 !important;
    border-color: #38BDF8 !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.3) !important;
}
/* Slider min/max labels */
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    color: #475569 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
}

/* Form submit button */
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 0.75rem 2.5rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1) !important;
    width: 100% !important;
    margin-top: 0.5rem !important;
}
[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(56, 189, 248, 0.25) !important;
}
[data-testid="stFormSubmitButton"] button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* Hide default st.subheader */
.stSubheader, [data-testid="stSubheader"] { display: none !important; }

/* Expander override */
[data-testid="stExpander"] {
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 14px !important;
    background: rgba(15, 17, 28, 0.5) !important;
}

/* iframe */
iframe { border: none !important; }

/* ─── FOOTER ─── */
.app-footer {
    text-align: center;
    padding: 2.5rem 0 2rem;
    margin-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.03);
}
.ft { font-size: 0.65rem; color: #334155 !important; letter-spacing: 0.12em; text-transform: uppercase; }
.ft-tags { display: flex; justify-content: center; gap: 10px; margin-top: 0.6rem; flex-wrap: wrap; }
.ft-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: #475569;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.04);
    padding: 3px 10px;
    border-radius: 6px;
}

/* ─── RESPONSIVE ─── */
@media (max-width: 768px) {
    .hero-title { font-size: 2rem; }
    .hero-stats { gap: 1.5rem; }
    .form-section { padding: 1.25rem; }
}
</style>
""", unsafe_allow_html=True)


# ===============================
# RESULT HTML (via components.html)
# ===============================
def build_result_html(result, proba, record_dict):
    is_diabetic = result == 1
    prob = proba[1] * 100 if is_diabetic else proba[0] * 100
    risk_prob = proba[1] * 100

    if is_diabetic:
        color = "#FB7185"
        bg = "rgba(251, 113, 133, 0.06)"
        border = "rgba(251, 113, 133, 0.25)"
        icon = "🔴"
        label = "Diabetic — High Risk"
        tag_text = "Positive detection"
        severity = "High"
        message = "The model indicates a high probability of diabetes. Please consult a healthcare professional for comprehensive blood work and clinical evaluation."
        action = "Schedule fasting glucose and OGTT tests. Review medication options with your endocrinologist. Begin dietary modifications and increase physical activity."
    else:
        color = "#34D399"
        bg = "rgba(52, 211, 153, 0.06)"
        border = "rgba(52, 211, 153, 0.25)"
        icon = "🟢"
        label = "Not Diabetic — Low Risk"
        tag_text = "Negative detection"
        severity = "Low"
        message = "The model indicates a low probability of diabetes. Maintain your current healthy lifestyle and schedule regular checkups."
        action = "Continue balanced diet and regular exercise. Monitor blood sugar annually. Maintain healthy BMI and stay hydrated."

    # Risk factors analysis
    risk_flags = []
    if record_dict['bmi'] > 30:
        risk_flags.append(("BMI", f"{record_dict['bmi']:.1f}", "Above 30 — obese range", "#F59E0B"))
    if record_dict['a1c'] > 6.5:
        risk_flags.append(("HbA1c", f"{record_dict['a1c']:.1f}%", "Above 6.5% — diabetic range", "#FB7185"))
    elif record_dict['a1c'] > 5.7:
        risk_flags.append(("HbA1c", f"{record_dict['a1c']:.1f}%", "5.7-6.5% — prediabetic range", "#F59E0B"))
    if record_dict['bsr'] > 200:
        risk_flags.append(("Blood Sugar", str(record_dict['bsr']), "Above 200 — very high", "#FB7185"))
    elif record_dict['bsr'] > 140:
        risk_flags.append(("Blood Sugar", str(record_dict['bsr']), "140-200 — elevated", "#F59E0B"))
    if record_dict['sys'] > 140:
        risk_flags.append(("Systolic BP", str(record_dict['sys']), "Above 140 — hypertensive", "#F59E0B"))
    if record_dict['family_history'] == 1:
        risk_flags.append(("Family History", "Positive", "Genetic predisposition present", "#A78BFA"))
    if record_dict['exercise'] < 15:
        risk_flags.append(("Exercise", f"{record_dict['exercise']} min/day", "Below recommended 30 min/day", "#F59E0B"))

    risk_html = ""
    if risk_flags:
        risk_items = ""
        for name, val, desc, rcolor in risk_flags:
            risk_items += f"""
            <div style="display:flex;align-items:flex-start;gap:10px;padding:10px 12px;background:rgba(255,255,255,0.015);border:1px solid rgba(255,255,255,0.04);border-radius:10px;">
                <div style="width:4px;height:36px;border-radius:4px;background:{rcolor};flex-shrink:0;margin-top:2px;"></div>
                <div style="flex:1;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-size:12px;font-weight:600;color:#E2E8F0;">{name}</span>
                        <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:{rcolor};font-weight:500;">{val}</span>
                    </div>
                    <div style="font-size:11px;color:#64748B;margin-top:2px;">{desc}</div>
                </div>
            </div>
            """
        risk_html = f"""
        <div style="margin-top:1.5rem;padding-top:1.25rem;border-top:1px solid rgba(255,255,255,0.05);">
            <div style="font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;margin-bottom:0.85rem;">⚡ Risk Factor Analysis</div>
            <div style="display:flex;flex-direction:column;gap:8px;">
                {risk_items}
            </div>
        </div>
        """
    else:
        risk_html = """
        <div style="margin-top:1.5rem;padding-top:1.25rem;border-top:1px solid rgba(255,255,255,0.05);">
            <div style="font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;margin-bottom:0.85rem;">⚡ Risk Factor Analysis</div>
            <div style="font-size:13px;color:#34D399;padding:12px;background:rgba(52,211,153,0.04);border:1px solid rgba(52,211,153,0.15);border-radius:10px;">
                All monitored parameters are within healthy ranges. No significant risk factors detected.
            </div>
        </div>
        """

    # Gauge visual
    gauge_pct = risk_prob
    gauge_color = "#34D399" if gauge_pct < 30 else ("#F59E0B" if gauge_pct < 60 else "#FB7185")
    gauge_label = "Low" if gauge_pct < 30 else ("Moderate" if gauge_pct < 60 else "High")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        *{{margin:0;padding:0;box-sizing:border-box;}}
        body{{font-family:'Plus Jakarta Sans',sans-serif;background:transparent;color:#E2E8F0;padding:6px;}}
        .card{{background:{bg};border:1px solid {border};border-radius:20px;padding:1.75rem;animation:pop 0.8s cubic-bezier(0.22,1,0.36,1);}}
        @keyframes pop{{from{{opacity:0;transform:translateY(25px) scale(0.97);}}to{{opacity:1;transform:translateY(0) scale(1);}}}}
        .hdr{{display:flex;align-items:center;gap:14px;margin-bottom:1.5rem;padding-bottom:1.25rem;border-bottom:1px solid rgba(255,255,255,0.05);}}
        .ico{{width:54px;height:54px;border-radius:14px;background:{bg};border:1px solid {border};display:flex;align-items:center;justify-content:center;font-size:26px;}}
        .cls{{font-size:1.35rem;font-weight:700;color:#E2E8F0;}}
        .tag{{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:{color};margin-top:3px;}}

        .gauge-area{{display:flex;gap:1.5rem;margin-bottom:1.5rem;flex-wrap:wrap;}}
        .gauge-box{{flex:1;min-width:180px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);border-radius:14px;padding:1.25rem;text-align:center;}}
        .gauge-label{{font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;margin-bottom:0.75rem;}}
        .gauge-ring{{width:100px;height:100px;border-radius:50%;margin:0 auto 0.75rem;position:relative;
            background:conic-gradient({gauge_color} 0% {gauge_pct}%, rgba(255,255,255,0.04) {gauge_pct}% 100%);
            display:flex;align-items:center;justify-content:center;}}
        .gauge-inner{{width:78px;height:78px;border-radius:50%;background:#0F1120;display:flex;flex-direction:column;align-items:center;justify-content:center;}}
        .gauge-pct{{font-family:'JetBrains Mono',monospace;font-size:20px;font-weight:700;color:{gauge_color};}}
        .gauge-txt{{font-size:9px;color:#64748B;text-transform:uppercase;letter-spacing:0.08em;margin-top:2px;}}
        .gauge-status{{font-size:13px;font-weight:600;color:{gauge_color};}}

        .info-row{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:1.5rem;}}
        .info-box{{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.04);border-radius:12px;padding:0.85rem;}}
        .info-lbl{{font-size:9px;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;font-weight:600;}}
        .info-val{{font-size:13px;color:#E2E8F0;font-weight:500;}}

        .desc{{font-size:13px;color:#94A3B8;line-height:1.75;margin-bottom:1.25rem;}}

        .abox{{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:14px;padding:1.15rem;}}
        .ah{{display:flex;align-items:center;gap:8px;margin-bottom:0.6rem;}}
        .at{{font-size:10px;color:#E2E8F0;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;}}
        .atxt{{font-size:13px;color:#94A3B8;line-height:1.7;}}

        .prob-section{{margin-top:1.5rem;padding-top:1.25rem;border-top:1px solid rgba(255,255,255,0.05);}}
        .prob-title{{font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1rem;font-weight:600;}}
        .prob-row{{display:flex;align-items:center;gap:12px;margin-bottom:10px;}}
        .prob-name{{font-size:13px;color:#94A3B8;width:120px;flex-shrink:0;}}
        .prob-bar{{flex:1;height:6px;background:rgba(255,255,255,0.04);border-radius:100px;overflow:hidden;}}
        .prob-fill{{height:100%;border-radius:100px;}}
        .prob-val{{font-family:'JetBrains Mono',monospace;font-size:12px;color:#64748B;width:55px;text-align:right;flex-shrink:0;}}

        @media(max-width:600px){{
            .info-row{{grid-template-columns:1fr;}}
            .gauge-area{{flex-direction:column;}}
        }}
    </style>
    </head>
    <body>
    <div class="card">
        <div class="hdr">
            <div class="ico">{icon}</div>
            <div>
                <div class="cls">{label}</div>
                <div class="tag">{tag_text}</div>
            </div>
        </div>

        <div class="gauge-area">
            <div class="gauge-box">
                <div class="gauge-label">Diabetes Risk Score</div>
                <div class="gauge-ring">
                    <div class="gauge-inner">
                        <div class="gauge-pct">{risk_prob:.0f}%</div>
                        <div class="gauge-txt">risk</div>
                    </div>
                </div>
                <div class="gauge-status">{gauge_label} Risk</div>
            </div>
            <div style="flex:1.5;display:flex;flex-direction:column;justify-content:center;">
                <div class="info-row" style="margin-bottom:0;">
                    <div class="info-box">
                        <div class="info-lbl">Confidence</div>
                        <div class="info-val" style="color:{color};">{prob:.1f}%</div>
                    </div>
                    <div class="info-box">
                        <div class="info-lbl">Severity</div>
                        <div class="info-val">{severity}</div>
                    </div>
                    <div class="info-box">
                        <div class="info-lbl">Model</div>
                        <div class="info-val">AdaBoost</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="desc">{message}</div>

        <div class="abox">
            <div class="ah">
                <span style="font-size:14px;">💊</span>
                <span class="at">Recommended Action</span>
            </div>
            <div class="atxt">{action}</div>
        </div>

        <div class="prob-section">
            <div class="prob-title">Classification Probabilities</div>
            <div class="prob-row">
                <span class="prob-name">Not Diabetic</span>
                <div class="prob-bar"><div class="prob-fill" style="width:{proba[0]*100:.1f}%;background:#34D399;"></div></div>
                <span class="prob-val">{proba[0]*100:.1f}%</span>
            </div>
            <div class="prob-row">
                <span class="prob-name">Diabetic</span>
                <div class="prob-bar"><div class="prob-fill" style="width:{proba[1]*100:.1f}%;background:#FB7185;"></div></div>
                <span class="prob-val">{proba[1]*100:.1f}%</span>
            </div>
        </div>

        {risk_html}
    </div>
    </body>
    </html>
    """


def build_scan_html(step=1):
    msgs = [
        ("Preprocessing patient data...", "Validating 17 clinical parameters"),
        ("Running AdaBoost classifier...", "Analyzing feature interactions"),
        ("Computing risk assessment...", "Generating clinical report"),
    ]
    msg = msgs[min(step - 1, 2)]
    steps = [
        ("Validate", "done" if step >= 1 else ""),
        ("Preprocess", "active" if step == 1 else ("done" if step > 1 else "")),
        ("Classify", "active" if step == 2 else ("done" if step > 2 else "")),
        ("Report", "active" if step == 3 else ""),
    ]
    sh = ""
    for l, c in steps:
        sh += f'<div class="s {c}"><span class="d"></span><span>{l}</span></div>'

    return f"""
    <!DOCTYPE html><html><head><meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
    <style>
        *{{margin:0;padding:0;box-sizing:border-box;}}
        body{{font-family:'Plus Jakarta Sans',sans-serif;background:transparent;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:240px;padding:2rem 1rem;}}
        .ring{{width:64px;height:64px;border-radius:50%;border:3px solid rgba(56,189,248,0.12);border-top-color:#38BDF8;animation:sp 1s linear infinite;display:flex;align-items:center;justify-content:center;font-size:24px;margin-bottom:1.25rem;}}
        @keyframes sp{{to{{transform:rotate(360deg);}}}}
        .t1{{font-size:14px;color:#38BDF8;font-weight:500;text-align:center;}}
        .t2{{font-size:11px;color:#475569;margin-top:0.3rem;text-align:center;}}
        .pr{{display:flex;justify-content:center;gap:1.5rem;margin-top:1.5rem;flex-wrap:wrap;}}
        .s{{display:flex;align-items:center;gap:5px;font-size:10px;color:#334155;}}
        .s.active{{color:#38BDF8;}}
        .s.done{{color:#94A3B8;}}
        .d{{width:6px;height:6px;border-radius:50%;background:#1E293B;display:inline-block;}}
        .s.done .d{{background:#94A3B8;}}
        .s.active .d{{background:#38BDF8;box-shadow:0 0 8px rgba(56,189,248,0.4);}}
    </style></head><body>
    <div class="ring">🧬</div>
    <div class="t1">{msg[0]}</div>
    <div class="t2">{msg[1]}</div>
    <div class="pr">{sh}</div>
    </body></html>
    """


# ===============================
# STREAMLIT UI
# ===============================

# ─── HERO ───
st.markdown("""
<div class="hero">
    <div class="hero-badge">
        <span class="dot"></span>
        AI Clinical Analyzer
    </div>
    <div class="hero-title">Diabetes Risk<br>Prediction</div>
    <div class="hero-sub">
        Enter patient clinical parameters and let our machine learning model
        assess diabetes risk with intelligent analysis in seconds.
    </div>
    <div class="hero-stats">
        <div class="hs-item"><div class="hs-val">17</div><div class="hs-lbl">Parameters</div></div>
        <div class="hs-item"><div class="hs-val">AdaBoost</div><div class="hs-lbl">Classifier</div></div>
        <div class="hs-item"><div class="hs-val">2</div><div class="hs-lbl">Classes</div></div>
        <div class="hs-item"><div class="hs-val">&lt;1s</div><div class="hs-lbl">Inference</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ─── FORM ───
with st.form("form"):

    # Section 1 — Demographics
    st.markdown("""
    <div class="form-section-head">
        <div class="fs-icon" style="background:rgba(56,189,248,0.08);border:1px solid rgba(56,189,248,0.15);">🧍</div>
        <div>
            <div class="fs-title">Demographics</div>
            <div class="fs-sub">Basic patient information</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    with d1:
        age = st.slider("Age", 10, 100, 30)
    with d2:
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    with d3:
        rgn = st.radio("Region", ["Urban", "Rural"], horizontal=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Section 2 — Body Metrics
    st.markdown("""
    <div class="form-section-head">
        <div class="fs-icon" style="background:rgba(168,85,247,0.08);border:1px solid rgba(168,85,247,0.15);">⚖️</div>
        <div>
            <div class="fs-title">Body Metrics</div>
            <div class="fs-sub">Physical measurements and vitals</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    with b1:
        wt = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
    with b2:
        bmi = st.number_input("BMI", 10.0, 60.0, 24.0)
    with b3:
        wst = st.number_input("Waist (inches)", 20.0, 80.0, 34.0)

    bp1, bp2 = st.columns(2)
    with bp1:
        sys = st.slider("Systolic BP", 80, 200, 120)
    with bp2:
        dia = st.slider("Diastolic BP", 50, 120, 80)

    st.markdown("<br>", unsafe_allow_html=True)

    # Section 3 — Blood Work
    st.markdown("""
    <div class="form-section-head">
        <div class="fs-icon" style="background:rgba(251,113,133,0.08);border:1px solid rgba(251,113,133,0.15);">🩸</div>
        <div>
            <div class="fs-title">Blood Work</div>
            <div class="fs-sub">Lab results and glucose markers</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    bl1, bl2, bl3 = st.columns(3)
    with bl1:
        a1c = st.number_input("Hemoglobin A1c (%)", 3.0, 15.0, 5.5)
    with bl2:
        bsr = st.number_input("Random Blood Sugar", 50, 500, 90)
    with bl3:
        hdl = st.number_input("HDL Cholesterol", 10, 100, 50)

    st.markdown("<br>", unsafe_allow_html=True)

    # Section 4 — Clinical History
    st.markdown("""
    <div class="form-section-head">
        <div class="fs-icon" style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.15);">📋</div>
        <div>
            <div class="fs-title">Clinical History & Symptoms</div>
            <div class="fs-sub">Medical background and current symptoms</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        his = st.radio("Family History of Diabetes", ["No", "Yes"], horizontal=True)
        vision = st.radio("Vision Issues", ["No", "Yes"], horizontal=True)
        dipsia = st.radio("Dipsia (Excessive Thirst)", ["No", "Yes"], horizontal=True)
    with c2:
        uria = st.radio("Uria (Sugar/Protein in Urine)", ["No", "Yes"], horizontal=True)
        neph = st.radio("Nephropathy (Kidney Issues)", ["No", "Yes"], horizontal=True)
        exr = st.slider("Exercise (minutes/day)", 0, 120, 30)

    st.markdown("<br>", unsafe_allow_html=True)

    predict_button = st.form_submit_button("🧬  Analyze Patient Risk")


# ===============================
# PREDICTION
# ===============================
if predict_button:
    record = [
        age,
        1 if gender == "Male" else 0,
        0 if rgn == "Urban" else 1,
        wt,
        bmi,
        wst,
        sys,
        dia,
        1 if his == "Yes" else 0,
        a1c,
        bsr,
        1 if vision == "Yes" else 0,
        exr,
        1 if dipsia == "Yes" else 0,
        1 if uria == "Yes" else 0,
        1 if neph == "Yes" else 0,
        hdl
    ]

    record_dict = {
        'age': age, 'bmi': bmi, 'a1c': a1c, 'bsr': bsr,
        'sys': sys, 'dia': dia, 'family_history': 1 if his == "Yes" else 0,
        'exercise': exr, 'hdl': hdl, 'wt': wt, 'wst': wst
    }

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ─── SCANNING ANIMATION ───
    scan_slot = st.empty()
    with scan_slot.container():
        components.html(build_scan_html(step=1), height=280)
    time.sleep(0.7)

    scan_slot.empty()
    with scan_slot.container():
        components.html(build_scan_html(step=2), height=280)

    # ─── ACTUAL PREDICTION (LOGIC UNTOUCHED) ───
    proba = model.predict_proba(np.array([record]))[0]
    result = model.predict(np.array([record]))[0]

    time.sleep(0.5)

    # ─── SHOW RESULT ───
    scan_slot.empty()
    with scan_slot.container():
        components.html(build_result_html(result, proba, record_dict), height=900, scrolling=True)


# ─── FOOTER ───
st.markdown("""
<div class="app-footer">
    <div class="ft">Built with precision for portfolio demonstration</div>
    <div class="ft-tags">
        <span class="ft-tag">Scikit-Learn</span>
        <span class="ft-tag">AdaBoost</span>
        <span class="ft-tag">Streamlit</span>
        <span class="ft-tag">Python</span>
        <span class="ft-tag">17 Features</span>
    </div>
</div>
""", unsafe_allow_html=True)
