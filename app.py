from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from llm_client import TriageClient
from prompts import build_user_prompt
from red_flags import screen

load_dotenv(Path(__file__).parent / ".env")

st.set_page_config(page_title="مساعد الفحص المبدئي للألم", page_icon="🩺")

st.title("🩺 مساعد الفحص المبدئي للألم")
st.warning(
    "⚠️ هذا الموقع أداة **فحص مبدئي فقط وليس تشخيصًا طبيًا نهائيًا**. "
    "في حالة الطوارئ اتصل بالإسعاف فورًا أو توجه لأقرب مستشفى."
)

with st.form("triage_form"):
    description = st.text_area(
        "اكتب وصف الألم أو الأعراض (بالعربي أو الإنجليزي)",
        placeholder="مثال: عندي ألم في الصدر من ساعتين، بيزيد لما اتنفس بعمق...",
        height=140,
    )
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        age = st.text_input("العمر", "")
    with col2:
        sex = st.selectbox("الجنس", ["", "ذكر", "أنثى"])
    with col3:
        duration = st.text_input("مدة الألم", placeholder="مثال: يومين")
    with col4:
        severity = st.slider("شدة الألم (0-10)", 0, 10, 5)

    submitted = st.form_submit_button("اعمل الفحص المبدئي")

if submitted:
    if not description.strip():
        st.error("من فضلك اكتب وصف الألم الأول.")
        st.stop()

    emergency_hits = screen(description)
    if emergency_hits:
        st.error(
            "🚨 **الوصف بتاعك فيه إشارات ممكن تكون طارئة "
            f"({', '.join(emergency_hits)}).** توجه لأقرب طوارئ / اتصل بالإسعاف فورًا، "
            "ومتستناش رد النموذج تحت."
        )

    with st.spinner("جاري تحليل الوصف..."):
        try:
            client = TriageClient()
            user_prompt = build_user_prompt(description, age, sex, duration, severity)
            result = client.assess(user_prompt)
        except Exception as e:
            st.error(f"حصل خطأ أثناء الاتصال بالنموذج: {e}")
            st.stop()

    st.subheader("نتيجة الفحص المبدئي")
    st.markdown(result)
    st.caption("هذا الفحص المبدئي لا يغني عن استشارة طبيب مختص.")
