import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. 기본 설정
# ==========================================

# [중요] API 키 가져오기
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("API 키가 설정되지 않았습니다. Streamlit Secrets를 확인하세요.")
    st.stop()

genai.configure(api_key=API_KEY)

# [사용자 요청] 모델 버전 변경 (2.5가 아직 출시 전이라면 에러가 날 수 있으니 확인 필요)
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
    # [추가 1] 사이드바 하단에도 짧은 경고 문구 추가
    st.caption("⚠️ AI can make mistakes. Please verify important information.")

if "Dark" in theme_mode:
    bg_color = "#0E1117"
    text_color = "#FAFAFA"
    card_bg = "#262730"
    border_color = "#374151"
    header_bg = "#312E81"
    sub_text = "#9CA3AF" # 면책 조항용 회색 텍스트 색상
else:
    bg_color = "#F3F4F6"
    text_color = "#1F2937"
    card_bg = "#FFFFFF"
    border_color = "#E5E7EB"
    header_bg = "#4F46E5"
    sub_text = "#6B7280" # 면책 조항용 회색 텍스트 색상

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

    div[data-testid="stFileUploader"] {{
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

    /* [추가 2] 면책 조항 스타일 (작고 흐린 글씨) */
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
    
    uploaded_file = st.file_uploader("Take a photo or upload", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
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
                
                # [추가 3] 분석 결과 아래에 면책 조항 표시
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