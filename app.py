import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. 기본 설정 (Configuration)
# ==========================================

# [중요] API 키 설정
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    try:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
    except:
        st.error("API 키를 찾을 수 없습니다. Streamlit Cloud의 Secrets 설정을 확인해주세요.")
        st.stop()

genai.configure(api_key=API_KEY)

# 모델 설정: Gemini 2.5 Flash 적용
MODEL_NAME = "gemini-2.5-flash" 

st.set_page_config(
    page_title="Super Parents: Heroes Without Borders", # 페이지 탭 이름도 변경
    page_icon="🦸", # 아이콘 변경
    layout="centered"
)

# ==========================================
# [AI Function] 응답 생성 함수 (Global Setting)
# ==========================================
def get_gemini_response(image, parent_lang, homework_lang):
    """
    Generates a coaching guide using Gemini 2.5 Flash.
    System instructions are in English for better global performance.
    """
    
    # 프롬프트 지시문을 전면 영어로 변경 (모델 이해도 상승)
    prompt = f"""
    ### Role & Objective
    You are the **Lead AI Tutor** for the app "Super Parents".
    Your goal is to empower a parent who speaks **[ {parent_lang} ]** to perfectly understand and guide their child's homework (originally in **[ {homework_lang} ]**).

    ### Instructions
    Analyze the provided homework image and generate a structured guide.
    **The final output must be written entirely in {parent_lang}.**

    ### Output Format (Please follow this structure)
    
    1. **🎯 Homework Overview (1-Sentence Summary)**
       - Briefly explain the core learning objective of this assignment to the parent.
    
    2. **🗣️ Coaching Guide (Conversational Scripts)**
       - Provide specific dialogue/scripts the parent can say to the child.
       - Do NOT just give the answers. Instead, provide **guiding questions** to stimulate the child's thinking.
       - (e.g., "Ask your child: 'What do you think happens if we add these two numbers?'")

    3. **📝 Essential Vocabulary (Table Format)**
       - Select 3-5 key terms from the homework image.
       - Columns: [Original Word] | [Pronunciation (written in {parent_lang})] | [Meaning in {parent_lang}]

    4. **💡 Teacher's Pro Tip**
       - Explain the underlying concept, formula, or cultural context simply.
       - Mention common mistakes or traps students often fall into.

    ### Tone & Style
    - Professional, supportive, and encouraging (like a kind teacher).
    - Use clear **Markdown** (Bold, Tables, Lists) for readability.
    - **CRITICAL:** Regardless of the input language, your entire response must be in **{parent_lang}**.
    """
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        # 이미지 리스트 처리 (혹시 모를 호환성 대비)
        content_input = [prompt, image[0]] if isinstance(image, list) else [prompt, image]
        
        response = model.generate_content(content_input)
        return response.text
    except Exception as e:
        return f"Error occurred during analysis: {e}"


# ==========================================
# 2. 테마 및 디자인 (CSS)
# ==========================================

with st.sidebar:
    st.header("⚙️ Settings")
    theme_mode = st.selectbox("Theme Mode", ["Light Mode (Default)", "Dark Mode"])
    st.divider()
    st.markdown("Developed with Google Gemini")
    st.caption("⚠️ AI can make mistakes. Please verify important information.")

if "Dark" in theme_mode:
    bg_color = "#0E1117"
    text_color = "#FAFAFA"
    card_bg = "#262730"
    border_color = "#374151"
    header_bg = "#312E81" # 어두운 모드 헤더색 유지
    sub_text = "#D1D5DB" 
else:
    bg_color = "#F3F4F6"
    text_color = "#1F2937"
    card_bg = "#FFFFFF"
    border_color = "#E5E7EB"
    header_bg = "#4F46E5" # 밝은 모드: 인디고 퍼플 계열 (슈퍼히어로 느낌)
    sub_text = "#6B7280"


