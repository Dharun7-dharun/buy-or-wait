import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, timedelta
from pathlib import Path
from collections import Counter
import sys

# Ensure code directory is in sys.path
CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from main import Engine, OUTPUT_COLS

# Page Configuration
st.set_page_config(
    page_title="Buy or Wait? — AI Financial Advisor",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom High-Quality CSS Styling with Micro-Animations
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Animation Keyframes */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes pulseGlowGreen {
        0% { box-shadow: 0 0 12px rgba(16, 185, 129, 0.25); border-color: #10B981; }
        50% { box-shadow: 0 0 28px rgba(16, 185, 129, 0.65); border-color: #34D399; }
        100% { box-shadow: 0 0 12px rgba(16, 185, 129, 0.25); border-color: #10B981; }
    }
    
    @keyframes pulseGlowBlue {
        0% { box-shadow: 0 0 12px rgba(59, 130, 246, 0.25); border-color: #3B82F6; }
        50% { box-shadow: 0 0 28px rgba(59, 130, 246, 0.65); border-color: #60A5FA; }
        100% { box-shadow: 0 0 12px rgba(59, 130, 246, 0.25); border-color: #3B82F6; }
    }
    
    @keyframes pulseGlowAmber {
        0% { box-shadow: 0 0 12px rgba(245, 158, 11, 0.25); border-color: #F59E0B; }
        50% { box-shadow: 0 0 28px rgba(245, 158, 11, 0.65); border-color: #FBBF24; }
        100% { box-shadow: 0 0 12px rgba(245, 158, 11, 0.25); border-color: #F59E0B; }
    }
    
    @keyframes pulseGlowRed {
        0% { box-shadow: 0 0 12px rgba(239, 68, 68, 0.25); border-color: #EF4444; }
        50% { box-shadow: 0 0 28px rgba(239, 68, 68, 0.65); border-color: #F87171; }
        100% { box-shadow: 0 0 12px rgba(239, 68, 68, 0.25); border-color: #EF4444; }
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(18px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes meterFill {
        from { width: 0%; }
        to { width: var(--meter-width, 70%); }
    }

    /* Header Card */
    .app-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 22px 28px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        animation: slideInUp 0.5s ease-out;
    }
    .app-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8, #818CF8, #F472B6, #38BDF8);
        background-size: 300% auto;
        animation: gradientShift 6s linear infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 6px 0;
    }
    .app-subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        margin: 0;
        line-height: 1.5;
    }

    /* Animated Verdict Banners */
    .verdict-banner {
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 20px;
        animation: slideInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        transition: all 0.3s ease;
    }
    .verdict-affordable_now {
        background: linear-gradient(135deg, rgba(6, 95, 70, 0.35) 0%, rgba(6, 78, 59, 0.65) 100%);
        animation: pulseGlowGreen 3.5s infinite ease-in-out, slideInUp 0.6s ease-out;
    }
    .verdict-affordable_with_plan {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.35) 0%, rgba(30, 64, 175, 0.65) 100%);
        animation: pulseGlowBlue 3.5s infinite ease-in-out, slideInUp 0.6s ease-out;
    }
    .verdict-affordable_later {
        background: linear-gradient(135deg, rgba(146, 64, 14, 0.35) 0%, rgba(120, 53, 15, 0.65) 100%);
        animation: pulseGlowAmber 3.5s infinite ease-in-out, slideInUp 0.6s ease-out;
    }
    .verdict-not_affordable {
        background: linear-gradient(135deg, rgba(153, 27, 27, 0.35) 0%, rgba(127, 29, 29, 0.65) 100%);
        animation: pulseGlowRed 3.5s infinite ease-in-out, slideInUp 0.6s ease-out;
    }
    .verdict-headline {
        font-size: 1.65rem;
        font-weight: 800;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .verdict-subtext {
        font-size: 1.08rem;
        line-height: 1.55;
        color: #F8FAFC;
    }

    /* Interactive Hover KPI Cards */
    .kpi-card {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
        height: 100%;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .kpi-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.4), 0 0 16px rgba(56, 189, 248, 0.3);
        border-color: rgba(56, 189, 248, 0.5);
    }
    .kpi-title {
        font-size: 0.82rem;
        color: #94A3B8;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-number {
        font-size: 1.65rem;
        font-weight: 800;
        color: #F8FAFC;
    }
    .kpi-desc {
        font-size: 0.8rem;
        color: #64748B;
        margin-top: 4px;
    }

    /* Animated Traffic Light Meter */
    .meter-container {
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 14px;
        padding: 18px 22px;
        margin: 18px 0;
    }
    .meter-track {
        height: 16px;
        background: linear-gradient(90deg, #10B981 0%, #3B82F6 50%, #F59E0B 75%, #EF4444 100%);
        border-radius: 999px;
        position: relative;
        margin: 14px 0 8px 0;
    }
    .meter-pointer {
        position: absolute;
        top: -6px;
        width: 28px;
        height: 28px;
        background: #FFFFFF;
        border: 3px solid #0F172A;
        border-radius: 50%;
        transform: translateX(-50%);
        box-shadow: 0 0 12px rgba(255, 255, 255, 0.8);
        transition: left 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .meter-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #94A3B8;
    }

    /* Audit Step Grid */
    .audit-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 12px;
        margin-top: 14px;
    }
    .audit-step {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px 16px;
        transition: all 0.25s ease;
    }
    .audit-step:hover {
        background: rgba(30, 41, 59, 0.9);
        border-color: #38BDF8;
    }
    .audit-step-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
        font-size: 0.9rem;
        color: #38BDF8;
        margin-bottom: 4px;
    }
    .audit-step-body {
        font-size: 0.88rem;
        color: #CBD5E1;
        line-height: 1.35;
    }

    /* Question Bubble */
    .user-question-bubble {
        background: linear-gradient(135deg, #1E293B, #0F172A);
        border-left: 6px solid #38BDF8;
        border-radius: 0 16px 16px 0;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        animation: slideInUp 0.4s ease-out;
    }
    .question-tag {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #38BDF8;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
    }
    .question-text {
        font-size: 1.25rem;
        font-weight: 600;
        font-style: italic;
        color: #FFFFFF;
        line-height: 1.45;
    }
</style>
""", unsafe_allow_html=True)


# --- LOAD ENGINE ---
@st.cache_resource(show_spinner="Starting AI Financial Engine...")
def load_engine():
    return Engine()

engine = load_engine()

# Cache ground-truth predictions
@st.cache_data(show_spinner="Running 90-day simulations across dataset...")
def get_all_predictions():
    records = []
    for r in engine.requests:
        rec = engine.recommend(r)
        records.append({**r, **rec})
    return pd.DataFrame(records)

all_preds_df = get_all_predictions()

CATEGORY_ICONS = {
    "purchase": ("🛍️", "Shopping & Electronics"),
    "travel": ("✈️", "Travel & Vacation"),
    "education": ("🎓", "Education & Courses"),
    "family_transfer": ("👨‍👩‍👧", "Family Support"),
    "debt_repayment": ("💳", "Debt Repayment"),
    "investment": ("📈", "Investment / Asset"),
    "housing": ("🏠", "Home & Housing"),
    "emergency_expense": ("🚨", "Emergency Expense"),
    "other": ("📦", "General Expense")
}

def get_cat_info(cat):
    return CATEGORY_ICONS.get(cat, ("🏷️", cat.replace("_", " ").title()))


# --- APP HEADER ---
st.markdown("""
<div class="app-header">
    <div class="app-title">💸 Buy or Wait? — AI Financial Advisor</div>
    <div class="app-subtitle">
        <b>Interactive Personal Affordability & 90-Day Cash Flow Simulator.</b><br>
        Ask any expense question, simulate custom purchases, toggle subscriptions on/off, and verify that your bank balance never breaches your emergency reserve.
    </div>
</div>
""", unsafe_allow_html=True)


# --- TOP LEVEL NAVIGATION MODES ---
nav_mode = st.radio(
    "Choose Experience Mode:",
    [
        "🔎 Browse Inquiries & Live Scenarios",
        "🧮 Ask Your Own Expense Question (Interactive Simulator)",
        "💬 Chat with AI Financial Assistant",
        "🗂️ All 250 Predictions Table (Benchmark & CSV)"
    ],
    horizontal=True
)

st.markdown("---")


# ==============================================================================
# MODE 1: BROWSE INQUIRIES & LIVE SCENARIOS
# ==============================================================================
if nav_mode.startswith("🔎"):
    st.sidebar.title("🎯 Choose an Inquiry")
    
    # Presets
    st.sidebar.markdown("### ⚡ Quick Presets:")
    col_p1, col_p2 = st.sidebar.columns(2)
    if col_p1.button("🟢 Buy Today", help="request_26: Safe family transfer"):
        st.session_state["selected_rid"] = "request_26"
    if col_p2.button("💳 Split Plan", help="request_49: Safe with 3 installments"):
        st.session_state["selected_rid"] = "request_49"
    if col_p1.button("⏳ Wait Payday", help="request_31: Safe once salary arrives"):
        st.session_state["selected_rid"] = "request_31"
    if col_p2.button("✂️ Partial Pay", help="request_46: Safe paying half now, half later"):
        st.session_state["selected_rid"] = "request_46"
    if st.sidebar.button("⛔ Risky Expense", help="request_28: Breaches safety buffer"):
        st.session_state["selected_rid"] = "request_28"

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Filters:")
    
    filter_status = st.sidebar.selectbox(
        "Decision Type",
        ["All", "affordable_now", "affordable_with_plan", "affordable_later", "not_affordable"],
        format_func=lambda x: "All Decisions" if x == "All" else x.replace("_", " ").title()
    )
    
    user_currencies = ["All"] + sorted(list(set(engine.profiles[r["user_id"]]["home_currency"] for r in engine.requests)))
    filter_cur = st.sidebar.selectbox("Currency", user_currencies)
    
    user_categories = ["All"] + sorted(list(set(r["request_type"] for r in engine.requests)))
    filter_cat = st.sidebar.selectbox("Category", user_categories, format_func=lambda c: "All Categories" if c == "All" else get_cat_info(c)[1])
    
    search_text = st.sidebar.text_input("Search keyword or User ID", "").strip().lower()

    # Filter records
    filtered_list = []
    for r in engine.requests:
        uid = r["user_id"]
        prof = engine.profiles[uid]
        pred_row = all_preds_df.loc[all_preds_df["request_id"] == r["request_id"]].iloc[0]
        if filter_status != "All" and pred_row["affordability_status"] != filter_status:
            continue
        if filter_cur != "All" and prof["home_currency"] != filter_cur:
            continue
        if filter_cat != "All" and r["request_type"] != filter_cat:
            continue
        if search_text:
            if search_text not in r["request_id"].lower() and search_text not in r["user_id"].lower() and search_text not in r["request_text"].lower():
                continue
        filtered_list.append(r)

    if not filtered_list:
        st.sidebar.warning("No matches found. Showing all.")
        filtered_list = engine.requests

    req_ids = [r["request_id"] for r in filtered_list]
    if "selected_rid" not in st.session_state or st.session_state["selected_rid"] not in req_ids:
        st.session_state["selected_rid"] = req_ids[0]

    def format_inquiry_label(rid):
        r_obj = next((x for x in engine.requests if x["request_id"] == rid), None)
        if not r_obj: return rid
        prof = engine.profiles[r_obj["user_id"]]
        icon, name = get_cat_info(r_obj["request_type"])
        return f"{icon} {rid} • {prof['home_currency']} {float(r_obj['requested_amount']):,.0f} • {r_obj['user_id']}"

    cur_idx = req_ids.index(st.session_state["selected_rid"])
    selected_rid = st.sidebar.selectbox("Select Inquiry", req_ids, index=cur_idx, format_func=format_inquiry_label)
    st.session_state["selected_rid"] = selected_rid

    # Run diagnostic
    diag = engine.diagnose(selected_rid)
    req = diag["request"]
    prof = diag["profile"]
    rec = diag["recommendation"]
    cur = diag["home_currency"]
    req_amt = diag["requested_amount"]
    safe_amt = diag["safe_amount_today"]
    avail_bal = diag["current_available_balance"]
    min_bal = diag["minimum_balance_to_keep"]
    status = rec["affordability_status"]
    method = rec["recommended_payment_method"]
    cat_icon, cat_name = get_cat_info(req["request_type"])

    # 1. User Question Card
    st.markdown(f"""
    <div class="user-question-bubble">
        <div class="question-tag">{cat_icon} {cat_name} • Requested for {req['request_date']} • Deadline: {req['desired_completion_date']}</div>
        <div class="question-text">“{req['request_text']}”</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Interactive Budget Adjuster (Toggle Subscriptions ON/OFF)
    st.markdown("### 🎛️ Interactive Budget Toggles (Test What-If Scenarios)")
    st.caption("See how pausing optional subscriptions or reducing flexible spending immediately changes your 90-day safety cushion!")

    streams = diag["recurring_streams"]
    flexible_streams = [s for s in streams if s["key"][2] == "debit" and s["key"][3] in ("stoppable", "reducible", "reducible_or_stoppable")]

    stop_events_selected = set()
    reduce_events_selected = {}

    if flexible_streams:
        st.write("Check any flexible expense to pause or trim it:")
        t_cols = st.columns(min(3, len(flexible_streams)))
        for idx, s in enumerate(flexible_streams):
            col_target = t_cols[idx % len(t_cols)]
            cat_clean = s["key"][1].replace("_", " ").title()
            ev_id = s["history"][-1].event_id
            avg_amt = s["amount"]
            
            with col_target:
                is_checked = st.checkbox(
                    f"🛑 Pause {cat_clean} (~{cur} {avg_amt:,.0f}/mo)",
                    key=f"toggle_stream_{ev_id}_{selected_rid}",
                    help=f"Temporarily stop {cat_clean} to increase safety buffer"
                )
                if is_checked:
                    stop_events_selected.add(ev_id)
    else:
        st.write("*(No flexible subscriptions recorded for this user.)*")

    # If user selected custom spending cuts, recalculate with override!
    active_changes = {"stop": stop_events_selected, "reduce": reduce_events_selected} if stop_events_selected else None
    if active_changes:
        custom_sim = engine.evaluate_custom(
            user_id=req["user_id"],
            amount=req_amt,
            req_date=req["request_date"],
            deadline=req["desired_completion_date"],
            category=req["request_type"],
            allows_partial=str(req["allows_partial_payment"]).lower() == "true",
            request_text=req["request_text"],
            changes_override=active_changes
        )
        plan_traj = custom_sim["custom_plan_trajectory"]
        lowest_bal = custom_sim["custom_lowest_balance"]
        is_safe_now = custom_sim["custom_is_safe"]
        st.success(f"🎉 **Live Simulation Updated!** By pausing the selected expenses, your lowest balance increases to **{cur} {lowest_bal:,.2f}** (Safe: {'YES ✅' if is_safe_now else 'Still below floor ⚠️'}).")
    else:
        plan_traj = diag["plan_trajectory"]
        lowest_bal = diag["lowest_balance_with_plan"]

    # 3. Big Plain-English Animated Verdict
    st.markdown("### 🤖 The Verdict")
    if status == "affordable_now":
        st.markdown(f"""
        <div class="verdict-banner verdict-affordable_now">
            <div class="verdict-headline" style="color: #34D399;">✅ YES, YOU CAN AFFORD THIS TODAY!</div>
            <div class="verdict-subtext">You have plenty of cash to safely pay <b>{cur} {req_amt:,.2f}</b> today. After paying, your account stays safely above your <b>{cur} {min_bal:,.2f}</b> emergency buffer.</div>
        </div>
        """, unsafe_allow_html=True)
    elif status == "affordable_with_plan":
        st.markdown(f"""
        <div class="verdict-banner verdict-affordable_with_plan">
            <div class="verdict-headline" style="color: #60A5FA;">🔵 YES, YOU CAN AFFORD THIS WITH A PAYMENT PLAN!</div>
            <div class="verdict-subtext">Paying all at once today would cut too close to your safety buffer. But you can safely complete it using <b>{method.replace('_', ' ').title()}</b> before your deadline of <b>{req['desired_completion_date']}</b>!</div>
        </div>
        """, unsafe_allow_html=True)
    elif status == "affordable_later":
        st.markdown(f"""
        <div class="verdict-banner verdict-affordable_later">
            <div class="verdict-headline" style="color: #FBBF24;">⏳ WAIT UNTIL {rec['earliest_date_for_full_payment']} BEFORE BUYING</div>
            <div class="verdict-subtext">Holding off until <b>{rec['earliest_date_for_full_payment']}</b> lets your next confirmed salary arrive, allowing you to pay in full without risking your emergency savings.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="verdict-banner verdict-not_affordable">
            <div class="verdict-headline" style="color: #F87171;">⛔ NOT RECOMMENDED RIGHT NOW</div>
            <div class="verdict-subtext">Buying today would endanger your emergency buffer. You only have <b>{cur} {safe_amt:,.2f}</b> safely available to spend today.</div>
        </div>
        """, unsafe_allow_html=True)

    # 4. 4 KPI Snapshot Cards with Hover Micro-Animations
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"""<div class="kpi-card"><div class="kpi-title">Current Balance</div><div class="kpi-number">{cur} {avail_bal:,.2f}</div><div class="kpi-desc">Available cash today</div></div>""", unsafe_allow_html=True)
    k2.markdown(f"""<div class="kpi-card"><div class="kpi-title">Emergency Buffer</div><div class="kpi-number" style="color: #CBD5E1;">{cur} {min_bal:,.2f}</div><div class="kpi-desc">Required reserve floor</div></div>""", unsafe_allow_html=True)
    k3.markdown(f"""<div class="kpi-card"><div class="kpi-title">Requested Amount</div><div class="kpi-number" style="color: {'#34D399' if status in ('affordable_now', 'affordable_with_plan') else '#F87171'};">{cur} {req_amt:,.2f}</div><div class="kpi-desc">Expense cost</div></div>""", unsafe_allow_html=True)
    k4.markdown(f"""<div class="kpi-card"><div class="kpi-title">Max Safe to Pay Today</div><div class="kpi-number" style="color: #38BDF8;">{cur} {safe_amt:,.2f}</div><div class="kpi-desc">Immediate safe limit</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Visual Animated Traffic Light Meter Gauge
    st.markdown("### 🚦 Visual Affordability Meter Gauge")
    
    # Calculate pointer position on 0% to 100% track
    gauge_max = max(req_amt, safe_amt * 1.5, 1.0)
    percent_pos = min(98.0, max(2.0, (req_amt / gauge_max) * 100))
    meter_color = "#10B981" if status == "affordable_now" else ("#3B82F6" if status == "affordable_with_plan" else ("#F59E0B" if status == "affordable_later" else "#EF4444"))
    
    st.markdown(f"""
    <div class="meter-container">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 700; color: #F8FAFC; font-size: 0.95rem;">Expense Affordability Position:</span>
            <span style="font-weight: 800; color: {meter_color}; font-size: 1rem;">{status.replace('_', ' ').upper()}</span>
        </div>
        <div class="meter-track">
            <div class="meter-pointer" style="left: {percent_pos}%; background: {meter_color};"></div>
        </div>
        <div class="meter-labels">
            <span>🟢 0 Safe Headroom</span>
            <span>🔵 Safe with Plan</span>
            <span>🟡 Wait for Payday</span>
            <span>🔴 High Risk Deficit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. Step-by-Step Financial Health Audit Checklist
    st.markdown("### 🛡️ Step-by-Step Safety Audit")
    cushion = lowest_bal - min_bal
    
    st.markdown(f"""
    <div class="audit-grid">
        <div class="audit-step">
            <div class="audit-step-header">🏦 1. Current Balance</div>
            <div class="audit-step-body"><b>{cur} {avail_bal:,.2f}</b> currently verified in your account.</div>
        </div>
        <div class="audit-step">
            <div class="audit-step-header">🔒 2. Emergency Floor</div>
            <div class="audit-step-body"><b>{cur} {min_bal:,.2f}</b> strictly locked away for safety.</div>
        </div>
        <div class="audit-step">
            <div class="audit-step-header">🔄 3. 90-Day Cash Flows</div>
            <div class="audit-step-body">Simulated <b>{len(streams)} recurring streams</b> (rent, bills, salary).</div>
        </div>
        <div class="audit-step">
            <div class="audit-step-header">🎯 4. Lowest Safety Cushion</div>
            <div class="audit-step-body">Lowest balance will be <b>{cur} {lowest_bal:,.2f}</b> (Margin: <b>{cur} {cushion:+,.2f}</b>).</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 7. Interactive Price Slider
    st.markdown("### 🎚️ Test Different Price Points")
    slider_max = float(max(req_amt * 2.0, avail_bal * 1.2, 500.0))
    test_val = st.slider(f"What if this expense cost a different amount? ({cur})", 0.0, slider_max, float(req_amt), float(max(1.0, round(slider_max/100))))
    
    if test_val <= safe_amt + 1e-7:
        st.success(f"🟢 **Safe Today!** Spending **{cur} {test_val:,.2f}** today leaves a comfortable margin above your emergency floor.")
    else:
        over = test_val - safe_amt
        st.error(f"🔴 **Unsafe!** Spending **{cur} {test_val:,.2f}** exceeds your safe spending limit by **{cur} {over:,.2f}**.")

    # 8. Chart: 90-Day Money Journey
    st.markdown("---")
    st.markdown("### 📈 90-Day Projected Cash Flow Curve")
    
    chart_data = []
    base_traj = diag["baseline_trajectory"]
    for b, p in zip(base_traj, plan_traj):
        chart_data.append({
            "Date": b["date"].isoformat(),
            "Projected Balance": p["balance"],
            "Emergency Buffer Floor": b["minimum"]
        })
    df_c = pd.DataFrame(chart_data).melt(id_vars=["Date"], var_name="Type", value_name="Balance")
    
    altair_chart = alt.Chart(df_c).mark_line().encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y("Balance:Q", title=f"Account Balance ({cur})"),
        color=alt.Color("Type:N", scale=alt.Scale(domain=["Projected Balance", "Emergency Buffer Floor"], range=["#38BDF8", "#EF4444"]), legend=alt.Legend(orient="top", title=None)),
        strokeDash=alt.condition(alt.datum.Type == "Emergency Buffer Floor", alt.value([6, 4]), alt.value([0])),
        strokeWidth=alt.condition(alt.datum.Type == "Projected Balance", alt.value(2.8), alt.value(1.8)),
        tooltip=["Date:T", "Type:N", alt.Tooltip("Balance:Q", format=",.2f")]
    ).properties(height=360).interactive()
    
    st.altair_chart(altair_chart, width="stretch")


# ==============================================================================
# MODE 2: ASK YOUR OWN EXPENSE QUESTION (INTERACTIVE SIMULATOR)
# ==============================================================================
elif nav_mode.startswith("🧮"):
    st.markdown("## 🧮 Custom Expense Affordability Simulator")
    st.write("Type your own financial question or configure custom amounts, dates, and guardrails to run an instant 90-day simulation!")

    with st.form("custom_expense_form"):
        st.markdown("#### 1. Who is asking?")
        all_uids = sorted(list(engine.profiles.keys()))
        def format_user_option(uid):
            p = engine.profiles[uid]
            return f"👤 {uid} ({p['home_currency']} • Balance: {float(p['current_available_balance']):,.0f} • Floor: {float(p['minimum_balance_to_keep']):,.0f})"
        
        sim_user = st.selectbox("Select User Profile", all_uids, format_func=format_user_option)
        curr_prof = engine.profiles[sim_user]
        user_home_cur = curr_prof["home_currency"]

        st.markdown("#### 2. What do you want to spend?")
        sim_question = st.text_input("Your Question / Expense Description", "Can I afford to buy a new smartphone?")
        
        c_amt1, c_amt2, c_amt3 = st.columns(3)
        with c_amt1:
            sim_amt = st.number_input(f"Amount ({user_home_cur})", min_value=1.0, value=float(min(5000.0, float(curr_prof['current_available_balance'])*0.5)), step=50.0)
        with c_amt2:
            sim_req_date = st.date_input("Purchase Date", date(2025, 6, 1))
        with c_amt3:
            sim_deadline = st.date_input("Desired Completion Deadline", date(2025, 8, 1))

        c_opt1, c_opt2 = st.columns(2)
        with c_opt1:
            sim_category = st.selectbox("Expense Category", list(CATEGORY_ICONS.keys()), format_func=lambda x: get_cat_info(x)[1])
        with c_opt2:
            sim_allow_partial = st.checkbox("Allow 2-Part Payment if needed?", value=True)

        with st.expander("⚙️ Optional: Tweak Current Balance or Emergency Buffer"):
            sim_bal_override = st.number_input(f"Override Current Balance ({user_home_cur})", min_value=0.0, value=float(curr_prof["current_available_balance"]), step=500.0)
            sim_floor_override = st.number_input(f"Override Emergency Buffer ({user_home_cur})", min_value=0.0, value=float(curr_prof["minimum_balance_to_keep"]), step=500.0)

        submitted = st.form_submit_button("🚀 Run 90-Day Safety Simulation", type="primary")

    if submitted:
        if sim_deadline < sim_req_date:
            st.error("Error: Completion deadline cannot be earlier than the purchase date.")
        else:
            with st.spinner("Simulating full 90-day cash flows..."):
                sim_res = engine.evaluate_custom(
                    user_id=sim_user,
                    amount=sim_amt,
                    req_date=sim_req_date,
                    deadline=sim_deadline,
                    category=sim_category,
                    allows_partial=sim_allow_partial,
                    request_text=sim_question,
                    balance_override=sim_bal_override,
                    min_balance_override=sim_floor_override
                )
            
            s_rec = sim_res["recommendation"]
            s_status = s_rec["affordability_status"]
            s_safe = sim_res["safe_amount_today"]
            s_method = s_rec["recommended_payment_method"].replace("_", " ").title()

            st.markdown("---")
            st.markdown("### 🎯 Simulation Result")

            if s_status == "affordable_now":
                st.success(f"### 🟢 YES! Affordable Today\n{s_rec['decision_explanation']}")
            elif s_status == "affordable_with_plan":
                st.info(f"### 🔵 YES! Affordable with Plan ({s_method})\n{s_rec['decision_explanation']}")
            elif s_status == "affordable_later":
                st.warning(f"### 🟡 Wait until {s_rec['earliest_date_for_full_payment']}\n{s_rec['decision_explanation']}")
            else:
                st.error(f"### 🔴 Not Recommended Right Now\n{s_rec['decision_explanation']}")

            res_col1, res_col2, res_col3 = st.columns(3)
            res_col1.metric("Max Safe Today", f"{user_home_cur} {s_safe:,.2f}")
            res_col2.metric("Requested Amount", f"{user_home_cur} {sim_amt:,.2f}")
            res_col3.metric("Emergency Buffer", f"{user_home_cur} {sim_floor_override:,.2f}")

            # Schedule table if available
            if s_rec["payment_plan"] != "none":
                st.markdown("#### 🗓️ Generated Payment Schedule:")
                sched_items = []
                for idx, part in enumerate(s_rec["payment_plan"].split("|"), 1):
                    pd_date, pd_val = part.split(":")
                    sched_items.append({"Payment #": idx, "Date": pd_date, "Amount": f"{user_home_cur} {float(pd_val):,.2f}"})
                st.dataframe(pd.DataFrame(sched_items), hide_index=True)


# ==============================================================================
# MODE 3: CHAT WITH AI FINANCIAL ASSISTANT (CONVERSATIONAL INTERFACE)
# ==============================================================================
elif nav_mode.startswith("💬"):
    st.markdown("## 💬 Chat with your AI Financial Assistant")
    st.caption("Ask questions about your finances, upcoming bills, salary arrival, or affordability!")

    all_uids = sorted(list(engine.profiles.keys()))
    chat_user = st.selectbox("Select Your Profile", all_uids, index=0)
    c_prof = engine.profiles[chat_user]
    c_cur = c_prof["home_currency"]
    c_diag = engine.diagnose(next(r for r in engine.requests if r["user_id"] == chat_user))

    # Suggested Prompts
    st.markdown("**💡 Click a quick question to ask:**")
    q1, q2, q3, q4 = st.columns(4)
    
    prompt_clicked = None
    if q1.button("💰 Max Safe Spending Today?"):
        prompt_clicked = "How much can I safely spend today without breaking my emergency buffer?"
    if q2.button("📅 When is my next salary?"):
        prompt_clicked = "When will my next salary arrive and how much is it?"
    if q3.button("🧾 What are my top bills?"):
        prompt_clicked = "What are my biggest recurring monthly bills?"
    if q4.button("🛡️ What is my tightest cash day?"):
        prompt_clicked = "What day will my bank balance dip to its lowest in the next 90 days?"

    user_chat_input = st.chat_input("Type any financial question here...") or prompt_clicked

    if user_chat_input:
        with st.chat_message("user"):
            st.write(user_chat_input)

        with st.chat_message("assistant"):
            query = user_chat_input.lower()
            
            if "safe" in query or "spend" in query or "max" in query:
                safe_val = c_diag["safe_amount_today"]
                st.write(f"Based on your 90-day cash flow simulation, your **maximum safe spending amount today** is **{c_cur} {safe_val:,.2f}**.")
                st.write(f"Your current bank balance is **{c_cur} {float(c_prof['current_available_balance']):,.2f}**, and we must protect your **{c_cur} {float(c_prof['minimum_balance_to_keep']):,.2f}** emergency buffer alongside upcoming bills.")

            elif "salary" in query or "income" in query or "payday" in query:
                salary_streams = [s for s in c_diag["recurring_streams"] if s["key"][1] == "salary" and s["key"][2] == "credit"]
                if salary_streams:
                    sal = salary_streams[0]
                    st.write(f"Your confirmed regular **salary** is approximately **{c_cur} {sal['amount']:,.2f}**, received every **~{sal['cadence']} days**.")
                else:
                    st.write(f"We verified your income records. Look out for scheduled credits in your cash flow forecast.")

            elif "bills" in query or "recurring" in query or "expenses" in query:
                expenses = [s for s in c_diag["recurring_streams"] if s["key"][2] == "debit"]
                expenses.sort(key=lambda x: x["amount"], reverse=True)
                st.write("Here are your largest regular recurring commitments:")
                for e in expenses[:4]:
                    st.write(f"• **{e['key'][1].replace('_', ' ').title()}**: ~{c_cur} {e['amount']:,.2f} every {e['cadence']} days")

            elif "lowest" in query or "tightest" in query or "dip" in query:
                lowest_b = c_diag["lowest_balance_baseline"]
                floor = float(c_prof["minimum_balance_to_keep"])
                cush = lowest_b - floor
                st.write(f"The lowest your balance is forecasted to dip over the next 90 days is **{c_cur} {lowest_b:,.2f}**.")
                st.write(f"This leaves a safety cushion of **{c_cur} {cush:,.2f}** above your **{c_cur} {floor:,.2f}** emergency reserve floor.")

            else:
                st.write(f"I analyzed your financial profile ({c_prof['home_currency']}):")
                st.write(f"• **Available Balance Today:** {c_cur} {float(c_prof['current_available_balance']):,.2f}")
                st.write(f"• **Emergency Buffer to Protect:** {c_cur} {float(c_prof['minimum_balance_to_keep']):,.2f}")
                st.write(f"• **Safe Today Headroom:** {c_cur} {c_diag['safe_amount_today']:,.2f}")
                st.write("Feel free to ask about your salary, bills, or test an expense in the **Simulator** tab!")


# ==============================================================================
# MODE 4: ALL 250 PREDICTIONS TABLE & CSV EXPORT
# ==============================================================================
elif nav_mode.startswith("🗂️"):
    st.markdown("## 🗂️ Official 250 Predictions Table (`output.csv`)")
    st.caption("Browse, filter, and download the full deterministic benchmark output.")

    out_file_path = CODE_DIR.parent / "output.csv"
    if out_file_path.exists():
        with open(out_file_path, "rb") as f:
            csv_bytes = f.read()
        st.download_button(
            label="⬇️ Download output.csv",
            data=csv_bytes,
            file_name="output.csv",
            mime="text/csv",
            type="primary"
        )

    st.dataframe(all_preds_df[OUTPUT_COLS], width="stretch", height=500)

st.markdown("---")
st.caption("Buy or Wait? AI Financial Agent • HackerRank Orchestrate Challenge")
