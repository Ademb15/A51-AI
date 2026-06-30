import streamlit as st
import uuid

# 1. إعدادات الصفحة والـ CSS للحفاظ على التصميم الفخم وتعديل الصور
st.set_page_config(page_title="A51 AI", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    /* تصميم الخلفية والخطوط */
    .stApp {
        background-color: #0b0a0a;
        color: #ffffff;
    }
    .main-title {
        font-size: 50px;
        font-weight: bold;
        color: #d4af37; /* اللون الذهبي */
        text-align: center;
        letter-spacing: 5px;
        margin-top: 50px;
    }
    .subtitle {
        font-size: 14px;
        color: #888888;
        text-align: center;
        letter-spacing: 3px;
        margin-bottom: 30px;
    }
    /* إخفاء التاج الأحمر المزعج والحفاظ على أيقونة البروفايل الدائرية فقط */
    .profile-area {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 10px;
    }
    .profile-pic {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        border: 2px solid #d4af37;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
    }
    /* أزرار مخصصة وتنسيقات الجانبية */
    .sidebar-title {
        color: #d4af37;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 2. إعداد الحالات الافتراضية (Session State)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_type" not in st.session_state: # 'guest' أو 'user'
    st.session_state.user_type = None
if "chats" not in st.session_state:
    st.session_state.chats = {} # تخزين المحادثات {chat_id: {"name": name, "messages": []}}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# دالة لإنشاء محادثة جديدة
def create_new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {"name": f"محادثة جديدة {len(st.session_state.chats)+1}", "messages": []}
    st.session_state.current_chat_id = chat_id

# إنشاء أول محادثة تلقائياً إذا لم توجد
if not st.session_state.chats:
    create_new_chat()

# ==========================================
# 3. واجهة تسجيل الدخول (Authentication)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<div class='main-title'>A 5 1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>STRENGTH . POWER . PRESTIGE</div>", unsafe_allow_html=True)
    
    st.subheader("مرحباً بك في A51 AI - الرجاء تسجيل الدخول")
    
    tab1, tab2 = st.tabs(["تسجيل بالبريد الإلكتروني / Google", "الدخول كـ ضيف"])
    
    with tab1:
        email = st.text_input("البريد الإلكتروني")
        password = st.text_input("كلمة المرور", type="password")
        if st.button("تسجيل الدخول / إنشاء حساب"):
            if email: # محاكاة نجاح التسجيل
                st.session_state.logged_in = True
                st.session_state.user_type = "user"
                st.rerun()
            else:
                st.error("الرجاء إدخال البريد الإلكتروني")
                
    with tab2:
        st.write("يمكنك تجربة التطبيق كضيف، لكن بعض الميزات المتقدمة (مثل حفظ المحادثات وتوليد الصور) لن تكون متاحة.")
        if st.button("الدخول كـ ضيف 🚶‍♂️"):
            st.session_state.logged_in = True
            st.session_state.user_type = "guest"
            st.rerun()

# ==========================================
# 4. الواجهة الرئيسية بعد تسجيل الدخول
# ==========================================
else:
    # --- القائمة الجانبية (Sidebar) لادارة المحادثات ---
    with st.sidebar:
        st.markdown("<div class='sidebar-title'>A51 - إدارة المحادثات</div>", unsafe_allow_html=True)
        st.write(f"نوع الحساب: **{'مستخدم مسجل 👑' if st.session_state.user_type == 'user' else 'ضيف 🚶‍♂️'}**")
        
        if st.button("➕ محادثة جديدة"):
            create_new_chat()
            st.rerun()
            
        st.write("---")
        st.write("💬 المحادثات السابقة:")
        
        # عرض قائمة المحادثات مع إمكانية التعديل والمسح (متاحة فقط للمسجلين)
        if st.session_state.user_type == "guest":
            st.warning("⚠️ حفظ وتعديل المحادثات غير متاح للضيوف.")
            current_messages = st.session_state.chats[st.session_state.current_chat_id]["messages"]
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
                        else:
                            st.error("يجب ترك محادثة واحدة على الأقل!")

        if st.button("🚪 تسجيل الخروج"):
            st.session_state.logged_in = False
            st.session_state.chats = {}
            st.rerun()

    # --- القسم الرئيسي للتطبيق ---
    st.markdown("<div class='main-title'>A 5 1</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>STRENGTH . POWER . PRESTIGE</div>", unsafe_allow_html=True)

    # عرض المحادثة الحالية
    current_chat = st.session_state.chats[st.session_state.current_chat_id]
    
    for msg in current_chat["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "image" in msg:
                st.image(msg["image"])

    # --- الميزات المتقدمة والأزرار السريعة نتاع (1000094888.jpg) ---
    st.write("---")
    col_img, col_write, col_wc = st.columns(3)
    
    with col_img:
        if st.button("🎨 Créer une image"):
            if st.session_state.user_type == "guest":
                st.error("🔒 هذه الميزة تطلب تسجيل الدخول!")
            else:
                st.info("أكتب في الشات نوع الصورة التي تريد رسمها.")
                
    with col_write:
        if st.button("✍️ Écrire ou modifier"):
            st.info("أرسل النص الذي تريد كتابته أو تعديله الآن.")
            
    with col_wc:
        if st.button("⚽ Suivez la Coupe du monde"):
            st.success("🏆 تفعيل جلب آخر أخبار ونتائج كأس العالم حالياً!")

    # --- أدوات الـ Chat (الزائد نتاع 1000094886.jpg) ---
    with st.expander("🛠️ أدوات إضافية (Ajouter au chat)"):
        web_search = st.toggle("🌐 Recherche Web (البحث في الإنترنت)", value=True)
        
        uploaded_files = st.file_uploader("📁 تحميل صور وملفات بلا حدود (Fichiers)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        camera_file = st.camera_input("📷 إلتقاط صورة فورية (Caméra)")

    # --- خانة إدخال الرسائل والمستخدم (1000094885.jpg) ---
    user_input = st.chat_input("...أن يخدمك اليوم؟ A51 بماذا يمكن لـ")

    if user_input or uploaded_files or camera_file:
        # إضافة رسالة المستخدم للمحادثة
        user_msg = {"role": "user", "content": user_input if user_input else "تم إرسال ملف/صورة"}
        current_chat["messages"].append(user_msg)
        
        # محاكاة رد الذكاء الاصطناعي A51
        ai_response = f"أهلاً بك! أنا A51 AI. استلمت طلبك بنجاح."
        if web_search:
            ai_response += " [تم تفعيل البحث في الويب لتوفير معلومات دقيقة]"
            
        ai_msg = {"role": "assistant", "content": ai_response}
        current_chat["messages"].append(ai_msg)
        st.rerun()

    # --- ميزة مشاركة المحادثة ---
    st.write("---")
    share_text = "جربت تطبيق A51 AI الفخم! تطبيق ذكي وممتاز جداً."
    st.markdown(f'[📢 مشاركة التطبيق على فيسبوك](https://www.facebook.com/sharer/sharer.php?u=https://streamlit.io&quote={share_text})', unsafe_allow_html=True)

    # --- عرض أيقونة البروفايل نتاعك الفخمة فقط من لوطة (دون التاج الأحمر) ---
    st.markdown("""
        <div class='profile-area'>
            <!-- تم إبقاء أيقونة البروفايل الدائرية وحذف التاج الأحمر تماماً -->
            <div class='profile-pic' style='background-image: url("https://via.placeholder.com/45/d4af37/000000?text=A51"); background-size: cover;'></div>
        </div>
    """, unsafe_allow_html=True)
                
