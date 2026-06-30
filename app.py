import streamlit as st
import uuid
import os
import urllib.request
import json

# 1. إعدادات الصفحة والـ CSS المتقدم لتغيير الألوان بالكامل وإخفاء البروفايل
st.set_page_config(page_title="A51 AI", page_icon="✨", layout="centered")

# التأكد من قراءة صورة الأسد المحلية logo.jpg
if os.path.exists("logo.jpg"):
    AI_AVATAR = "logo.jpg"
else:
    AI_AVATAR = "👑"

st.markdown("""
    <style>
    /* 1. إخفاء التاج الأحمر الافتراضي وأدوات السيرفر من أسفل الصفحة */
    #MainMenu, footer, .stDeployButton {
        visibility: hidden;
        display: none;
    }
    header[data-testid="stHeader"] {
        visibility: hidden;
        display: none;
    }
    
    /* 2. إخفاء صورة بروفايل المستخدم (User Avatar) تماماً من الشات */
    div[data-testid="chatAvatarUser"] {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* 3. تنظيف وتغيير ألوان الخلفية والنصوص */
    .stApp {
        background-color: #0b0a0a;
        color: #ffffff;
    }
    .main-title {
        font-size: 50px;
        font-weight: bold;
        color: #d4af37; /* ذهبي */
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
    
    /* 4. إبادة اللون الأحمر من التبويبات (Tabs) وتحويلها للأزرق والذهبي */
    button[data-baseweb="tab"] {
        color: #ffffff !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1e90ff !important; /* أزرق فخم عند الاختيار */
    }
    div[data-testid="stTabs"] div[role="tablist"] div[style*="background-color: rgb(255, 75, 75)"] {
        background-color: #1e90ff !important; 
    }
    div[data-baseweb="tab-highlight-id"] {
        background-color: #1e90ff !important;
    }
    
    /* 5. إبادة الحواف الحمراء من خانات الإدخال (Inputs) عند الضغط عليها */
    div[data-baseweb="input"] {
        border-color: #d4af37 !important; /* تحويل الحواف للذهبي */
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #1e90ff !important; /* أزرق عند الكتابة */
        box-shadow: 0 0 0 1px #1e90ff !important;
    }
    
    /* 6. تعديل ألوان أزرار الـ Sidebar والأزرار العامة لتبتعد عن الأحمر */
    button[kind="primary"] {
        background-color: #1e90ff !important;
        color: white !important;
        border: none !important;
    }
    button[kind="secondary"] {
        background-color: #1c1a1a !important;
        color: #d4af37 !important;
        border: 1px solid #d4af37 !important;
    }
    button:hover {
        border-color: #1e90ff !important;
        color: #1e90ff !important;
    }
    
    /* 7. تغيير لون حواف الـ chat input الافتراضية لمنع اللون الأحمر */
    .stChatInputContainer {
        border-color: #d4af37 !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #1e90ff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. إعداد الحالات الافتراضية (Session State)
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
# 3. واجهة تسجيل الدخول (Authentication)
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
# 4. الواجهة الرئيسية بعد تسجيل الدخول
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
            st.session_state.chats = {}
            st.rerun()

    st.markdown("<div class='main-title'>A 5 1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>STRENGTH . POWER . PRESTIGE</div>", unsafe_allow_html=True)

    current_chat = st.session_state.chats[st.session_state.current_chat_id]
    
    # عرض الرسائل مع إخفاء كامل لبروفايل المستخدم
    for msg in current_chat["messages"]:
        if msg["role"] == "user":
            with st.chat_message("user", avatar=None): 
                st.write(msg["content"])
        else:
            with st.chat_message("assistant", avatar=AI_AVATAR): 
                st.write(msg["content"])

    st.write("---")

    col_plus, col_empty = st.columns([1, 10])
    with col_plus:
        if st.button("➕", help="انقر لفتح الأدوات الإضافية", key="tools_toggle"):
            st.session_state.show_tools = not st.session_state.show_tools
            st.rerun()

    if st.session_state.show_tools:
        st.markdown("### 🛠️ الأدوات المضافة للشات")
        col1, col2 = st.columns(2)
        with col1:
            web_search = st.toggle("🌐 Recherche Web (البحث في الإنترنت)", value=True, key="search_toggle")
            camera_file = st.camera_input("📷 إلتقاط صورة فورية (Caméra)", key="cam_input")
        with col2:
            uploaded_files = st.file_uploader("📁 تحميل ملفات وصور (Fichiers)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], key="file_upload")
            st.button("⚽ Suivez la Coupe du monde", key="wc_btn")
            st.button("✍️ Écrire ou modifier", key="edit_btn")

    user_input = st.chat_input("بماذا يمكن لـ A51 أن يخدمك اليوم؟...")
    
