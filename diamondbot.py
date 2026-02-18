import streamlit as st
import requests

# --- CONFIGURATION ---
BOT_TOKEN = "မင်းရဲ့_BOT_TOKEN_ဒီမှာထည့်ပါ"
ADMIN_CHAT_ID = "မင်းရဲ့_CHAT_ID_ဒီမှာထည့်ပါ"

def send_to_telegram(caption, image_file):
    # Telegram API သုံးပြီး ပုံနဲ့စာကို လှမ်းပို့တဲ့ Function
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {'photo': image_file.getvalue()}
    data = {'chat_id': ADMIN_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}
    response = requests.post(url, files=files, data=data)
    return response.json()

# --- UI DESIGN ---
st.set_page_config(page_title="MLBB Diamond Shop", layout="centered")

st.title("💎 MLBB Top-up Shop")
st.info("အချက်အလက်များကို မှန်ကန်စွာ ဖြည့်သွင်းပေးပါ")

# Input Fields
player_id = st.text_input("Player ID (Zone ID)", placeholder="ဥပမာ - 12345678 (1234)")
diamond_plan = st.selectbox("Diamond ပမာဏ ရွေးချယ်ပါ", [
    "86 Diamonds - 2500 Ks",
    "172 Diamonds - 5000 Ks",
    "257 Diamonds - 7500 Ks"
])
payment_ss = st.file_uploader("ငွေလွှဲပြေစာ (Screenshot) တင်ပေးပါ", type=['jpg', 'png', 'jpeg'])

if st.button("အခုပဲ ဝယ်ယူမည်"):
    if player_id and payment_ss:
        with st.spinner('Order တင်နေပါသည်...'):
            # Admin ဆီ ပို့မယ့် စာသားပုံစံ
            message_text = f"📦 *Order အသစ်တက်လာပါပြီ!*\n\n" \
                           f"👤 ID: `{player_id}`\n" \
                           f"💎 Plan: {diamond_plan}\n" \
                           f"⏳ Status: Pending"
            
            result = send_to_telegram(message_text, payment_ss)
            
            if result.get("ok"):
                st.success("Order တင်ခြင်း အောင်မြင်ပါသည်။ ခဏအတွင်း ဖြည့်သွင်းပေးပါမည်။")
                st.balloons()
            else:
                st.error("Error: Telegram ဆီသို့ အချက်အလက် ပို့၍မရပါ။")
    else:
        st.warning("ID နှင့် Screenshot ကို ပြည့်စုံအောင် ထည့်ပေးပါ။")