# ==========================================
# 수정된 디자인 및 헤더 코드
# ==========================================
st.markdown(f"""
<style>
    /* 전체 앱 배경 및 폰트 설정 */
    .stApp {{ background-color: {bg_color} !important; }}
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown li, .stMarkdown span {{ 
        color: {text_color} !important; 
    }}

    /* 헤더 숨김 */
    header {{visibility: hidden;}}

    /* 커스텀 헤더 컨테이너 */
    .custom-header {{
        background-color: {header_bg};
        padding: 2rem 1rem; /* 모바일 여백 최적화 */
        text-align: center;
        margin-top: -60px; /* 상단 빈 공간 제거 */
        margin-left: -5rem;
        margin-right: -5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}

    /* 헤더 타이틀 (Super Parents...) */
    .custom-header h1 {{
        color: #FFFFFF !important;
        font-family: sans-serif;
        font-weight: 800;
        font-size: clamp(1.5rem, 6vw, 2.5rem); /* 모바일에서 글자 크기 자동 조절 */
        margin-top: 10px;
        margin-bottom: 15px;
        line-height: 1.2;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.2);
    }}

    /* 서브타이틀 1 (You remain...) */
    .header-main-sub {{
        font-size: 1.1rem;
        font-weight: 600;
        color: #FFFFFF !important; /* 강제 흰색 */
        margin-bottom: 5px;
        opacity: 0.95;
        padding: 0 10px;
    }}

    /* 서브타이틀 2 (Understand in your language...) */
    .header-sub {{
        font-size: 0.9rem;
        color: #E0E7FF !important; /* 연한 보라/흰색 */
        font-weight: 400;
        line-height: 1.4;
        padding: 0 15px;
        opacity: 0.9;
    }}

    /* 파일 업로더 박스 디자인 */
    div[data-testid="stFileUploader"] {{
        border: 2px dashed {header_bg};
        border-radius: 12px;
        padding: 20px;
        background-color: {card_bg};
        text-align: center;
    }}

    /* 결과 박스 */
    .result-box {{
        background-color: {card_bg};
        padding: 20px;
        border-radius: 12px;
        border: 1px solid {border_color};
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    
    /* 면책 조항 */
    .disclaimer {{
        text-align: center;
        font-size: 0.75rem;
        color: {sub_text} !important;
        margin-top: 30px;
        margin-bottom: 50px;
    }}
</style>

<div class="custom-header">
<div style="font-size: 3rem; margin-bottom: 0;">🦸‍♂️ ♡ 🦸‍♀️</div>
<h1>Super Parents<br>Heroes Without Borders</h1>
<p class="header-main-sub">You remain your child's first and best teacher.</p>
<p class="header-sub">
Understand in your language, teach with confidence.<br>
Let your wisdom cross the language barrier.
</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. 메인 화면 (Main UI)
# ==========================================

with st.container():
    
    # 언어 선택 영역
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**🟣 Parent Language (Output)**")
        parent_lang = st.selectbox(
            "Select Parent Language", 
            [
                "English",
                "Korean (한국어)", 
                "Arabic (العربية)",
                "Turkish (Türkçe)",
                "Spanish (Español)",
                "Portuguese (Português)",
                "Dutch (Nederlands)",
                "French (Français)",
                "German (Deutsch)",
                "Chinese (中文)",
                "Japanese (日本語)",
                "Polish (Polski)",
                "Russian (Русский)",
                "Thai (ภาษาไทย)", 
                "Vietnamese (Tiếng Việt)"
            ], 
            index=0, # 기본값 English로 설정 (글로벌 타겟)
            label_visibility="collapsed"
        )
    with col2:
        st.markdown(f"**🟢 Homework Language (Input)**")
        target_lang = st.selectbox(
            "Select Homework Language", 
            ["Dutch", "English", "German", "French", "Spanish", "Chinese", "Auto Detect"], 
            index=0, # 기본값 Dutch (현재 타겟)
            label_visibility="collapsed"
        )

    st.markdown("---")
    
    # 단일 업로드 버튼
    st.markdown("### 📸 Upload Homework")
    st.caption("Tap 'Browse files' below to take a photo or choose from gallery.")
    
    image_data = st.file_uploader(
        "Upload Image or Take Photo", 
        type=["jpg", "png", "jpeg"], 
        label_visibility="collapsed"
    )

    # 이미지 처리 로직
    if image_data is not None:
        image = Image.open(image_data)
        
        st.markdown("### Preview")
        st.image(image, caption="Uploaded Homework", use_column_width=True)
        
        st.markdown("###") 
        
        # 버튼 문구도 약간 더 힘있게 변경
        submit = st.button("🚀 Activate Super Parent Mode", type="primary", use_container_width=True)

        if submit:
            status_text = st.empty()
            status_text.info("🤖 AI is preparing your coaching guide...")
            
            # 언어 텍스트 정리 (괄호 제거 등)
            p_lang_clean = parent_lang.split("(")[0].strip()
            
            # 함수 호출
            response_text = get_gemini_response(image, p_lang_clean, target_lang)
            
            # 결과 출력
            if "Error:" in response_text:
                status_text.error("❌ Error Occurred")
                st.error(response_text)
            else:
                status_text.success("✅ Ready to teach! (코칭 준비 완료!)")
                st.markdown("### 🎉 Your Coaching Guide")
                st.markdown(f'<div class="result-box">{response_text}</div>', unsafe_allow_html=True)
                
                # 면책 조항
                st.markdown("""
                    <div class="disclaimer">
                        ⚠️ <b>Disclaimer:</b> This tool supports parents but does not replace teachers.
                        Results by AI may vary. Always verify with official school materials.
                    </div>
                """, unsafe_allow_html=True)