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
    # 로컬 테스트 시 에러 방지를 위해 임시 처리 (배포 시엔 Secrets 사용 필수)
    # st.secrets가 없을 경우를 대비해 직접 입력하거나 에러 처리
    try:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
    except:
        # 배포 전 로컬 테스트를 위해 임시 키를 넣을 수 있는 곳
        # API_KEY = "여기에_API_키를_넣으세요" 
        st.error("API 키를 찾을 수 없습니다. Streamlit Cloud의 Secrets 설정을 확인해주세요.")
        st.stop()

genai.configure(api_key=API_KEY)

# 모델 설정 (2.5 버전이 아직 API에 없을 경우 1.5로 자동 대체하는 로직은 복잡하므로, 우선 1.5 Flash 권장)
# 만약 2.5가 안 되면 "gemini-1.5-flash"로 변경해주세요.
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
    sub_text = "#9CA3AF"
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

    /* 탭 스타일링 */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        background-color: {card_bg};
        border-radius: 5px;
        padding: 0 20px; 
        border: 1px solid {border_color};
    }}
    
    /* 파일 업로더 및 카메라 인풋 스타일 */
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
    
    # [수정됨] 탭을 사용하여 파일 업로드와 카메라 기능을 분리
    tab1, tab2 = st.tabs(["📁 Upload Image", "📸 Take Photo"])
    
    image_data = None # 최종적으로 분석할 이미지를 담을 변수

    with tab1:
        uploaded_file = st.file_uploader("Choose an image from gallery", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            image_data = uploaded_file

    with tab2:
        camera_file = st.camera_input("Take a picture directly")
        if camera_file is not None:
            image_data = camera_file

    # 이미지가 (파일이든 카메라든) 들어왔을 때 실행
    if image_data is not None:
        image = Image.open(image_data)
        
        # 탭 안에 이미지가 중복으로 보이지 않게 결과창 위에만 미리보기 표시
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