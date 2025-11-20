import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. 기본 설정
# ==========================================

# [중요] API 키 설정
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    try:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
    except:
        # 로컬 테스트용
        # API_KEY = "여기에_API_키를_넣으세요" 
        st.error("API 키를 찾을 수 없습니다. Streamlit Cloud의 Secrets 설정을 확인해주세요.")
        st.stop()

genai.configure(api_key=API_KEY)

# 모델 설정
MODEL_NAME = "gemini-2.5-flash" 

st.set_page_config(
    page_title="Parenting Without Borders",
    page_icon="♡",
    layout="centered"
)

# ==========================================
# 2. 테마 설정 및 CSS
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
    # [수정 1] 다크모드 면책조항 글씨를 더 밝은 회색으로 변경 (가독성 확보)
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

    /* [수정 2] 모바일 친화적 탭 스타일링 (Segmented Control) */
    
    /* 탭 컨테이너: 간격 없애기 */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: transparent;
        padding-bottom: 10px;
    }}

    /* 기본 탭 (선택 안 된 상태): 흐리게 표시 */
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        width: 100%; /* 모바일에서 꽉 차게 */
        background-color: {card_bg};
        border: 1px solid {border_color};
        border-radius: 8px;
        color: {text_color};
        font-weight: 400;
        flex-grow: 1; /* 화면 너비에 맞춰 늘어남 */
        justify-content: center; /* 텍스트 가운데 정렬 */
    }}
    
    /* 선택된 탭 (Active): 진한 색으로 꽉 채워서 확실하게 표시 */
    .stTabs [aria-selected="true"] {{
        background-color: {header_bg} !important; /* 브랜드 컬러 배경 */
        color: white !important; /* 흰색 글씨 */
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* 살짝 떠 있는 느낌 */
    }}

    div[data-testid="stFileUploader"], div[data-testid="stCameraInput"] {{
        border: 2px dashed {header_bg};
        border-radius: 10px;
        padding: 20px;
        background-color: {card_bg};
    }}
    
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
        <p>Upload a photo of your child's homework.<br>We'll translate and help you guide them.</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 3. 메인 화면
# ==========================================

with st.container():
    
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
    
    # 탭 생성
    tab1, tab2 = st.tabs(["📁 Upload Image", "📸 Take Photo"])
    
    image_data = None

    with tab1:
        st.caption("Choose an image from your gallery") # 안내 문구 추가
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
        if uploaded_file is not None:
            image_data = uploaded_file

    with tab2:
        st.caption("Take a picture of the homework directly") # 안내 문구 추가
        camera_file = st.camera_input("Take Photo", label_visibility="collapsed")
        if camera_file is not None:
            image_data = camera_file

    # 이미지 처리 로직
    if image_data is not None:
        image = Image.open(image_data)
        
        st.markdown("### Preview")
        st.image(image, caption="Homework Image", use_column_width=True)
        
        st.markdown("###") 
        
        submit = st.button("🚀 Translate & Explain", type="primary", use_container_width=True)

        if submit:
            status_text = st.empty()
            status_text.info("🤖 AI Tutor is analyzing... Please wait.")
            
            try:
                p_lang = parent_lang.split("(")[0].strip()
                t_lang = target_lang
                
                real_prompt = f"""
                **Role:** You are a helpful AI tutor for parents.
                **Goal:** Analyze the homework image (Language: {t_lang}) and explain it in **{p_lang}**.
                
                **Output Format:**
                1. **Overview**: What is this homework about? (Subject, Topic)
                2. **Detailed Explanation**: Translate and explain the questions step-by-step in {p_lang}.
                3. **Vocabulary**: Key words table ({t_lang} -> {p_lang}).
                4. **Coaching Tip**: How should the parent ask the child? (Provide sentences in {t_lang} and {p_lang}).
                
                **Constraint:** The final explanation must be in **{p_lang}**.
                """
                
                model = genai.GenerativeModel(MODEL_NAME)
                response = model.generate_content([real_prompt, image])
                
                status_text.success("✅ Analysis Complete!")
                
                st.markdown("### 🎉 Analysis Result")
                st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
                
                # 면책 조항
                st.markdown("""
                    <div class="disclaimer">
                        ⚠️ <b>Disclaimer:</b> This service uses Artificial Intelligence. 
                        Results may be inaccurate or incomplete. Please use this for reference only 
                        and verify important information with school materials.
                    </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                status_text.error("❌ Error Occurred")
                st.error(f"Details: {e}")