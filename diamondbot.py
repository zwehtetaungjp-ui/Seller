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
        "select_pack": "ပစ္စည်းအမျိုးအစား ရွေးချယ်ပါ",
        "pay_method": "ငွေပေးချေမှုစနစ်",
        "upload": "ငွေလွှဲပြေစာ တင်ပေးပါ",
        "btn": "အခုပဲ ဝယ်ယူမည်",
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
        "upload": "振込明細書（レシート）をアップロード",
        "btn": "今すぐ購入",
        "success": "注文が完了しました！",
        "error": "すべての項目を入力してください！",
        "curr_label": "通貨を選択"
    }
}

packs_data = [
    {"name": "Weekly Diamond Pass", "icon": "🎟️", "mmk": 2500, "jpy": 150, "usdt": 1.0},
    {"name": "Starlight Pass", "icon": "🌟", "mmk": 7500, "jpy": 450, "usdt": 3.2},
    {"name": "275 Diamonds", "icon": "💎", "mmk": 8500, "jpy": 480, "usdt": 3.3},
    {"name": "565 Diamonds", "icon": "🎁", "mmk": 16500, "jpy": 950, "usdt": 6.5},
    {"name": "1155 Diamonds", "icon": "📦", "mmk": 32000, "jpy": 1850, "usdt": 12.8},
    {"name": "1765 Diamonds", "icon": "🏆", "mmk": 48000, "jpy": 2800, "usdt": 19.5},
    {"name": "2975 Diamonds", "icon": "👜", "mmk": 82000, "jpy": 4700, "usdt": 32.5},
    {"name": "6000 Diamonds", "icon": "👑", "mmk": 160000, "jpy": 9200, "usdt": 63.0}
]

# --- ၃။ Page Setup & Styling ---
st.set_page_config(page_title="MLBB Shop", page_icon="💎", layout="centered")

# CSS: Language Selector ကို ညာဘက်အပေါ်မှာထားခြင်းနှင့် Button Styling
st.markdown("""
    <style>
    /* Language Selector UI */
    .stSelectbox {
        margin-top: -50px;
    }
    div.stButton > button {
        width: 100%;
        height: 140px;
        border-radius: 15px;
        border: 1px solid #555;
        font-size: 16px !important;
        white-space: pre-line;
    }
    div.stButton > button:active, div.stButton > button:focus {
        border: 3px solid #007bff !important;
        background-color: #f0f8ff !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ညာဘက်အပေါ်ထောင့်မှာ Language Selector ပြရန် column ခွဲခြင်း
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
currency = st.radio(t["curr_label"], ["MMK", "JPY", "USDT"], horizontal=True, label_visibility="collapsed")

# --- ၆။ Item Selection Grid (တစ်တန်း ၂ ခု) ---
st.subheader(t["select_pack"])
cols = st.columns(2)

if 'selected_pack' not in st.session_state:
    st.session_state.selected_pack = None
if 'selected_price' not in st.session_state:
    st.session_state.selected_price = None

for i, pack in enumerate(packs_data):
    price_val = pack[currency.lower()]
    # JPY အတွက်ဆိုရင် 円 လို့ပြမယ်
    curr_text = "円" if currency == "JPY" else currency
    price_display = f"{price_val:,} {curr_text}"
    label = f"{pack['icon']}\n{pack['name']}\n{price_display}"
    
    with cols[i % 2]:
        if st.button(label, key=f"pack_{i}"):
            st.session_state.selected_pack = pack['name']
            st.session_state.selected_price = price_display

if st.session_state.selected_pack:
    st.info(f"Selected: *{st.session_state.selected_pack}* ({st.session_state.selected_price})")

# --- ၇။ Payment & Upload ---
st.markdown("---")
with st.container(border=True):
    # Japan ဘာသာစကားဆိုရင် Japan Post ကို အပေါ်မှာပြပေးမယ်
    st.markdown(f"*Transfer to {currency}:*")
    if currency == "MMK": st.code("KPay: 09 123 456 789")
    elif currency == "JPY": st.code("Japan Post: 12345-67890 (MYO MIN)")
    else: st.code("USDT (TRC20): TXXXXXXXXXXXXXXXX")

payment_ss = st.file_uploader(t["upload"], type=['jpg', 'png', 'jpeg'])

# --- ၈။ Final Submit ---
if st.button(t["btn"], use_container_width=True, type="primary"):
    if user_id and zone_id and payment_ss and st.session_state.selected_pack:
        with st.spinner("Processing..."):
            caption = (f"📦 New Order!\n\n👤 ID: {user_id} ({zone_id})\n📦 Item: {st.session_state.selected_pack}\n💰 Price: {st.session_state.selected_price}\n💳 Method: {currency}")
            
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            reply_markup = {"inline_keyboard": [[{"text": "✅ Approve", "callback_data": "approve"},{"text": "❌ Reject", "callback_data": "reject"}]]}
            
            data = {'chat_id': ADMIN_CHAT_ID, 'caption': caption, 'reply_markup': json.dumps(reply_markup)}
            res = requests.post(url, files={'photo': payment_ss.getvalue()}, data=data)
            
            if res.status_code == 200:
                st.success(t["success"])
                st.balloons()
            else:
                st.error("Telegram Error! Check Token/ID.")
    else:
        st.error(t["error"])

