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
    page_title="Parenting Without Borders",
    page_icon="♡",
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
    You are the **Lead AI Tutor** for the app "Parenting Without Borders".
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
    header_bg = "#312E81"
    sub_text = "#D1D5DB" 
else:
    bg_color = "#F3F4F6"
    text_color = "#1F2937"
    card_bg = "#FFFFFF"
    border_color = "#E5E7EB"
    header_bg = "#4F46E5"
    sub_text = "#6B7280"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color} !important; }}
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown li, .stMarkdown span {{ color: {text_color} !important; }}
    
    header {{visibility: hidden;}}
    
    .custom-header {{
        background-color: {header_bg};
        padding: 2rem 1rem;
        text-align: center;
        margin-top: -50px;
        margin-left: -5rem;
        margin-right: -5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    .custom-header h1 {{
        color: white !important;
        font-weight: 700;
        font-size: clamp(1.8rem, 5vw, 2.5rem); 
        margin-bottom: 0.5rem;
        white-space: normal;
        word-wrap: break-word;
        line-height: 1.2;
    }}
    
    .custom-header p {{
        color: #E0E7FF !important;
        font-size: 1.0rem;
        padding: 0 10px;
    }}

    /* 파일 업로더 디자인 커스텀 */
    div[data-testid="stFileUploader"] {{
        border: 2px dashed {header_bg};
        border-radius: 10px;
        padding: 30px;
        background-color: {card_bg};
        text-align: center;
    }}
    
    /* 결과 박스 디자인 */
    .result-box {{
        background-color: {card_bg};
        padding: 25px;
        border-radius: 10px;
        border: 1px solid {border_color};
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .disclaimer {{
        text-align: center;
        font-size: 0.8rem;
        color: {sub_text} !important;
        margin-top: 20px;
        margin-bottom: 50px;
    }}
    </style>
    
    <div class="custom-header">
        <div style="font-size: 3rem; margin-bottom: 10px;">📖 ♡ 文</div>
        <h1>Parenting Without Borders</h1>
        <p>Global Parenting Support<br>Translate & Guide Homework in Your Language</p>
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
            label_visibility="collapsed"
        )
    with col2:
        st.markdown(f"**🟢 Homework Language (Input)**")
        target_lang = st.selectbox(
            "Select Homework Language", 
            ["Dutch", "English", "German", "French", "Spanish", "Chinese", "Auto Detect"], 
            label_visibility="collapsed"
        )

    st.markdown("---")
    
    # [변경] 탭 제거 -> 단일 업로드 버튼으로 통합
    # 모바일에서는 이 버튼 하나로 '사진 찍기'와 '앨범 선택'이 모두 가능합니다.
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
        
        submit = st.button("🚀 Translate & Explain", type="primary", use_container_width=True)

        if submit:
            status_text = st.empty()
            status_text.info("🤖 AI Tutor is analyzing... Please wait.")
            
            # 언어 텍스트 정리 (괄호 제거 등)
            p_lang_clean = parent_lang.split("(")[0].strip()
            
            # 함수 호출
            response_text = get_gemini_response(image, p_lang_clean, target_lang)
            
            # 결과 출력
            if "Error:" in response_text:
                status_text.error("❌ Error Occurred")
                st.error(response_text)
            else:
                status_text.success("✅ Analysis Complete!")
                st.markdown("### 🎉 Analysis Result")
                st.markdown(f'<div class="result-box">{response_text}</div>', unsafe_allow_html=True)
                
                # 면책 조항
                st.markdown("""
                    <div class="disclaimer">
                        ⚠️ <b>Disclaimer:</b> This service uses Artificial Intelligence. 
                        Results may be inaccurate or incomplete. Please use this for reference only 
                        and verify important information with school materials.
                    </div>
                """, unsafe_allow_html=True)