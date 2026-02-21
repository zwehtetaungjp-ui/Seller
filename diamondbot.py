import streamlit as st
import requests
import json
import time

# --- ၁။ CONFIGURATION ---
BOT_TOKEN = "8403531874:AAGZjRK_4xPNZ5igmHRmu5NIuLf8rS1sb-g"
ADMIN_CHAT_ID = "6826543956"

# --- ၂။ ဘာသာစကား နှင့် ဒေတာများ ---
LANG = {
    "မြန်မာ": {
        "title": "💎 MLBB Diamond ဆိုင်",
        "acc_info": "အကောင့်အချက်အလက်",
        "id": "ဂိမ်း ID", "zone": "Zone ID",
        "select_pack": "ပစ္စည်းအမျိုးအစား ရွေးချယ်ပါ",
        "pay_method": "ငွေပေးချေမှုစနစ်",
        "upload": "ငွေလွှဲပြေစာ တင်ပေးပါ",
        "btn": "အခုပဲ ဝယ်ယူမည်",
        "processing": "Order တင်နေပါပြီ... ခေတ္တစောင့်ပေးပါ (Admin စစ်ဆေးနေသည်)",
        "success": "Order တင်ခြင်း အောင်မြင်ပါသည်!",
        "error": "အချက်အလက် ပြည့်စုံအောင် ဖြည့်ပါ!",
        "curr_label": "ငွေကြေးရွေးချယ်ရန်"
    },
    "English": {
        "title": "💎 MLBB Diamond Shop",
        "acc_info": "Account Information",
        "id": "Player ID", "zone": "Zone ID",
        "select_pack": "Select Item/Pack",
        "pay_method": "Payment Method",
        "upload": "Upload Receipt",
        "btn": "Order Now",
        "processing": "Processing... Please wait for Admin Approval",
        "success": "Order Successful!",
        "error": "Please fill all fields!",
        "curr_label": "Select Currency"
    },
    "日本語": {
        "title": "💎 MLBB ダイヤショップ",
        "acc_info": "アカウント情報",
        "id": "プレイヤーID", "zone": "ゾーンID",
        "select_pack": "パックを選択してください",
        "pay_method": "支払い方法",
        "upload": "振込明細書をアップロード",
        "btn": "今すぐ購入",
        "processing": "注文を処理中... 管理者の承認を待っています",
        "success": "注文が完了しました！",
        "error": "すべての項目を入力してください！",
        "curr_label": "通貨を選択"
    }
}

packs_data = [
    {"name": "Weekly Diamond Pass", "icon": "🎟️", "mmk": 6100, "jpy": 270, "usdt": 1.8},
    {"name": "Twilight Pass", "icon": "🌟", "mmk": 35100, "jpy": 1300, "usdt": 8},
    {"name": "86 Diamonds", "icon": "💎", "mmk": 5500, "jpy": 216, "usdt": 1.72},
    {"name": "172 Diamonds", "icon": "🎁", "mmk": 10500, "jpy": 432, "usdt": 3.44 },
    {"name": "257 Diamonds", "icon": "📦", "mmk": 15000, "jpy": 623, "usdt": 5.14},
    {"name": "706 Diamonds", "icon": "🏆", "mmk": 39000, "jpy": 1680, "usdt": 14.12}
]

