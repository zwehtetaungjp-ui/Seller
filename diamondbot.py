import streamlit as st
import requests
import json
from streamlit_option_menu import option_menu

# --- ၁။ CONFIGURATION ---
BOT_TOKEN = "မင်းရဲ့_BOT_TOKEN_ဒီမှာထည့်"
ADMIN_CHAT_ID = "မင်းရဲ့_CHAT_ID_ဒီမှာထည့်"

# --- ၂။ ဘာသာစကား နှင့် ဒေတာများ ---
LANG = {
    "မြန်မာ": {
        "title": "💎 MLBB Diamond ဆိုင်",
        "acc_info": "အကောင့်အချက်အလက်",
        "id": "ဂိမ်း ID", "zone": "Zone ID",
        "select_pack": "Diamond ပမာဏ ရွေးချယ်ပါ (အကွက်ကိုနှိပ်ပါ)",
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
        "select_pack": "Select Diamond Pack (Click a card)",
        "pay_method": "Payment Method",
        "upload": "Upload Receipt",
        "btn": "Order Now",
        "success": "Order Successful!",
        "error": "Please fill all fields!"
    }
}

packs_data = [
    {"name": "86 Diamonds", "mmk": 2500, "jpy": 150, "usdt": 1.0},
    {"name": "172 Diamonds", "mmk": 5000, "jpy": 300, "usdt": 2.0},
    {"name": "257 Diamonds", "mmk": 7500, "jpy": 450, "usdt": 3.0},
    {"name": "706 Diamonds", "mmk": 20000, "jpy": 1200, "usdt": 8.0}
]

st.set_page_config(page_title="MLBB Shop", page_icon="💎", layout="centered")
sel_lang = st.sidebar.selectbox("Language / ဘာသာစကား", ["မြန်မာ", "English"])
t = LANG[sel_lang]

st.title(t["title"])

# ID & Zone ID
st.subheader(t["acc_info"])
col_id, col_zone = st.columns([3, 1])
with col_id:
    user_id = st.text_input(t["id"], placeholder="12345678")
with col_zone:
    zone_id = st.text_input(t["zone"], placeholder="1234")

# Currency Selection
st.subheader(t["pay_method"])
currency = st.radio("Currency:", ["MMK", "JPY", "USDT"], horizontal=True, label_visibility="collapsed")

# --- Diamond Packs Selection (Active State Design) ---
st.subheader(t["select_pack"])
pack_options = [f"{p['name']}\n({p[currency.lower()]} {currency})" for p in packs_data]

selected_raw = option_menu(
    menu_title=None,
    options=pack_options,
    icons=["gem", "gem", "gem", "gem"],
    orientation="horizontal",
    styles={
        "icon": {"color": "#00d4ff", "font-size": "20px"},
        "nav-link": {"font-size": "11px", "text-align": "center", "border": "0.5px solid #555"},
        "nav-link-selected": {"background-color": "#023e8a", "color": "white"}
    }
)
selected_pack_name = selected_raw.split("\n")[0]
selected_price = selected_raw.split("\n")[1]

# Payment Address
with st.container(border=True):
    st.markdown(f"*🏦 Transfer to {currency} Address:*")
    if currency == "MMK": st.code("KPay: 09 123 456 789")
    elif currency == "JPY": st.code("Japan Post: 12345-67890")
    else: st.code("USDT (TRC20): TXXXXXXX...")

payment_ss = st.file_uploader(t["upload"], type=['jpg', 'png', 'jpeg'])

# Send Button
if st.button(t["btn"], use_container_width=True, type="primary"):
    if user_id and zone_id and payment_ss:
        with st.spinner("Processing..."):
            caption = (f"📦 *New Order!*\n\n👤 ID: {user_id} ({zone_id})\n"
                      f"💎 Pack: {selected_pack_name}\n💰 Price: {selected_price}")
            
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            data = {'chat_id': ADMIN_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown', 'reply_markup': json.dumps({"inline_keyboard": [[{"text": "✅ Approve", "callback_data": "approve"},{"text": "❌ Reject", "callback_data": "reject"}]]})}
            res = requests.post(url, files={'photo': payment_ss.getvalue()}, data=data)
            
            if res.status_code == 200:
                st.success(t["success"])
                st.balloons()
