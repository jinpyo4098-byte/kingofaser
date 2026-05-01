import streamlit as st
import random
# 실제 이미지 처리와 문제 생성을 위해 외부 라이브러리나 API가 필요할 수 있습니다.
# 이 코드는 구조를 보여주는 예시이므로, 실제 작동을 위해 OCR 및 AI 모델 API 연동이 필요할 수 있습니다.
from PIL import Image

# 1. 페이지 설정
st.set_page_config(page_title="📝 변형문제제조기", page_icon="🧠", layout="centered")

# 2. 메인 제목 및 설명 (첫 화면)
st.title("🧠 변형문제제조기")
st.markdown("문제 사진을 넣어주세요! 사진 속 문제와 비슷한 **새로운 변형 문제**를 만들어 드립니다. 🍀")

# 3. 사진 업로드 섹션
uploaded_file = st.file_uploader("여기에 문제 사진을 올려주세요.", type=["png", "jpg", "jpeg"])

# 4. 세션 상태 초기화 (결과를 저장하고 '다시하기' 기능을 구현하기 위해 사용)
if 'original_text' not in st.session_state:
    st.session_state['original_text'] = ""
if 'variant_problem' not in st.session_state:
    st.session_state['variant_problem'] = ""
if 'image_uploaded' not in st.session_state:
    st.session_state['image_uploaded'] = False

# 사진을 읽고 문제를 생성하는 함수 (모의 구현)
# 실제 작동을 위해서는 OCR API(Google Vision, Tesseract 등)와 문제 생성 AI(OpenAI 등)를 연동해야 합니다.
def process_and_generate(file):
    with st.spinner("사진을 읽고 문제를 분석하는 중입니다... 잠시만 기다려주세요."):
        # 사진을 텍스트로 읽는 OCR 과정 (모의)
        # 이미지 열기
        image = Image.open(file)
        # 실제 OCR 코드가 들어갈 자리입니다. 예시로 가상의 텍스트를 생성합니다.
        # 예시 문제: "철수는 사과 3개를 가지고 있습니다. 영희에게 1개를 주면 몇 개가 남나요?"
        # 이 단계에서 실제 OCR API를 호출하여 이미지 내 텍스트를 추출합니다.
        mock_ocr_text = "문제 사진 내용 (OCR 추출 예시): '철수는 사과 3개를 가지고 있습니다. 영희에게 1개를 주면 몇 개가 남나요?'"
        
        # 변형 문제를 생성하는 과정 (모의)
        # 실제 문제 생성 AI(예: GPT) API를 호출하여 변형 문제를 생성합니다.
        variant_prompt = "이 문제와 비슷한 숫자를 바꾸고 상황을 변형한 문제를 만들어주세요: " + mock_ocr_text
        # 가상의 AI 응답
        mock_variant_problem = "변형 문제 (예시): '영수는 귤 5개를 가지고 있습니다. 지수에게 2개를 주면 몇 개가 남나요?'"
        
        return image, mock_ocr_text, mock_variant_problem

# 5. 사진 업로드 시 작동 로직
if uploaded_file is not None and not st.session_state['image_uploaded']:
    # 사진을 열어 사용자에게 보여줍니다.
    original_image, ocr_text, variant_problem = process_and_generate(uploaded_file)
    
    # 세션 상태에 데이터 저장
    st.session_state['original_text'] = ocr_text
    st.session_state['variant_problem'] = variant_problem
    st.session_state['image_uploaded'] = True
    
    # 화면을 새로고침하여 결과를 표시합니다.
    st.rerun()

# 6. 결과 표시 섹션 (사진 업로드 및 처리가 완료된 경우)
if st.session_state['image_uploaded']:
    st.subheader("📸 원본 문제 사진")
    # 원본 이미지를 다시 보여줍니다.
    # st.image(uploaded_file) # 파일 업로드 위젯이 살아있으면 다시 보여주기 어렵습니다.
    # 세션 상태에 이미지를 저장하는 것은 복잡하므로, 파일 업로드 위젯을 사용하여 다시 보여줍니다.
    # 또는 process_and_generate 함수에서 이미지를 반환하지 않고 파일 업로드 위젯을 그대로 사용합니다.
    
    # st.image 함수는 다시 호출해야 합니다.
    # uploaded_file은 st.rerun 이후에 사라지지 않으므로 st.image(uploaded_file)을 사용할 수 있습니다.
    # 하지만 결과 화면에서는 file_uploader가 사라지게 하는 것이 더 자연스럽습니다.
    # 이를 해결하기 위해 이전에 st.image(original_image)로 이미지 객체를 st.session_state에 저장할 수도 있지만,
    # 여기서는 간단하게 uploaded_file이 None이 아니라는 것을 이용하여 다시 보여줍니다.
    if uploaded_file is not None:
        st.image(uploaded_file, caption="업로드한 원본 문제 사진", use_column_width=True)

    st.subheader("📝 추출된 문제")
    st.code(st.session_state['original_text'], language="python") # 이전 코드의 map, str 등과 유사하게 서식을 맞춥니다.

    st.subheader("💡 변형 문제 결과")
    st.success(st.session_state['variant_problem'])

    # 7. 다시하기 버튼
    st.markdown("---")
    if st.button("🔄 다시하기 (새 사진 넣기)"):
        # 세션 상태 초기화
        st.session_state['original_text'] = ""
        st.session_state['variant_problem'] = ""
        st.session_state['image_uploaded'] = False
        # 사진 업로드 위젯을 초기화하기 위해 페이지를 새로고침합니다.
        st.rerun()

# 8. 하단 구분선 및 캡션 (첫 화면 및 결과 화면 공통)
st.markdown("---")
st.caption("Made with Streamlit · 변형 문제로 학습 효과 Up! 🍀")
