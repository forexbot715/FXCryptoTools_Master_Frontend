import streamlit as st
from streamlit_ace import st_ace
import requests
import time
import re

st.set_page_config(page_title="FXCryptoTools Terminal", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; }
    .footer { text-align: center; color: #888; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 FXCryptoTools MQL Lab")
st.sidebar.title("💎 FXCryptoTools")
st.sidebar.info("Professional Code Injection Hub")

# --- INSTRUCTIONS ---
with st.expander("📖 User Instructions (English)", expanded=False):
    st.markdown("""
    1. **Download Bridge:** Get the `bridge.exe` from the link below and run it.
    2. **Syntax Check:** Use the 'Check Syntax' button anytime to find code errors (No ID required).
    3. **Live Injection:** Once code is ready, enter your **Bridge ID** and click 'Apply to MT4/MT5'.
    """)

# --- CODE AREA ---
st.subheader("📝 MQL Editor")

# This provides the White background and Syntax Highlighting (C++ style for MQL)
mql_code = st_ace(
    placeholder="// Write your MQL4/5 code here...",
    language="c_cpp",
    theme="chrome",  # This gives the white background
    keybinding="vscode",
    font_size=14,
    height=450,
    show_gutter=True,
    value="""// Built by FXCryptoTools
#property indicator_chart_window

int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
   return(rates_total);
}"""
)

# --- BUTTONS ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Check Syntax (Fast Test)"):
        # This function works WITHOUT a token
        st.info("Analyzing syntax structure...")
        errors = []
        if ";" not in mql_code and "{" in mql_code:
            errors.append("Line missing semicolon (;)")
        if mql_code.count("{") != mql_code.count("}"):
            errors.append("Mismatched curly brackets { }")
        
        if not errors:
            st.success("✅ Basic Syntax looks good! (Structural Test Passed)")
        else:
            for err in errors:
                st.error(f"❌ {err}")

with col2:
    uid = st.text_input("Bridge ID:", placeholder="Enter ID from bridge.exe")
    version = st.selectbox("Terminal Version:", ["MT4", "MT5"])
    if st.button("⚡ Apply to MT4/MT5 Terminal"):
        if not uid:
            st.warning("Please enter your Bridge ID to inject code.")
        else:
            with st.spinner("Injecting to Remote Terminal..."):
                try:
                    relay_url = "https://your-relay-app.render.com/send_to_bridge"
                    requests.post(relay_url, json={"uid": uid, "code": mql_code, "version": version})
                    st.success(f"Sent! Check your terminal for ID: {uid}")
                except:
                    st.error("Relay Server connection failed.")

st.markdown("---")
st.markdown('<div class="footer">Powered by FXCryptoTools | Precision Trading Solutions</div>', unsafe_allow_html=True)