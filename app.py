import streamlit as st
import uuid
import os
import urllib.request
import urllib.parse

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="A51 AI", page_icon="✨", layout="centered")

# التأكد من مسار صورة الأسد الفخمة
if os.path.exists("logo.jpg"):
    AI_AVATAR = "logo.jpg"
else:
    AI_AVATAR = "👑"

# 2. الـ CSS المطور والجذري لحذف الأيقونات الحمراء وتكبير شعار الأسد الجديد
st.markdown("""
    <style>
    /* إخفاء أدوات السيرفر والتاج من أعلى وأسفل الصفحة */
    #MainMenu, footer, .stDeployButton {
        visibility: hidden !important;
        display: none !important;
    }
    header[data-testid="stHeader"] {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* إخفاء أيقونة المستخدم نهائياً (المسجل والضيف والـ Red Icon) */
    div[data-testid="stChatMessageAvatarUser"] {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* تكبير وتحسين مظهر صورة الأسد المذهبة للـ AI الخاص بك */
    div[data-testid="stChatMessageAvatarAssistant"] {
        width: 45px !important;
        height: 45px !important;
        border-radius: 50% !important;
        border: 2px solid #d4af37 !important; /* إطار ذهبي فخم */
        overflow: hidden !important;
    }
    div[data-testid="stChatMessageAvatarAssistant"] img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
    }
    
    /* خلفية التطبيق الداكنة الفخمة */
    .stApp {
        background-color: #0b0a0a !important;
        color: #ffffff !important;
    }
    .main-title {
        font-size: 50px;
        font-weight: bold;
        color: #d4af37;
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
    
    /* ألوان التبويبات وصندوق الكتابة لمنع اللون الأحمر */
    button[data-baseweb="tab"] {
        color: #ffffff !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1e90ff !important;
    }
    div[data-baseweb="tab-highlight-id"] {
        background-color: #1e90ff !important;
    }
    .stChatInputContainer {
        border-color: #d4af37 !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #1e90ff !important;
    }
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

# 3. إعداد الـ Session State
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
# 4. واجهة تسجيل الدخول
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<div class='main-title'>A 5 1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>STRENGTH . POWER . PRESTIGE</div>", unsafe_allow_html=True)
    st.subheader("مرحباً بك في A51 AI")
    
    tab1, tab2 = st.tabs(["تسجيل بالبريد الإلكتروني / Google", "الدخول كضيف"])
    with tab1:
        email = st.text_input("البريد الإلكتروني")
        password = st.text_input("كلمة المرور", type="password")
        if st.button("تسجيل الدخول", key="login_btn"):
            if email:
                st.session_state.logged_in = True
                st.session_state.user_type = "user"
                st.rerun()
            else:
                st.error("الرجاء إدخال البريد الإلكتروني")
    with tab2:
        if st.button("الدخول كضيف 🚶‍♂️", key="guest_btn"):
            st.session_state.logged_in = True
            st.session_state.user_type = "guest"
            st.rerun()

# ==========================================
# 5. واجهة الشات الرئيسية
# ==========================================
else:
    with st.sidebar:
        st.markdown("<div style='color:#d4af37; font-size:20px; font-weight:bold;'>A51 - إدارة المحادثات</div>", unsafe_allow_html=True)
        if st.button("➕ محادثة جديدة", key="new_chat_btn"):
            create_new_chat()
            st.rerun()
        st.write("---")
        
        if st.session_state.user_type != "guest":
            for chat_id, chat_data in list(st.session_state.chats.items()):
                col_name, col_del = st.columns([7, 2])
                with col_name:
                    if st.button(chat_data["name"], key=f"select_{chat_id}"):
                        st.session_state.current_chat_id = chat_id
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
    
    # عرض الرسائل بـ Avatars مصلحة
    for msg in current_chat["messages"]:
        if msg["role"] == "user":
            with st.chat_message("user", avatar=None):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant", avatar=AI_AVATAR):
                st.write(msg["content"])

    st.write("---")

    col_plus, _ = st.columns([1, 10])
    with col_plus:
        if st.button("➕", key="tools_toggle"):
            st.session_state.show_tools = not st.session_state.show_tools
            st.rerun()

    if st.session_state.show_tools:
        st.markdown("### 🛠️ الأدوات المتقدمة")
        col1, col2 = st.columns(2)
        with col1:
            web_search = st.toggle("🌐 Recherche Web", value=True, key="search_toggle")
            camera_file = st.camera_input("📷 Caméra", key="cam_input")
            dev_mode = st.toggle("💻 Mode Programmation (وضع البرمجة)", value=False, key="dev_mode_toggle")
        with col2:
            uploaded_files = st.file_uploader("📁 Fichiers", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], key="file_upload")
            cyber_mode = st.toggle("🛡️ Mode CyberSécurité (وضع الأمن السيبراني)", value=False, key="cyber_mode_toggle")

    user_input = st.chat_input("بماذا يمكن لـ A51 أن يخدمك اليوم؟...")

    if user_input:
        user_msg = {"role": "user", "content": user_input}
        current_chat["messages"].append(user_msg)
        
        # تحسين صياغة النظام لمنع أي مشاكل في الروابط
        system_instructions = "You are A51 AI, an expert assistant. Respond directly and beautifully in Arabic."
        if st.session_state.get("dev_mode_toggle"):
            system_instructions += " Focus deeply on programming and algorithms."
        if st.session_state.get("cyber_mode_toggle"):
            system_instructions += " Focus deeply on cybersecurity and systems protection."

        # الاتصال المباشر والآمن بالـ API بدون استخدام نصوص طوارئ مكررة
        try:
            api_url = "https://text.pollinations.ai/"
            encoded_prompt = urllib.parse.quote(user_input)
            encoded_system = urllib.parse.quote(system_instructions)
            full_url = f"{api_url}{encoded_prompt}?model=searchgpt&system={encoded_system}" # تم التغيير لـ searchgpt لسرعة الاستجابة
            
            req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                ai_response = response.read().decode('utf-8')
        except Exception as e:
            ai_response = f"عذراً يا غالي، واجهت مشكلة في الاتصال بالسيرفر الخارجي. تأكد من الإنترنت وأعد المحاولة! (الخطأ: {str(e)})"

        ai_msg = {"role": "assistant", "content": ai_response}
        current_chat["messages"].append(ai_msg)
        st.rerun()
    