# --- ၃။ Page Setup & Styling ---
st.set_page_config(page_title="MLBB Shop", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    .stSelectbox { margin-top: -50px; }
    div.stButton > button {
        width: 100%;
        height: 120px;
        border-radius: 15px;
        border: 1px solid #555;
        font-size: 16px !important;
        white-space: pre-line;
    }
    div.stButton > button:active, div.stButton > button:focus {
        border: 3px solid #007bff !important;
        background-color: #f0f8ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

lang_col1, lang_col2 = st.columns([4, 1.5])
with lang_col2:
    sel_lang = st.selectbox("", ["မြန်မာ", "English", "日本語"], label_visibility="collapsed")

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
currency = st.radio(t["curr_label"], ["JPY", "MMK", "USDT"], horizontal=True, label_visibility="collapsed")

# --- ၆။ Item Selection Grid ---
st.subheader(t["select_pack"])
cols = st.columns(2)

if 'selected_pack' not in st.session_state:
    st.session_state.selected_pack = None
if 'selected_price' not in st.session_state:
    st.session_state.selected_price = None

for i, pack in enumerate(packs_data):
    price_val = pack[currency.lower()]
    curr_text = "円" if currency == "JPY" else currency
    price_display = f"{price_val:,} {curr_text}"
    label = f"{pack['icon']}\n{pack['name']}\n{price_display}"
    
    with cols[i % 2]:
        if st.button(label, key=f"pack_{i}"):
            st.session_state.selected_pack = pack['name']
            st.session_state.selected_price = price_display

if st.session_state.selected_pack:
    st.info(f"Selected: **{st.session_state.selected_pack}** ({st.session_state.selected_price})")

# --- ၇။ Payment & Upload ---
st.markdown("---")
with st.container(border=True):
    st.markdown(f"**Transfer to {currency}:**")
    if currency == "MMK": st.code("KPay: 09256084562 (U ZWE HTET AUNG)")
    elif currency == "JPY": st.code("PayPay : 08042419779")
    else: st.code("USDT (TRC20): TXXXXXXXXXXXXXXXX")

payment_ss = st.file_uploader(t["upload"], type=['jpg', 'png', 'jpeg'])

# --- ၈။ Final Submit with Approval Logic ---
if st.button(t["btn"], use_container_width=True, type="primary"):
    if user_id and zone_id and payment_ss and st.session_state.selected_pack:
        # စာသားပြရန် နေရာယူခြင်း
        status_placeholder = st.empty()
        status_placeholder.warning(t["processing"])
        
        with st.spinner(""):
            caption = (f"📩 *New Order (Pending Approval)*\n\n"
                      f"👤 ID: `{user_id}` ({zone_id})\n"
                      f"📦 Item: {st.session_state.selected_pack}\n"
                      f"💰 Price: {st.session_state.selected_price}\n"
                      f"💳 Method: {currency}")
            
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            reply_markup = {"inline_keyboard": [[
                {"text": "✅ Approve", "callback_data": "approve"},
                {"text": "❌ Reject", "callback_data": "reject"}
            ]]}
            
            data = {'chat_id': ADMIN_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown', 'reply_markup': json.dumps(reply_markup)}
            res = requests.post(url, files={'photo': payment_ss.getvalue()}, data=data)
            
            if res.status_code == 200:
                # Admin ရဲ့ Approve ကို စောင့်ကြည့်ခြင်း (၆၀ စက္ကန့်အထိ စောင့်မည်)
                found_approval = False
                for _ in range(30):
                    time.sleep(2)
                    try:
                        updates = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates").json()
                        for up in updates.get("result", []):
                            # Button နှိပ်ခြင်းကို စစ်ဆေးခြင်း
                            if "callback_query" in up and up["callback_query"].get("data") == "approve":
                                found_approval = True
                                break
                            # Admin က 'ok' လို့ စာရိုက်ပို့ခြင်းကို စစ်ဆေးခြင်း
                            if "message" in up and up["message"].get("text", "").lower() in ["ok", "done", "approve"]:
                                found_approval = True
                                break
                        if found_approval: break
                    except: continue
                
                status_placeholder.empty()
                if found_approval:
                    st.success(t["success"])
                    st.balloons()
                else:
                    st.error("Approval Timeout: ကျေးဇူးပြု၍ Admin ဆီ တိုက်ရိုက်ဆက်သွယ်ပါ။")
            else:
                status_placeholder.empty()
                st.error("Telegram Connection Error!")
    else:
        st.error(t["error"])
