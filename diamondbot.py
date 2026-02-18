import streamlit as st
import requests
import json
from streamlit_option_menu import option_menu

# --- ၁။ CONFIGURATION (မင်းရဲ့ အချက်အလက်များ ပြောင်းရန်) ---
BOT_TOKEN = "7823456789:AAH-xXyYzZ..." # @BotFather ကရတဲ့ Token ထည့်ပါ
ADMIN_CHAT_ID = "123456789" # @userinfobot ကရတဲ့ ID ထည့်ပါ

# --- ၂။ ဘာသာစကား Dictionary ---
LANG = {
    "မြန်မာ": {
        "title": "💎 MLBB Diamond ဆိုင်",
        "player_id": "ဂိမ်း ID (Zone ID)",
        "select_pack": "Diamond ပမာဏ ရွေးချယ်ပါ",
        "pay_method": "ငွေပေးချေမှု စနစ်ရွေးချယ်ပါ",
        "upload_ss": "ငွေလွှဲပြေစာ (Screenshot) တင်ပေးပါ",
        "order_btn": "အခုပဲ ဝယ်ယူမည်",
        "pay_info": "ငွေလွှဲပေးရမည့် လိပ်စာ -",
        "success": "Order တင်ခြင်း အောင်မြင်ပါသည်။",
        "error": "အချက်အလက်များ ပြည့်စုံအောင် ဖြည့်ပေးပါ!"
    },
    "English": {
        "title": "💎 MLBB Diamond Shop",
        "player_id": "Player ID (Zone ID)",
        "select_pack": "Select Diamond Pack",
        "pay_method": "Payment Method",
        "upload_ss": "Upload Payment Screenshot",
        "order_btn": "Order Now",
        "pay_info": "Transfer Address -",
        "success": "Order submitted successfully!",
        "error": "Please fill all fields!"
    }
}

# --- ၃။ Page Setup & UI ---
st.set_page_config(page_title="MLBB Shop", page_icon="💎", layout="centered")

# ဘာသာစကား ရွေးချယ်မှု (Sidebar)
sel_lang = st.sidebar.selectbox("Language / ဘာသာစကား", ["မြန်မာ", "English"])
t = LANG[sel_lang]

st.title(t["title"])

# Player ID ရိုက်ရန်
player_id = st.text_input(t["player_id"], placeholder="e.g. 12345678 (1234)")

# Diamond Packs (Icon Cards Design)
st.subheader(t["select_pack"])
diamond_packs = {
    "86 Diamonds": {"icon": "gem", "price": "2,500 MMK / 150 JPY / 1.0 USDT"},
    "172 Diamonds": {"icon": "boxes", "price": "5,000 MMK / 300 JPY / 2.0 USDT"},
    "257 Diamonds": {"icon": "award", "price": "7,500 MMK / 450 JPY / 3.0 USDT"},
    "706 Diamonds": {"icon": "stars", "price": "20,000 MMK / 1,200 JPY / 8.0 USDT"}
}

selected_pack = option_menu(
    menu_title=None,
    options=list(diamond_packs.keys()),
    icons=[d["icon"] for d in diamond_packs.values()],
    orientation="horizontal",
    styles={
        "nav-link-selected": {"background-color": "#023e8a"},
        "nav-link": {"font-size": "13px"}
    }
)
st.info(f"💰 {t['pay_info']} {diamond_packs[selected_pack]['price']}")

# Payment Selection & Address
pay_method = st.selectbox(t["pay_method"], ["MMK (KPay/Wave)", "JPY (Yen/Bank)", "Crypto (USDT)"])

with st.container(border=True):
    if pay_method == "MMK (KPay/Wave)":
        st.write("📱 *KPay/Wave:* 09 123 456 789 (U Myo Min)")
    elif pay_method == "JPY (Yen/Bank)":
        st.write("🏦 *Japan Post Bank:* 12345678 (MYO MIN)")
    else:
        st.write("🌐 *USDT (TRC20):* TXXXXXXXXXXXXXXXXXXXXXXXXX")

payment_ss = st.file_uploader(t["upload_ss"], type=['jpg', 'png', 'jpeg'])

# Order Button Logic
if st.button(t["order_btn"], use_container_width=True, type="primary"):
    if player_id and payment_ss:
        with st.spinner("Processing..."):
            caption = f"📦 *New Order!*\n\n👤 ID: `{player_id}`\n💎 Pack: {selected_pack}\n💰 Method: {pay_method}"
            
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            # Telegram Buttons
            reply_markup = {"inline_keyboard": [[
                {"text": "✅ Approve", "callback_data": f"approve_{player_id}"},
                {"text": "❌ Reject", "callback_data": "reject"}
            ]]}
            
            files = {'photo': payment_ss.getvalue()}
            data = {'chat_id': ADMIN_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown', 'reply_markup': json.dumps(reply_markup)}
            
            res = requests.post(url, files=files, data=data)
            if res.status_code == 200:
                st.success(t["success"])
                st.balloons()
            else:
                st.error("Connection Error!")
    else:
        st.error(t["error"])
