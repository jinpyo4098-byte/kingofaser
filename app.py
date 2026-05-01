import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API 키 설정 (본인의 키로 교체)
GOOGLE_API_KEY = "여기에_발급받은_API_키를_넣으세요"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. 페이지 설정
st.set_page_config(page_title="📝 변형문제제조기", page_icon="🧠", layout="centered")

st.title("🧠 변형문제 제조기")
st.markdown("문제 사진을 업로드하면 AI가 분석하여 **유사한 변형 문제**를 만들어 드립니다! 🍀")
st.markdown("---")

# 세션 상태 초기화
if 'result' not in st.session_state:
    st.session_state.result = None

# 3. 파일 업로드
uploaded_file = st.file_uploader("문제 사진을 선택하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 문제 사진", use_container_width=True)
    
    if st.button("✨ 변형 문제 생성하기"):
        try:
            with st.spinner("AI가 문제를 분석 중입니다..."):
                # 모델 이름을 최신 버전인 'gemini-1.5-flash'로 설정
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                
                prompt = "이 이미지 속 문제를 읽고, 숫자나 상황을 바꾼 변형 문제를 정답/해설과 함께 한국어로 만들어줘."
                
                # AI 호출
                response = model.generate_content([prompt, image])
                st.session_state.result = response.text

        except Exception as e:
            st.error(f"에러가 발생했습니다: {e}")

# 결과 출력
if st.session_state.result:
    st.markdown("---")
    st.subheader("💡 생성된 변형 문제")
    st.success(st.session_state.result)
    
    if st.button("🔄 다시하기"):
        st.session_state.result = None
        st.rerun()

st.markdown("---")
st.caption("Made with Streamlit · Gemini AI 🍀")
