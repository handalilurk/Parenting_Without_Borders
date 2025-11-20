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
    page_title="Super Parents: Heroes Without Borders",
    page_icon="🦸",
    layout="centered"
)

# ==========================================
# [AI Function] 응답 생성 함수
# ==========================================
def get_gemini_response(image, parent_lang, homework_lang):
    """
    Generates a coaching guide using Gemini 2.5 Flash.
    """
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
# 2. 테마 및 디자인 (CSS & Header)
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

# [핵심 수정] HTML 코드를 왼쪽 끝으로 바짝 당겼습니다. (들여쓰기 없음)
st.markdown(f"""
<style>
    .stApp {{ background-color: {bg_color} !important; }}
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown li, .stMarkdown span {{ 
        color: {text_color} !important; 
    }}
    header {{visibility: hidden;}}
    
    .custom-header {{
        background-color: {header_bg};
        padding: 2rem 1rem;
        text-align: center;
        margin-top: -60px;
        margin-left: -5rem;
        margin-right: -5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    
    .custom-header h1 {{
        color: #FFFFFF !important;
        font-family: sans-serif;
        font-weight: 800;
        font-size: clamp(1.8rem, 6vw, 2.5rem);
        margin-top: 10px;
        margin-bottom: 15px;
        line-height: 1.2;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.2);
    }}

    div[data-testid="stFileUploader"] {{
        border: 2px dashed {header_bg};
        border-radius: 12px;
        padding: 20px;
        background-color: {card_bg};
        text-align: center;
    }}
    
    .result-box {{
        background-color: {card_bg};
        padding: 20px;
        border-radius: 12px;
        border: 1px solid {border_color};
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    
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
<p style="color: #FFD700 !important; font-size: 1.25rem !important; font-weight: 800 !important; margin-bottom: 10px !important; text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important; opacity: 1 !important;">
You remain your child's first and best teacher.
</p>
<p style="color: #FFFFFF !important; font-size: 1.0rem !important; font-weight: 500 !important; line-height: 1.5 !important; margin-top: 0 !important; opacity: 0.95 !important;">
Understand in your language, teach with confidence.<br>
Let your wisdom cross the language barrier.
</p>
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
            index=0, 
            label_visibility="collapsed"
        )
    with col2:
        st.markdown(f"**🟢 Homework Language (Input)**")
        target_lang = st.selectbox(
            "Select Homework Language", 
            ["Dutch", "English", "German", "French", "Spanish", "Chinese", "Auto Detect"], 
            index=0, 
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
                status_text.success("✅ Ready to teach! (코칭 준비 완료!)")
                st.markdown("### 🎉 Your Coaching Guide")
                st.markdown(f'<div class="result-box">{response_text}</div>', unsafe_allow_html=True)
                
                st.markdown("""
                    <div class="disclaimer">
                        ⚠️ <b>Disclaimer:</b> This tool supports parents but does not replace teachers.
                        Results by AI may vary. Always verify with official school materials.
                    </div>
                """, unsafe_allow_html=True)