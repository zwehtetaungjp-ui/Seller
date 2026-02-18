import streamlit as st
import requests
import json

# --- Configuration ---
BOT_TOKEN = "မင်းရဲ့_BOT_TOKEN"
ADMIN_CHAT_ID = "မင်းရဲ့_CHAT_ID"

# --- Language Dictionary ---
LANG = {
    "English": {
        "title": "💎 MLBB Diamond Shop",
        "lang_select": "Choose Language",
        "player_id": "Player ID (Zone ID)",
        "select_pack": "Select Diamond Pack",
        "pay_method": "Select Payment Method",
        "upload_ss": "Upload Payment Screenshot",
        "order_btn": "Order Now",
        "pay_info": "Please transfer to the following address:",
        "success": "Order submitted successfully!",
        "error": "Please fill all fields."
    },
    "မြန်မာ": {
        "title": "💎 MLBB Diamond ဆိုင်",
        "lang_select": "ဘာသာစကား ရွေးချယ်ပါ",
        "player_id": "ဂိမ်း ID (Zone ID)",
        "select_pack": "Diamond ပမာဏ ရွေးချယ်ပါ",
        "pay_method": "ငွေပေးချေမှု စနစ်ရွေးချယ်ပါ",
        "upload_ss": "ငွေလွှဲပြေစာ (Screenshot) တင်ပေးပါ",
        "order_btn": "အခုပဲ ဝယ်ယူမည်",
        "pay_info": "အောက်ပါလိပ်စာသို့ ငွေလွှဲပေးပါ -",
        "success": "Order တင်ခြင်း အောင်မြင်ပါသည်။",
        "error": "အချက်အလက်များ ပြည့်စုံအောင် ဖြည့်ပေးပါ။"
    }
}

# --- Page Setup ---
st.set_page_config(page_title="MLBB Shop", page_icon="💎")

# Language Selection
selected_lang = st.sidebar.selectbox("Language", ["မြန်မာ", "English"])
t = LANG[selected_lang]

st.title(t["title"])

# --- User Inputs ---
player_id = st.text_input(t["player_id"], placeholder="e.g. 12345678 (1234)")

# Diamond Selection with Icons (using Markdown for better visual)
st.subheader(t["select_pack"])
packs = {
    "🔹 86 Diamonds": "2,500 MMK / 150 JPY / 1.0 USDT",
    "📦 172 Diamonds": "5,000 MMK / 300 JPY / 2.0 USDT",
    "💎 257 Diamonds": "7,500 MMK / 450 JPY / 3.0 USDT",
    "🔥 706 Diamonds": "20,000 MMK / 1,200 JPY / 8.0 USDT"
}
selected_pack = st.radio("Packs:", list(packs.keys()), label_visibility="collapsed")
st.info(f"Price: {packs[selected_pack]}")

# Payment Method logic
st.subheader(t["pay_method"])
pay_method = st.selectbox("", ["MMK (KPay/Wave)", "JPY (Yen/Bank)", "Crypto (USDT)"], label_visibility="collapsed")

# Dynamic Payment Address based on method
st.warning(t["pay_info"])
if pay_method == "MMK (KPay/Wave)":
    st.code("09 123 456 789 (U Myo Min)", language="text")
elif pay_method == "JPY (Yen/Bank)":
    st.code("Bank: Japan Post Bank\nAcc: 12345678\nName: MYO MIN", language="text")
else:
    st.code("Network: TRC20\nAddress: TXXXXXXXXXXXXXXXXXXXXXXXXX", language="text")

payment_ss = st.file_uploader(t["upload_ss"], type=['jpg', 'png', 'jpeg'])

# --- Order Logic ---
if st.button(t["order_btn"], use_container_width=True):
    if player_id and payment_ss:
        with st.spinner("Processing..."):
            caption = f"📦 *New Order! ({selected_lang})*\n\n" \
                      f"👤 ID: `{player_id}`\n" \
                      f"💎 Pack: {selected_pack}\n" \
                      f"💰 Method: {pay_method}\n" \
                      f"⏳ Status: Pending"
            
            # Send to Telegram
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            reply_markup = {"inline_keyboard": [[
                {"text": "✅ Approve", "callback_data": "approve"},
                {"text": "❌ Reject", "callback_data": "reject"}
            ]]}
            files = {'photo': payment_ss.getvalue()}
            data = {'chat_id': ADMIN_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown', 'reply_markup': json.dumps(reply_markup)}
            
            res = requests.post(url, files=files, data=data)
            if res.status_code == 200:
                st.success(t["success"])
                st.balloons()
            else:
                st.error("Telegram Connection Error.")
    else:
        st.error(t["error"])
