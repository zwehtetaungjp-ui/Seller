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
    {"name": "86 Diamonds", "img": "💎", "mmk": 2500, "jpy": 150, "usdt": 1.0},
    {"name": "172 Diamonds", "img": "🎁", "mmk": 5000, "jpy": 300, "usdt": 2.0},
    {"name": "257 Diamonds", "img": "🏆", "mmk": 7500, "jpy": 450, "usdt": 3.0},
    {"name": "706 Diamonds", "img": "👑", "mmk": 20000, "jpy": 1200, "usdt": 8.0}
]

# --- ၃။ Page Layout ---
st.set_page_config(page_title="MLBB Shop", page_icon="💎")
sel_lang = st.sidebar.selectbox("Language / ဘာသာစကား", ["မြန်မာ", "English"])
t = LANG[sel_lang]

st.title(t["title"])

# ID & Zone ID အကွက်ခွဲခြင်း
st.subheader(t["acc_info"])
col_id, col_zone = st.columns([3, 1])
with col_id:
    user_id = st.text_input(t["id"], placeholder="12345678")
with col_zone:
    zone_id = st.text_input(t["zone"], placeholder="1234")

# ငွေကြေးရွေးချယ်မှု (ဈေးနှုန်းတန်းပြောင်းရန်)
st.subheader(t["pay_method"])
currency = st.radio("Currency:", ["MMK", "JPY", "USDT"], horizontal=True, label_visibility="collapsed")

# Diamond Packs (Grid UI with Icons)
st.subheader(t["select_pack"])
cols = st.columns(2)
if 'selected_pack' not in st.session_state:
    st.session_state.selected_pack = packs_data[0]["name"]

for i, pack in enumerate(packs_data):
    # Currency အလိုက် ဈေးနှုန်းတွက်ချက်ခြင်း
    price = pack[currency.lower()]
    price_str = f"{price} {currency}"
    
    with cols[i % 2]:
        with st.container(border=True):
            st.markdown(f"<h1 style='text-align: center;'>{pack['img']}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'><b>{pack['name']}</b><br>{price_str}</p>", unsafe_allow_html=True)
            if st.button(f"Choose {pack['name']}", key=f"btn_{i}", use_container_width=True):
                st.session_state.selected_pack = pack['name']
                st.session_state.selected_price = price_str

# ရွေးချယ်ထားသော အထုပ်အား ပြသခြင်း
if 'selected_pack' in st.session_state:
    st.info(f"Selected: {st.session_state.selected_pack} ({st.session_state.get('selected_price', '---')})")

# Payment Address Details
with st.expander("🏦 View Payment Addresses", expanded=True):
    if currency == "MMK":
        st.code("KPay: 09 123 456 789 (U Myo Min)", language="text")
    elif currency == "JPY":
        st.code("Japan Post: 12345-67890 (MYO MIN)", language="text")
    else:
        st.code("USDT (TRC20): TXXXXXXXXXXXXXXXXXXXXX", language="text")

payment_ss = st.file_uploader(t["upload"], type=['jpg', 'png', 'jpeg'])

# --- ၄။ ပို့ဆောင်ခြင်း ---
if st.button(t["btn"], use_container_width=True, type="primary"):
    if user_id and zone_id and payment_ss:
        with st.spinner("Sending..."):
            caption = (f"📦 *New Order!*\n\n"
                      f"👤 ID: {user_id} ({zone_id})\n"
                      f"💎 Pack: {st.session_state.selected_pack}\n"
                      f"💰 Price: {st.session_state.selected_price}\n"
                      f"💳 Method: {currency}")
            
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
                st.error("Telegram Error!")
    else:
        st.error(t["error"])
