import streamlit as st
from google import genai
import time
import os

# 1. إعدادات المنصة الملكية
st.set_page_config(
    page_title="A51 - AI PREMIUM", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. هندسة الـ CSS الفخمة والأنيقة (الذهبي والأسود الملكي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=400;600;800&family=Cinzel:wght=700&display=swap');
    
    /* الخلفية السينمائية للموقع */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background: radial-gradient(circle at top, #1c1917 0%, #0c0a09 100%) !important;
        color: #f5f5f4;
    }
    
    /* هيدر فخم جداً يحاكي التصميم الذهبي */
    .brand-container {
        text-align: center;
        padding: 20px;
        margin-bottom: 25px;
    }
    
    .brand-title {
        font-family: 'Cinzel', serif;
        font-size: 55px;
        font-weight: 800;
        letter-spacing: 3px;
        background: linear-gradient(135deg, #bf953f 0%, #fcf6ba 25%, #b38728 50%, #fbf5b7 75%, #aa771c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        filter: drop-shadow(0px 4px 15px rgba(212, 175, 55, 0.3));
        animation: goldGlow 3s ease-in-out infinite alternate;
    }
    
    .brand-subtitle {
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 5px;
        color: #a8a29e;
        margin-top: 5px;
    }

    @keyframes goldGlow {
        0% { filter: drop-shadow(0px 4px 10px rgba(189, 149, 63, 0.2)); }
        100% { filter: drop-shadow(0px 4px 25px rgba(252, 246, 186, 0.5)); }
    }

    /* صناديق الشات الفخمة المحاطة بلمسة ذهبية وخلفية داكنة مخملية */
    [data-testid="stChatMessage"] {
        border-radius: 16px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        background: rgba(28, 25, 23, 0.7) !important;
        border: 1px solid rgba(212, 175, 55, 0.1) !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    [data-testid="stChatMessage"]:hover {
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    
    /* تمييز صندوق المستخدم */
    [data-testid="stChatMessage"][data-test-avatar="user"] {
        border-left: 4px solid #bf953f !important;
    }
    
    /* تمييز صندوق الـ AI */
    [data-testid="stChatMessage"][data-test-avatar="assistant"] {
        border-right: 4px solid #fcf6ba !important;
    }
    
    /* إخفاء شعارات ستريمليت الزايدة تحت لزيادة الاحترافية */
    footer {visibility: hidden;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0) !important;}
    
    /* ستايل صندوق المدخلات (الكتابة) */
    [data-testid="stChatInput"] {
        border-radius: 25px !important;
        border: 1px solid #44403c !important;
        background-color: #1c1917 !important;
        color: #f5f5f4 !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #bf953f !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. واجهة البراند الملكي الفخم
st.markdown("""
    <div class="brand-container">
        <h1 class="brand-title">A 5 1</h1>
        <div class="brand-subtitle">STRENGTH . POWER . PRESTIGE</div>
    </div>
""", unsafe_allow_html=True)

# 4. إعداد صورة الـ Profile ديركت بالاسم الجديد الصحيح
IMAGE_NAME = "File_000000004f90724696ccafaa839a00f2.png"

ai_avatar = IMAGE_NAME if os.path.exists(IMAGE_NAME) else "👑"
user_avatar = "👤"

# 5. ربط الـ API بالذكاء الاصطناعي
# ما تنساش تبدل الجملة اللي لوطا بالـ Key السري متاعك!
API_KEY = "AQ.Ab8RN6LywCg9Qkt9LiH2a9WHltUJmBfyHzTEhh0sgh5V-a1VwA" 
client = genai.Client(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة باللوقو الفخم والجديد
for message in st.session_state.messages:
    current_avatar = user_avatar if message["role"] == "user" else ai_avatar
    with st.chat_message(message["role"], avatar=current_avatar):
        st.write(message["content"])

# 6. استقبال الكلام وصناعة أنيميشن الكتابة الفخمة
if prompt := st.chat_input("A51 في خدمتك..."):
    with st.chat_message("user", avatar=user_avatar):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar=ai_avatar):
        with st.spinner("🔱 يتم الآن استدعاء الذكاء الخارق لـ A51..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                full_response = response.text
                
                # أنيميشن ظهور الحروف التدريجي الفخم
                message_placeholder = st.empty()
                typed_text = ""
                for chunk in full_response.split(" "):
                    typed_text += chunk + " "
                    time.sleep(0.04)
                    message_placeholder.write(typed_text + "⏳")
                message_placeholder.write(full_response)
                
            except Exception as e:
                full_response = "❌ عذراً الملك، حدث خلل في الاتصال. تأكد من جودة الـ API Key."
                st.error(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
