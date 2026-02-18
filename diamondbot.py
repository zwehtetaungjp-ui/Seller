import streamlit as st
import requests
import json

# --- ၁။ CONFIGURATION ---
BOT_TOKEN = "မင်းရဲ့_BOT_TOKEN_ဒီမှာထည့်"
ADMIN_CHAT_ID = "မင်းရဲ့_CHAT_ID_ဒီမှာထည့်"

# --- ၂။ ဘာသာစကား နှင့် ဒေတာများ ---
LANG = {
    "မြန်မာ": {
        "title": "💎 MLBB Diamond ဆိုင်",
        "acc_info": "အကောင့်အချက်အလက်",
        "id": "ဂိမ်း ID", "zone": "Zone ID",
        "select_pack": "Diamond ပမာဏ ရွေးချယ်ပါ",
        "pay_method": "ငွေပေးချေမှုစနစ်",
        "upload": "ငွေလွှဲပြေစာ တင်ပေးပါ",
        "btn": "အခုပဲ ဝယ်ယူမည်",
        "success": "Order တင်ခြင်း အောင်မြင်ပါသည်!",
        "error": "အချက်အလက် ပြည့်စုံအောင် ဖြည့်ပါ!"
    },
    "English": {
        "title": "💎 MLBB Diamond Shop",
        "acc_info": "Account Information",
        "id": "Player ID", "zone": "Zone ID",
        "select_pack": "Select Diamond Pack",
        "pay_method": "Payment Method",
        "upload": "Upload Receipt",
        "btn": "Order Now",
        "success": "Order Successful!",
        "error": "Please fill all fields!"
    }
}

packs_data = [
    {"name": "86 Diamonds", "big-icon": "💎", "mmk": 2500, "jpy": 150, "usdt": 1.0},
    {"name": "172 Diamonds", "big-icon": "🎁", "mmk": 5000, "jpy": 300, "usdt": 2.0},
    {"name": "257 Diamonds", "big-icon": "🏆", "mmk": 7500, "jpy": 450, "usdt": 3.0},
    {"name": "706 Diamonds", "big-icon": "👑", "mmk": 20000, "jpy": 1200, "usdt": 8.0}
]

# --- ၃။ Page Setup & Custom CSS ---
st.set_page_config(page_title="MLBB Shop", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    div.stButton > button {
        width: 250px;
        height: 150px;
        border-radius: 15px;
        border: 1px solid #ddd;
        font-size: 18px !important;
        white-space: pre-line;
    }
    div.stButton > button:active, div.stButton > button:focus {
        border: 3px solid #007bff !important;
        background-color: #e7f3ff !important;
    }
    </style>
""", unsafe_allow_html=True)

if 'selected_pack' not in st.session_state:
    st.session_state.selected_pack = None
if 'selected_price' not in st.session_state:
    st.session_state.selected_price = None

sel_lang = st.sidebar.selectbox("Language / ဘာသာစကား", ["မြန်မာ", "English"])
t = LANG[sel_lang]

st.title(t["title"])

# --- ၄။ Account Info ---
st.subheader(t["acc_info"])
col_id, col_zone = st.columns([3, 1])
with col_id:
    user_id = st.text_input(t["id"], placeholder="12345678")
with col_zone:
    zone_id = st.text_input(t["zone"], placeholder="1234")

# --- ၅။ Currency Selection ---
st.subheader(t["pay_method"])
currency = st.radio("Currency:", ["MMK", "JPY", "USDT"], horizontal=True, label_visibility="collapsed")

# --- ၆။ Diamond Card Grid (တစ်တန်း ၂ ခု) ---
st.subheader(t["select_pack"])
cols = st.columns(2)

for i, pack in enumerate(packs_data):
    price_val = pack[currency.lower()]
    price_display = f"{price_val} {currency}"
    label = f"{pack['big-icon']}\n\n{pack['name']}\n{price_display}"
    
    with cols[i % 2]:
        if st.button(label, key=f"pack_{i}"):
            st.session_state.selected_pack = pack['name']
            st.session_state.selected_price = price_display

if st.session_state.selected_pack:
    st.success(f"Selected: *{st.session_state.selected_pack}* ({st.session_state.selected_price})")

# --- ၇။ Payment & Upload ---
st.markdown("---")
with st.container(border=True):
    st.markdown(f"*Transfer to {currency} Address:*")
    if currency == "MMK": st.code("KPay: 09 123 456 789")
    elif currency == "JPY": st.code("Japan Post: 12345-67890")
    else: st.code("USDT (TRC20): TXXXXXXXXXXXXXXXX")

payment_ss = st.file_uploader(t["upload"], type=['jpg', 'png', 'jpeg'])

# --- ၈။ Final Submit ---
if st.button(t["btn"], use_container_width=True, type="primary"):
    if user_id and zone_id and payment_ss and st.session_state.selected_pack:
        with st.spinner("Processing..."):
            caption = (f"📦 New Order!\n\n"
                      f"👤 ID: {user_id} ({zone_id})\n"
                      f"💎 Pack: {st.session_state.selected_pack}\n"
                      f"💰 Price: {st.session_state.selected_price}\n"
                      f"💳 Method: {currency}")
            
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            reply_markup = {"inline_keyboard": [[
                {"text": "✅ Approve", "callback_data": "approve"},
                {"text": "❌ Reject", "callback_data": "reject"}
            ]]}
            
            data = {'chat_id': ADMIN_CHAT_ID, 'caption': caption, 'reply_markup': json.dumps(reply_markup)}
            res = requests.post(url, files={'photo': payment_ss.getvalue()}, data=data)
            
            if res.status_code == 200:
                st.success(t["success"])
                st.balloons()
            else:
                st.error("Telegram Error! Check Token/ID.")
    else:
        st.error(t["error"])





