import streamlit as st
from google import genai
import time

# 1. إعدادات الصفحة الأساسية (الأيقونة والعرض الكامل)
st.set_page_config(
    page_title="AI Tools V7", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. زينة الـ CSS السحرية (الألوان، الانميشن، الخطوط، وخلفية الشات)
st.markdown("""
    <style>
    /* تغيير الخط وتنسيق الخلفية العامة */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-color: #0f172a; /* خلفية داكنة احترافية */
        color: #f8fafc;
    }
    
    /* أنيميشن وعنوان الموقع الملون */
    .main-title {
        font-size: 45px;
        font-weight: 700;
        background: linear-gradient(45deg, #00f2fe, #4facfe, #0000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: -20px;
        margin-bottom: 5px;
        animation: pulse 2s infinite;
    }
    
    .sub-title {
        color: #94a3b8;
        text-align: center;
        font-size: 16px;
        margin-bottom: 30px;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }

    /* تحسين شكل صناديق الشات */
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* تخصيص ميساج المستخدم */
    [data-testid="stChatMessage"][data-test-avatar="user"] {
        background-color: #1e293b !important;
        border-left: 5px solid #00f2fe;
    }
    
    /* تخصيص ميساج الـ Bot */
    [data-testid="stChatMessage"][data-test-avatar="assistant"] {
        background-color: #0f172a !important;
        border: 1px solid #334155;
        border-right: 5px solid #4facfe;
    }
    
    /* زينة لصندوق الكتابة اللوطاني */
    [data-testid="stChatInput"] {
        border-radius: 30px !important;
        border: 2px solid #334155 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. واجهة الموقع (العناوين المزينة)
st.markdown('<h1 class="main-title">✨ AI Tools V7 ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">المساعد الذكي الأقوى والأجمل على الإطلاق 🚀</p>', unsafe_allow_html=True)

# 4. ربط الـ API بالذكاء الاصطناعي (تأكد من وضع الـ Key متاعك هنا)
# ملاحظة: من المستحسن مستقبلاً تحط الـ Key في الـ Secrets متاع Streamlit
API_KEY = "حط_الـ_API_KEY_متاعك_هنا" 
client = genai.Client(api_key=API_KEY)

# 5. إدارة ذاكرة الشات (علشان يتفكر الميساجات القديمة)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الميساجات القديمة بالأيقونات المزينة الجديدة
for message in st.session_state.messages:
    avatar_icon = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.write(message["content"])

# 6. استقبال كلام المستخدم وتوليد الإجابة مع أنيميشن التفكير
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    # عرض ميساج المستخدم على البلاصة
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # أنيميشن التحميل والتفكير المزيانة (Spinner)
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("⚡ قاعد نخمم ونحلل في الإجابة... لحظة برك"):
            try:
                # إرسال السؤال للـ API (Gemini)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                full_response = response.text
                
                # حركة احترافية: إظهار الكتيبة كأن الـ Bot قاعد يكتب توا (Typewriter effect)
                message_placeholder = st.empty()
                typed_text = ""
                for chunk in full_response.split(" "):
                    typed_text += chunk + " "
                    time.sleep(0.05)  # سرعة ظهور الكلمات
                    message_placeholder.write(typed_text + "▌")
                message_placeholder.write(full_response)
                
            except Exception as e:
                full_response = "❌ صار خطأ صغير، ثبت من الـ API Key متاعك يا غالي!"
                st.error(full_response)
        
        # حفظ ميساج الـ Bot في الذاكرة
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
