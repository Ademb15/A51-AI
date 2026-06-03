import streamlit as st
from google import genai

# إعداد واجهة الموقع
st.set_page_config(page_title="AI Tools V7", page_icon="🤖")
st.title(" A51 AI")
st.write("اسألني أي شيء وسأجيبك فوراً!")

# حط المفتاح متاعك هنا
GEMINI_KEY = "AQ.Ab8RN6LywCg9Qkt9LiH2a9WHltUJmBfyHzTEhh0sgh5V-a1VwA"

try:
    client = genai.Client(api_key=GEMINI_KEY)
except Exception as e:
    st.error(f"خطأ في إعداد المفتاح: {e}")

# عمل مكان لرسائل المحادثة (Chat History)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال سؤال المستخدم
if user_input := st.chat_input("اكتب سؤالك هنا..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # إرسال الطلب لـ Gemini
    try:
        with st.chat_message("assistant"):
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_input,
            )
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
