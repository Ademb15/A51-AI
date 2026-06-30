import streamlit as st
import uuid
import os
import urllib.request
import json

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="A51 AI", page_icon="✨", layout="centered")

# التأكد من قراءة صورة الأسد المحلية logo.jpg
if os.path.exists("logo.jpg"):
    AI_AVATAR = "logo.jpg"
else:
    AI_AVATAR = "👑"

# 2. تدمير كامل وشامل للون الأحمر وإخفاء بروفايل المستخدم بالـ CSS
st.markdown("""
    <style>
    /* إخفاء أدوات السيرفر والتاج الافتراضي من أسفل وأعلى الصفحة */
    #MainMenu, footer, .stDeployButton {
        visibility: hidden;
        display: none;
    }
    header[data-testid="stHeader"] {
        visibility: hidden;
        display: none;
    }
    
    /* إخفاء صورة بروفايل المستخدم (User Avatar) نهائياً */
    div[data-testid="chatAvatarUser"] {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* تصميم الخلفية العامة والخطوط */
    .stApp {
        background-color: #0b0a0a;
        color: #ffffff;
    }
    .main-title {
        font-size: 50px;
        font-weight: bold;
        color: #d4af37; /* ذهبي فخم */
        text-align: center;
        letter-spacing: 5px;
        margin-top: 20px;
    }
    .subtitle {
        font-size: 14px;
        color: #888888;
        text-align: center;
        letter-spacing: 3px;
        margin-bottom: 30px;
    }
    
    /* إبادة الخط الأحمر تحت الـ Tabs وتحويله للأزرق والذهبي */
    button[data-baseweb="tab"] {
        color: #ffffff !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1e90ff !important; /* أزرق ملكي */
    }
    /* استهداف شريط التبويب السفلي لمنع ظهور الأحمر تماماً */
    div[role="tablist"] div {
        background-color: transparent !important;
    }
    div[data-baseweb="tab-highlight-id"] {
        background-color: #1e90ff !important;
    }
    
    /* إبادة الحواف الحمراء من الـ Chat Input وصناديق الإدخال بالكامل */
    .stChatInputContainer, div[data-baseweb="input"], .stTextArea textarea, input {
        border: 1px solid #d4af37 !important; /* ذهبي دائم */
        box-shadow: none !important;
    }
    .stChatInputContainer:focus-within, div[data-baseweb="input"]:focus-within {
        border: 1px solid #1e90ff !important; /* يتحول للأزرق عند الكتابة */
        box-shadow: 0 0 4px #1e90ff !important;
    }
    
    /* إلغاء اللون الأحمر الافتراضي من أزرار الإرسال والأزرار الجانبية */
    button {
        border-color: #d4af37 !important;
        color: #ffffff !important;
    }
    button:hover {
        border-color: #1e90ff !important;
        color: #1e90ff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. إعداد الحالات الافتراضية (Session State)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_type" not in st.session_state: 
    st.session_state.user_type = None
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "show_tools" not in st.session_state:
    st.session_state.show_tools = False

def create_new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {"name": f"محادثة جديدة {len(st.session_state.chats)+1}", "messages": []}
    st.session_state.current_chat_id = chat_id

if not st.session_state.chats:
    create_new_chat()

# ==========================================
# 4. واجهة تسجيل الدخول (Authentication)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<div class='main-title'>A 5 1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>STRENGTH . POWER . PRESTIGE</div>", unsafe_allow_html=True)
    
    st.subheader("مرحباً بك في A51 AI - الرجاء تسجيل الدخول")
    
    tab1, tab2 = st.tabs(["تسجيل بالبريد الإلكتروني / Google", "الدخول كضيف"])
    
    with tab1:
        email = st.text_input("البريد الإلكتروني")
        password = st.text_input("كلمة المرور", type="password")
        if st.button("تسجيل الدخول / إنشاء حساب", key="login_btn"):
            if email:
                st.session_state.logged_in = True
                st.session_state.user_type = "user"
                st.rerun()
            else:
                st.error("الرجاء إدخال البريد الإلكتروني")
                
    with tab2:
        st.write("يمكنك تجربة التطبيق كضيف، لكن بعض الميزات المتقدمة لن تكون متاحة.")
        if st.button("الدخول كضيف 🚶‍♂️", key="guest_btn"):
            st.session_state.logged_in = True
            st.session_state.user_type = "guest"
            st.rerun()

# ==========================================
# 5. الواجهة الرئيسية بعد تسجيل الدخول
# ==========================================
else:
    with st.sidebar:
        st.markdown("<div style='color:#d4af37; font-size:20px; font-weight:bold;'>A51 - إدارة المحادثات</div>", unsafe_allow_html=True)
        st.write(f"نوع الحساب: **{'مستخدم مسجل 👑' if st.session_state.user_type == 'user' else 'ضيف 🚶‍♂️'}**")
        
        if st.button("➕ محادثة جديدة", key="new_chat_btn"):
            create_new_chat()
            st.rerun()
            
        st.write("---")
        st.write("💬 المحادثات السابقة:")
        
        if st.session_state.user_type == "guest":
            st.info("حفظ وتعديل المحادثات متاح للمشتركين.")
        else:
            for chat_id, chat_data in list(st.session_state.chats.items()):
                col_name, col_edit, col_del = st.columns([5, 2, 2])
                with col_name:
                    if st.button(chat_data["name"], key=f"select_{chat_id}"):
                        st.session_state.current_chat_id = chat_id
                        st.rerun()
                with col_edit:
                    new_name = st.text_input("📝", value=chat_data["name"], key=f"rename_{chat_id}", label_visibility="collapsed")
                    if new_name != chat_data["name"]:
                        st.session_state.chats[chat_id]["name"] = new_name
                        st.rerun()
                with col_del:
                    if st.button("🗑️", key=f"del_{chat_id}"):
                        if len(st.session_state.chats) > 1:
                            del st.session_state.chats[chat_id]
                            st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]
                            st.rerun()

        if st.button("🚪 تسجيل الخروج", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_
    
