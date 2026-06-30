import streamlit as st
import uuid
import g4f  # مكتبة توليد الإجابات الذكية الحقيقية مجاناً

# 1. إعدادات الصفحة والـ CSS المتقدم لتعديل التصميم والبروفايلات
st.set_page_config(page_title="A51 AI", page_icon="✨", layout="centered")

# رابط صورة الأسد الذهبي للذكاء الاصطناعي من ملف 1000094872.jpg
AI_AVATAR = "https://i.imgur.com/E8Y0Tz6.jpeg" 

st.markdown(f"""
    <style>
    /* إخفاء التاج الأحمر والمربع الافتراضي من لوطة تماماً */
    #MainMenu, footer, .stDeployButton {{
        visibility: hidden;
        display: none;
    }}
    
    /* إخفاء شريط الـ Header الفوقاني بالكامل (Fork و علامة GitHub) */
    header[data-testid="stHeader"] {{
        visibility: hidden;
        display: none;
    }}
    
    /* تصميم الخلفية العامة والخطوط */
    .stApp {{
        background-color: #0b0a0a;
        color: #ffffff;
    }}
    .main-title {{
        font-size: 50px;
        font-weight: bold;
        color: #d4af37; /* اللون الذهبي الفخم */
        text-align: center;
        letter-spacing: 5px;
        margin-top: 20px;
    }}
    .subtitle {{
        font-size: 14px;
        color: #888888;
        text-align: center;
        letter-spacing: 3px;
        margin-bottom: 30px;
    }}
    
    /* تحويل خط التبويب النشط (Tabs) من الأحمر إلى اللون الأزرق الفخم */
    button[data-baseweb="tab"] {{
        color: #ffffff !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #1e90ff !important; /* أزرق */
    }}
    div[data-testid="stTabs"] div[role="tablist"] div[style*="background-color: rgb(255, 75, 75)"] {{
        background-color: #1e90ff !important; 
    }}
    div[data-baseweb="tab-highlight-id"] {{
        background-color: #1e90ff !important;
    }}
    
    /* إخفاء صورة بروفايل المستخدم تماماً حسب طلبك */
    div[data-testid="chatAvatarUser"] {{
        visibility: hidden !important;
        display: none !important;
    }}
    
    /* تنسيق شريط الإدخال المتطور المماثل لـ ChatGPT */
    .chat-input-container {{
        display: flex;
        align-items: center;
        background-color: #1e1e1e;
        border-radius: 25px;
        padding: 5px 15px;
        margin-top: 10px;
    }}
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

# دالة لإنشاء محادثة جديدة
def create_new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {"name": f"محادثة جديدة {len(st.session_state.chats)+1}", "messages": []}
    st.session_state.current_chat_id = chat_id

if not st.session_state.chats:
    create_new_chat()

# ==========================================
# 3. واجهة تسجيل الدخول المصلحة (Authentication)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<div class='main-title'>A 5 1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>STRENGTH . POWER . PRESTIGE</div>", unsafe_allow_html=True)
    
    st.subheader("مرحباً بك في A51 AI - الرجاء تسجيل الدخول")
    
    tab1, tab2 = st.tabs(["تسجيل بالبريد الإلكتروني / Google", "الدخول كضيف"])
    
    with tab1:
        email = st.text_input("البريد الإلكتروني")
        password = st.text_input("كلمة المرور", type="password")
        if st.button("تسجيل الدخول / إنشاء حساب"):
            if email:
                st.session_state.logged_in = True
                st.session_state.user_type = "user"
                st.rerun()
            else:
                st.error("الرجاء إدخال البريد الإلكتروني")
                
    with tab2:
        st.write("يمكنك تجربة التطبيق كضيف، لكن بعض الميزات المتقدمة لن تكون متاحة.")
        if st.button("الدخول كضيف 🚶‍♂️"):
            st.session_state.logged_in = True
            st.session_state.user_type = "guest"
            st.rerun()

# ==========================================
# 4. الواجهة الرئيسية بعد تسجيل الدخول
# ==========================================
else:
    # القائمة الجانبية لإدارة المحادثات
    with st.sidebar:
        st.markdown("<div style='color:#d4af37; font-size:20px; font-weight:bold;'>A51 - إدارة المحادثات</div>", unsafe_allow_html=True)
        st.write(f"نوع الحساب: **{'مستخدم مسجل 👑' if st.session_state.user_type == 'user' else 'ضيف 🚶‍♂️'}**")
        
        if st.button("➕ محادثة جديدة"):
            create_new_chat()
            st.rerun()
            
        st.write("---")
        st.write("💬 المحادثات السابقة:")
        
        if st.session_state.user_type == "guest":
            st.warning("⚠️ حفظ وتعديل المحادثات غير متاح للضيوف.")
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

        if st.button("🚪 تسجيل الخروج"):
            st.session_state.logged_in = False
            st.session_state.chats = {}
            st.rerun()

    # العنوان الرئيسي للـ AI
    st.markdown("<div class='main-title'>A 5 1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>STRENGTH . POWER . PRESTIGE</div>", unsafe_allow_html=True)

    # عرض المحادثة الحالية بالبروفايلات الجديدة
    current_chat = st.session_state.chats[st.session_state.current_chat_id]
    
    for msg in current_chat["messages"]:
        if msg["role"] == "user":
            with st.chat_message("user", avatar=None): # تنحية صورة المستخدم تماماً
                st.write(msg["content"])
        else:
            with st.chat_message("assistant", avatar=AI_AVATAR): # صورة الأسد اللوجو لـ A51
                st.write(msg["content"])

    st.write("---")

    # نظام محاكاة شريط ChatGPT المتطور (أزرار تفتح عند الضغط على +)
    col_plus, col_empty = st.columns([1, 10])
    with col_plus:
        if st.button("➕", help="انقر لفتح الأدوات الإضافية"):
            st.session_state.show_tools = not st.session_state.show_tools
            st.rerun()

    # إذا نقر المستخدم على الـ + تظهر الأدوات الإضافية
    if st.session_state.show_tools:
        st.markdown("### 🛠️ الأدوات المضافة للشات")
        col1, col2 = st.columns(2)
        with col1:
            web_search = st.toggle("🌐 Recherche Web (البحث في الإنترنت)", value=True)
            camera_file = st.camera_input("📷 إلتقاط صورة فورية (Caméra)")
        with col2:
            uploaded_files = st.file_uploader("📁 تحميل ملفات وصور (Fichiers)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
            st.button("⚽ Suivez la Coupe du monde")
            st.button("✍️ Écrire ou modifier")

    # خانة إدخال الرسائل
    user_input = st.chat_input("بماذا يمكن لـ A51 أن يخدمك اليوم؟...")

    if user_input:
        # 1. حفظ ورسم رسالة المستخدم
        user_msg = {"role": "user", "content": user_input}
        current_chat["messages"].append(user_msg)
        
        # 2. توليد إجابة ذكية وحقيقية من الـ AI باستعمال g4f لتجيب على أي سؤال
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=[{"role": "user", "content": user_input}]
            )
            ai_response = response
        except Exception as e:
            ai_response = "عذراً، واجهت مشكلة صغيرة في الاتصال بالخادم الذكي. حاول مجدداً!"

        # 3. حفظ رسالة الـ AI
        ai_msg = {"role": "assistant", "content": ai_response}
        current_chat["messages"].append(ai_msg)
        st.rerun()
    
