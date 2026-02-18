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
        "title": "💎 MLBB Diamond Shop",
        "acc_info": "အကောင့်အချက်အလက်",
        "id": "ဂိမ်း ID", "zone": "Zone ID",
        "select_pack": "Diamond ပမာဏ ရွေးချယ်ပါ",
        "pay_method": "ငွေပေးချေမှုစနစ်",
        "upload": "ငွေလွှဲပြေစာ (Screenshot) တင်ပေးပါ",
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
        "upload": "Upload Payment Receipt",
        "btn": "Order Now",
        "success": "Order Successful!",
        "error": "Please fill all fields!"
    }
}

packs_data = [
    {"name": "86 Diamonds", "mmk": "2,500", "jpy": "150", "usdt": "1.0"},
    {"name": "172 Diamonds", "mmk": "5,000", "jpy": "300", "usdt": "2.0"},
    {"name": "257 Diamonds", "mmk": "7,500", "jpy": "450", "usdt": "3.0"},
    {"name": "706 Diamonds", "mmk": "20,000", "jpy": "1,200", "usdt": "8.0"}
]

# --- ၃။ Page Layout & Styling ---
st.set_page_config(page_title="MLBB Shop", page_icon="💎", layout="centered")

# Custom CSS for bigger look
st.markdown("""
    <style>
    .stButton>button { height: 3em; font-size: 20px !important; font-weight: bold; }
    .stTextInput>div>div>input { font-size: 18px !important; }
    </style>
    """, unsafe_allow_html=True)

sel_lang = st.sidebar.selectbox("Language / ဘာသာစကား", ["မြန်မာ", "English"])
t = LANG[sel_lang]

st.title(t["title"])

# --- ၄။ Player ID & Zone ID (အကွက်ခွဲ) ---
st.subheader(t["acc_info"])
col_id, col_zone = st.columns([3, 1])
with col_id:
    user_id = st.text_input(t["id"], placeholder="12345678")
with col_zone:
    zone_id = st.text_input(t["zone"], placeholder="1234")

# --- ၅။ Currency Selection ---
st.subheader(t["pay_method"])
currency = st.radio("Currency:", ["MMK", "JPY", "USDT"], horizontal=True, label_visibility="collapsed")

# --- ၆။ Diamond Packs (အကွက်ကြီးကြီး + Highlight) ---
st.subheader(t["select_pack"])

# အကွက်ထဲမှာ ပြမယ့် စာသားစီစဉ်ခြင်း
options_list = []
for p in packs_data:
    price = p[currency.lower()]
    options_list.append(f"{p['name']}\n{price} {currency}")

# Grid ပုံစံ Icon Menu
selected_raw = option_menu(
    menu_title=None,
    options=options_list,
    icons=["gem", "gem", "gem", "gem"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "#00d4ff", "font-size": "25px"},
        "nav-link": {
            "font-size": "14px", 
            "text-align": "center", 
            "margin": "10px", 
            "height": "100px", # အကွက်ကို အမြင့်ကြီးပေးထားသည်
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "border": "1px solid #444",
            "border-radius": "15px"
        },
        "nav-link-selected": {
            "background-color": "#023e8a", 
            "color": "white",
            "border": "2px solid #00d4ff"
        }
    }
)

# ရွေးထားတဲ့ Data ကို ခွဲထုတ်ခြင်း
selected_pack_name = selected_raw.split("\n")[0]
selected_price = selected_raw.split("\n")[1]

# --- ၇။ Payment Address Details ---
st.markdown("---")
with st.container(border=True):
    st.markdown(f"### 🏦 Transfer to {currency}")
    if currency == "MMK":
        st.code("KPay/Wave: 09 123 456 789\nName: U Myo Min", language="text")
    elif currency == "JPY":
        st.code("Japan Post: 12345-67890\nName: MYO MIN", language="text")
    else:
        st.code("USDT (TRC20):\nTXXXXXXXXXXXXXXXXXXXXXXXXX", language="text")

payment_ss = st.file_uploader(t["upload"], type=['jpg', 'png', 'jpeg'])

# --- ၈။ Submit Button ---
if st.button(t["btn"], use_container_width=True, type="primary"):
    if user_id and zone_id and payment_ss:
        with st.spinner("Processing..."):
            # Telegram Caption
            caption = (f"📦 *New Order!*\n\n"
                      f"👤 ID: {user_id} ({zone_id})\n"
                      f"💎 Pack: {selected_pack_name}\n"
                      f"💰 Price: {selected_price}\n"
                      f"💳 Method: {currency}")
            
            # Send to Telegram
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            data = {
                'chat_id': ADMIN_CHAT_ID, 
                'caption': caption, 
                'parse_mode': 'Markdown',
                'reply_markup': json.dumps({
                    "inline_keyboard": [[
                        {"text": "✅ Approve", "callback_data": "approve"},
                        {"text": "❌ Reject", "callback_data": "reject"}
                    ]]
                })
            }
            files = {'photo': payment_ss.getvalue()}
            
            res = requests.post(url, files=files, data=data)
            if res.status_code == 200:
                st.success(t["success"])
                st.balloons()
            else:
                st.error("Connection Error! Check Token/ChatID.")
    else:
        st.error(t["error"])
