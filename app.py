import streamlit as st
import requests
import time

# --- CONFIGURATION ---
RELAY_URL = "https://fxcryptotools-master.onrender.com"

st.set_page_config(page_title="FXCryptoTools Remote Terminal", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { font-family: 'Courier New', monospace; background-color: #161a23; color: #00ff00; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    .check-btn>button { background-color: #2196F3; color: white; }
    .apply-btn>button { background-color: #4CAF50; color: white; }
    .footer { text-align: center; color: gray; padding: 20px; margin-top: 50px; border-top: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 FXCryptoTools Remote Lab")
st.caption("Professional MQL4/5 Development & Injection")

# --- INSTRUCTIONS ---
with st.expander("📖 Setup Instructions", expanded=True):
    c1, c2, c3 = st.columns(3)
    c1.info("**1. Download Bridge**\nRun 'FX_Bridge.exe' on your PC to link your MT4/MT5.")
    c2.info("**2. Get Your ID**\nCopy the 8-digit Unique ID from the Bridge window.")
    c3.info("**3. Deploy**\nEnter ID below, paste code, and click Apply.")

st.markdown("---")

# --- CODE AREA (TOP - FULL WIDTH) ---
st.subheader("📝 MQL Code Editor")
mql_code = st.text_area("Paste your MQL4 or MQL5 Code here:", height=500, placeholder="// Your indicator logic here...")

# --- SETTINGS & BUTTONS (BELOW CODE) ---
st.markdown("---")
col_cfg, col_btns = st.columns([1, 1])

with col_cfg:
    st.subheader("⚙️ Connection Settings")
    uid = st.text_input("Enter Bridge ID:", placeholder="Enter ID from Bridge.exe (e.g. A1B2C3D4)")
    version = st.selectbox("Select Terminal Version:", ["MT4", "MT5"])

with col_btns:
    st.subheader("⚡ Actions")
    # Action Buttons
    st.markdown('<div class="check-btn">', unsafe_allow_html=True)
    check_code = st.button("🔍 Check Code Syntax (Compiler Test)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="apply-btn">', unsafe_allow_html=True)
    apply_code = st.button("🚀 Apply Code to Terminal")
    st.markdown('</div>', unsafe_allow_html=True)

# --- RESULTS AREA ---
if check_code or apply_code:
    if not uid:
        st.warning("⚠️ Please enter your Bridge ID first.")
    elif not mql_code:
        st.warning("⚠️ Code editor is empty.")
    else:
        with st.spinner("Processing request..."):
            try:
                # Send code to Relay
                payload = {"uid": uid, "code": mql_code, "version": version}
                requests.post(f"{RELAY_URL}/send_to_bridge", json=payload)
                
                # Wait for response
                status_box = st.empty()
                status_box.info("⌛ Communicating with your PC... Please wait.")
                
                # Polling for 10 seconds
                for i in range(10):
                    time.sleep(1.5)
                    log_resp = requests.get(f"{RELAY_URL}/poll/{uid}").json()
                    logs = log_resp.get("logs", "")
                    
                    if logs and "Waiting" not in logs:
                        if "0 errors" in logs.lower():
                            status_box.success("✅ SUCCESS: Compiled successfully with no errors.")
                            if apply_code: st.balloons()
                        else:
                            status_box.error("❌ COMPILER ERROR:")
                            st.code(logs)
                        break
                    if i == 9:
                        status_box.warning("🕒 Timeout: Bridge did not respond. Is your EXE running?")
            except Exception as e:
                st.error(f"Connection Error: {e}")

st.markdown('<div class="footer">Made by FXCryptoTools | Professional Algorithmic Trading Suite</div>', unsafe_allow_html=True)