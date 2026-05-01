import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# ==========================================
# 1. API 키 설정 (여기에 발급받은 키를 넣으세요)
# ==========================================
GOOGLE_API_KEY = "AIzaSyBGvWNj0tilceOFsfh_HFLttSV4tAOmXe8"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. 페이지 설정
st.set_page_config(page_title="📝 변형문제제조기", page_icon="🧠", layout="centered")

# 3. 디자인 및 헤더
st.title("🧠 변형문제제조기")
st.markdown("문제 사진을 업로드하면 AI가 분석하여 **유사한 변형 문제**를 만들어 드립니다! 🍀")
st.markdown("---")

# 4. 세션 상태 초기화 (다시하기 기능을 위해)
if 'result' not in st.session_state:
    st.session_state.result = None

# 5. 파일 업로드 섹션
uploaded_file = st.file_uploader("문제 사진을 선택하거나 드래그하세요 (JPG, PNG, JPEG)", type=["jpg", "jpeg", "png"])

# 6. 메인 로직
if uploaded_file is not None:
    # 업로드된 이미지 표시
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 문제 사진", use_container_width=True)
    
    # 버튼 클릭 시 문제 생성
    if st.button("✨ 변형 문제 생성하기"):
        try:
            with st.spinner("AI가 문제를 읽고 열심히 새 문제를 만드는 중..."):
                # Gemini 1.5 Flash 모델 사용 (이미지 인식 + 텍스트 생성)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 프롬프트 구성
                prompt = """
                이미지 속의 문제를 정확히 읽고 분석한 뒤, 다음 조건에 맞춰 변형 문제를 만들어줘:
                1. 원본 문제와 개념은 같지만 숫자, 상황, 인물 등을 바꿔서 새로운 문제를 생성할 것.
                2. '문제', '정답', '해설'을 구분해서 보기 좋게 출력할 것.
                3. 한국어로 친절하게 설명해줄 것.
                """
                
                # API 호출 (이미지와 프롬프트 전달)
                response = model.generate_content([prompt, image])
                st.session_state.result = response.text

        except Exception as e:
            st.error(f"에러가 발생했습니다: {e}")
            st.info("API 키가 올바른지, 혹은 인터넷 연결을 확인해 주세요.")

# 7. 결과 출력
if st.session_state.result:
    st.markdown("---")
    st.subheader("💡 생성된 변형 문제")
    st.success(st.session_state.result)
    
    # 8. 다시하기 버튼
    if st.button("🔄 다시하기 (다른 문제 하기)"):
        st.session_state.result = None
        st.rerun()

# 9. 하단 캡션
st.markdown("---")
st.caption("Made with Streamlit · Gemini AI 기반 변형문제 생성기 🍀")
