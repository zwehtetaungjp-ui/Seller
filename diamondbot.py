import streamlit as st
import requests
import json
from streamlit_option_menu import option_menu

# --- ဘာသာစကား နှင့် ပုံသေနည်းများ ---
LANG = {
    "မြန်မာ": {"title": "💎 MLBB Shop", "id": "ဂိမ်း ID", "pack": "ပမာဏ ရွေးပါ", "pay": "ငွေပေးချေမှု", "btn": "ဝယ်ယူမည်"},
    "English": {"title": "💎 MLBB Shop", "id": "Player ID", "pack": "Select Pack", "pay": "Payment", "btn": "Order Now"}
}

st.set_page_config(page_title="MLBB Shop", layout="centered")
sel_lang = st.sidebar.selectbox("Language", ["မြန်မာ", "English"])
t = LANG[sel_lang]

st.title(t["title"])

# ၁။ Player ID Input
player_id = st.text_input(t["id"], placeholder="12345678 (1234)")

# ၂။ Diamond Selection (Icon Cards Style)
st.subheader(t["pack"])
selected_pack = option_menu(
    menu_title=None,
    options=["86 💎", "172 💎", "257 💎", "706 💎"],
    icons=["gem", "gem", "gem", "gem"],
    menu_icon="cast", default_index=0, orientation="horizontal",
)

# ၃။ Payment Method (Crypto, Yen, MMK)
st.subheader(t["pay"])
pay_method = st.radio("Choose Method:", ["USDT (Crypto)", "JPY (Yen)", "MMK (KPay)"], horizontal=True)

with st.expander("💳 Payment Address (ငွေလွှဲရန်လိပ်စာ)", expanded=True):
    if pay_method == "USDT (Crypto)":
        st.code("TRC20: TXXXXXXXXXXXXXXXXXXXXXXXXX", language="text")
    elif pay_method == "JPY (Yen)":
        st.code("Japan Post: 12345-67890", language="text")
    else:
        st.code("KPay: 09123456789", language="text")

payment_ss = st.file_uploader("Upload Receipt", type=['jpg', 'png'])

if st.button(t["btn"], use_container_width=True, type="primary"):
    # Telegram သို့ ပို့မည့် ကုဒ်များ (ယခင်အတိုင်း)
    st.success("Sent to Admin!")
