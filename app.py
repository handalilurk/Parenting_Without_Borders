import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. 기본 설정
# ==========================================
if "GOOGLE_API_KEY" in st.secrets:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    try:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
    except:
        st.error("API 키를 찾을 수 없습니다.")
        st.stop()

genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash" 

st.set_page_config(
    page_title="Super Parents: Heros Across Languages",
    page_icon="🦸",
    layout="centered"
)

# ==========================================
# [AI Function]
# ==========================================
def get_gemini_response(image, parent_lang, homework_lang):
    prompt = f"""
    ### Role & Objective
    You are the **Lead AI Tutor** for the app "Super Parents".
    Your goal is to empower a parent who speaks **[ {parent_lang} ]** to perfectly understand and guide their child's homework (originally in **[ {homework_lang} ]**).

    ### Instructions
    Analyze the provided homework image and generate a structured guide.
    **The final output must be written entirely in {parent_lang}.**

    ### Output Format
    1. **🎯 Homework Overview (1-Sentence Summary)**
    2. **🗣️ Coaching Guide (Conversational Scripts)**
    3. **📝 Essential Vocabulary (Table Format)**
    4. **💡 Teacher's Pro Tip**

    ### Tone & Style
    - Professional, supportive, and encouraging.
    - Use clear Markdown.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        content_input = [prompt, image[0]] if isinstance(image, list) else [prompt, image]
        response = model.generate_content(content_input)
        return response.text
    except Exception as e:
        return f"Error occurred during analysis: {e}"

# ==========================================
# 2. 테마 및 디자인 (절대 깨지지 않는 방식)
# ==========================================

with st.sidebar:
    st.header("⚙️ Settings")
    theme_mode = st.selectbox("Theme Mode", ["Light Mode (Default)", "Dark Mode"])
    st.divider()
    st.markdown("Developed with Google Gemini")

if "Dark" in theme_mode:
    bg_color = "#0E1117"
    text_color = "#FAFAFA"
    card_bg = "#262730"
    border_color = "#374151"
    header_bg = "#312E81" 
else:
    bg_color = "#F3F4F6"
    text_color = "#1F2937"
    card_bg = "#FFFFFF"
    border_color = "#E5E7EB"
    header_bg = "#4F46E5" 

# ------------------------------------------------------------------
# [수정 핵심] HTML 변수를 들여쓰기 없이 왼쪽 끝에 붙여서 정의
# 코드가 조금 못생겨 보여도, 이렇게 해야 화면에 코드가 노출되지 않습니다.
# ------------------------------------------------------------------
header_html = f"""
<style>
    .stApp {{ background-color: {bg_color} !important; }}
    .stMarkdown, p, h1, h2, h3, li, span {{ color: {text_color}; }}
    header {{visibility: hidden;}}
    
    .custom-header {{
        background-color: {header_bg};
        padding: 2.5rem 1rem;
        text-align: center;
        margin-top: -60px;
        margin-left: -5rem;
        margin-right: -5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    .custom-header h1 {{
        color: #FFFFFF !important;
        font-family: sans-serif; font-weight: 800; font-size: 2.2rem;
        margin-bottom: 15px; line-height: 1.2;
    }}
    .gold-text {{
        color: #FFD700 !important; font-size: 1.2rem; font-weight: 800;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }}
    .white-text {{
        color: #FFFFFF !important; font-size: 1.0rem; font-weight: 400; opacity: 0.95;
    }}
    
    div[data-testid="stFileUploader"] {{
        border: 2px dashed {header_bg}; border-radius: 12px; padding: 20px;
        background-color: {card_bg}; text-align: center;
    }}
    .result-box {{
        background-color: {card_bg}; padding: 20px; border-radius: 12px;
        border: 1px solid {border_color};
    }}
</style>

<div class="custom-header">
    <div style="font-size: 3rem; margin-bottom: 10px;">🦸‍♂️ ♡ 🦸‍♀️</div>
    <h1>Super Parents<br>Heros Across<br> Languages</h1>
    <p style="margin-bottom: 10px;">
        <span class="gold-text">No barrier beats a parent’s love.</span>
    </p>
    <p>
        <span class="white-text">Understand in your language, teach with confidence.<br>Children may speak differently, <br>but they listen with their hearts.</span>
    </p>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)


# ==========================================
# 3. 메인 화면
# ==========================================

with st.container():
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**🟣 Parent Language**")
        parent_lang = st.selectbox(
            "Select Parent Language", 
            [
                "English", "Korean (한국어)", "Arabic (العربية)", "Turkish (Türkçe)",
                "Spanish (Español)", "Portuguese (Português)", "Dutch (Nederlands)",
                "French (Français)", "German (Deutsch)", "Chinese (中文)",
                "Japanese (日本語)", "Polish (Polski)", "Russian (Русский)",
                "Thai (ภาษาไทย)", "Vietnamese (Tiếng Việt)"
            ], 
            label_visibility="collapsed"
        )
    with col2:
        st.markdown(f"**🟢 Homework Language**")
        target_lang = st.selectbox(
            "Select Homework Language", 
            ["Dutch", "English", "German", "French", "Spanish", "Chinese", "Auto Detect"], 
            label_visibility="collapsed"
        )

    st.markdown("---")
    
    st.markdown("### 📸 Upload Homework")
    st.caption("Tap 'Browse files' below to take a photo or choose from gallery.")
    
    image_data = st.file_uploader(
        "Upload Image or Take Photo", 
        type=["jpg", "png", "jpeg"], 
        label_visibility="collapsed"
    )

    if image_data is not None:
        image = Image.open(image_data)
        
        st.markdown("### Preview")
        st.image(image, caption="Uploaded Homework", use_column_width=True)
        
        st.markdown("###") 
        
        submit = st.button("🚀 Activate Super Parent Mode", type="primary", use_container_width=True)

        if submit:
            status_text = st.empty()
            status_text.info("🤖 AI is preparing your coaching guide...")
            
            p_lang_clean = parent_lang.split("(")[0].strip()
            response_text = get_gemini_response(image, p_lang_clean, target_lang)
            
            if "Error:" in response_text:
                status_text.error("❌ Error Occurred")
                st.error(response_text)
            else:
                status_text.success("✅ Ready to teach!")
                st.markdown("### 🎉 Your Coaching Guide")
                st.markdown(f'<div class="result-box">{response_text}</div>', unsafe_allow_html=True)
                
                st.markdown("""
                    <div style="text-align: center; font-size: 0.75rem; color: #6B7280; margin-top: 30px; margin-bottom: 50px;">
                        ⚠️ <b>Disclaimer:</b> This tool supports parents but does not replace teachers.
                    </div>
                """, unsafe_allow_html=True)