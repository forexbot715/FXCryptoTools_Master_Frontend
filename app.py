import streamlit as st
import requests
import time

# --- CONFIGURATION ---
RELAY_URL = "https://fxcryptotools-master.onrender.com"

st.set_page_config(page_title="FXCryptoTools Remote Terminal", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #4CAF50; color: white; }
    .footer { position: fixed; bottom: 0; width: 100%; text-align: center; color: gray; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 FXCryptoTools Remote Lab")
st.caption("Professional MQL4/5 Live Code Injection")

# Instructions Section
with st.expander("📖 Setup Instructions (English)", expanded=True):
    c1, c2, c3 = st.columns(3)
    c1.info("**Step 1: Download**\nDownload the 'FX_Bridge.exe' and run it on your Windows PC.")
    c2.info("**Step 2: Connect**\nCopy the 8-digit Unique ID from the Bridge window and paste it below.")
    c3.info("**Step 3: Deploy**\nPaste your MQL code, select your terminal version, and click 'Apply'.")

st.markdown("---")

col_editor, col_config = st.columns([1.5, 1])

with col_editor:
    st.subheader("📝 MQL Code Editor")
    mql_code = st.text_area("Paste your MQL4 or MQL5 Code here:", height=450, placeholder="// Your indicator logic here...")

with col_config:
    st.subheader("⚙️ Connection Settings")
    uid = st.text_input("Enter Bridge ID:", placeholder="Enter the ID from your Bridge.exe")
    version = st.selectbox("Select Terminal Version:", ["MT4", "MT5"])
    
    if st.button("⚡ Apply Code to Terminal"):
        if not uid or not mql_code:
            st.warning("⚠️ Please provide both Bridge ID and MQL Code.")
        else:
            with st.spinner("Injecting code to remote PC..."):
                # Send code to Relay
                try:
                    payload = {"uid": uid, "code": mql_code, "version": version}
                    requests.post(f"{RELAY_URL}/send_to_bridge", json=payload)
                    
                    st.info("⌛ Code sent. Waiting for compilation results...")
                    time.sleep(6) # Wait for bridge to process
                    
                    # Check for logs
                    log_resp = requests.get(f"{RELAY_URL}/poll/{uid}").json()
                    logs = log_resp.get("logs", "Waiting for bridge feedback...")
                    
                    if "0 errors" in logs.lower():
                        st.success("✅ SUCCESS: Indicator compiled and applied to your chart!")
                    else:
                        st.error("❌ COMPILATION ERRORS:")
                        st.code(logs)
                except Exception as e:
                    st.error(f"Connection Error: {e}")

st.markdown('<div class="footer">Made by FXCryptoTools | Professional Algorithmic Trading Suite</div>', unsafe_allow_html=True)