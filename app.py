import streamlit as st
import google.generativeai as genai
from PIL import Image


# 수정된 코드: Streamlit secrets에서 키를 불러옵니다.
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# ... (나머지 코드는 동일) ...

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

    # 버튼 클릭 시 AI 호출
    if st.button("✨ 변형 문제 생성하기"):
        try:
            with st.spinner("AI가 문제를 분석 중입니다..."):
                # 모델 설정
                model = genai.GenerativeModel('gemini-2.0-flash')
                
                prompt = "이 이미지 속 문제를 읽고, 숫자나 상황을 바꾼 변형 문제를 정답/해설과 함께 한국어로 만들어줘."
                
                # AI 호출
                response = model.generate_content([prompt, image])
                
                # 결과 저장 및 화면 갱신
                st.session_state.result = response.text
                st.rerun() # 결과를 즉시 보여주기 위해 새로고침
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# 4. 결과 출력 (버튼 밖에 위치해야 결과가 사라지지 않습니다)
if st.session_state.result:
    st.success("변형 문제 생성이 완료되었습니다!")
    st.markdown("---")
    st.markdown(st.session_state.result)
    
    # 다시하기 버튼
    if st.button("🔄 다시하기"):
        st.session_state.result = None
        st.rerun()

st.markdown("---")
st.caption("Made with Streamlit · Gemini AI 🍀")
