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
        st.error("API 키를 찾을 수 없습니다. secrets.toml 파일을 확인해주세요.")
        st.stop()

genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

st.set_page_config(
    page_title="Super Parents: Heroes Across Languages",
    page_icon="🦸",
    layout="centered"
)

# ==========================================
# [AI Function] - 문제 해결 능력 대폭 강화
# ==========================================
def get_gemini_response(image, parent_lang, homework_lang):
    prompt = f"""
    ### Role & Objective
    You are the **Lead AI Tutor** for the app "Super Parents".
    **Your #1 Priority is ACCURACY and CLARITY.** A parent, who speaks **[ {parent_lang} ]**, needs to understand this homework (originally in **[ {homework_lang} ]**) perfectly to teach their child.

    ### 🔍 Analysis Instructions (CRITICAL)
    1.  **Solve EVERY problem** visible in the image. Do not skip questions.
    2.  If the image contains text/reading, summarize the content and explain the key points.
    3.  If the image contains math, show the **step-by-step calculation process**, not just the final answer.
    4.  **The final output must be written entirely in {parent_lang} (except for the praise phrase).**

    ### Output Format (Strictly Follow This Order)
    
    1. **📝 Detailed Solution & Explanation (Key Section)**
       - **This is the most important part.**
       - Provide the correct answer for each question found in the image.
       - Explain *WHY* that is the answer.
       - If it is a math problem, break it down: "Step 1 -> Step 2 -> Answer".
       - If there are multiple questions, number them (1, 2, 3...) clearly.

    2. **🗣️ Coaching Guide (How to Teach)**
       - Now that the parent knows the answer, tell them *how* to explain it to the child.
       - Provide specific questions to ask the child to spark their thinking (e.g., "Why do you think this formula applies here?").

    3. **📚 Essential Vocabulary (Table Format)**
       - [Word in Homework Language] | [Meaning in {parent_lang}] | [Pronunciation]

    4. **💖 Praise the Hero (The Magic Moment)**
       - Provide a specific praise sentence in **the language of the homework** (so the child understands).
       - **Format:**
         - 🗨️ **Say to Child:** "[Insert Praise in Homework Language]"
         - 🗣️ **Pronunciation:** "[Write how to say it using {parent_lang} alphabet]"
         - 🧠 **Meaning:** "[Meaning in {parent_lang}]"

    ### Tone & Style
    - **In Section 1 (Solution):** Precise, Logical, Academic yet easy to understand.
    - **In Section 2 & 4 (Coaching/Praise):** Encouraging, Warm, Supportive.
    - Use clear Markdown with bold text for answers.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        # 이미지 처리 방식은 리스트로 감싸는 것이 안전합니다.
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
    st.markdown("Developed with Google Gemini 2.5 Flash")

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
        background-color: {card_bg}; padding: 25px; border-radius: 12px;
        border: 1px solid {border_color};
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
</style>

<div class="custom-header">
    <div style="font-size: 3rem; margin-bottom: 10px;">🦸‍♂️ ♡ 🦸‍♀️</div>
    <h1>Super Parents<br>Heroes Across<br> Languages</h1>
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
            status_text.info("🤖 AI is preparing your coaching guide...It may take 30 seconds...")
            
            p_lang_clean = parent_lang.split("(")[0].strip()
            response_text = get_gemini_response(image, p_lang_clean, target_lang)
            
            if "Error:" in response_text:
                status_text.error("❌ Error Occurred")
                st.error(response_text)
            else:
                status_text.success("✅ Ready to teach!")
                st.markdown("### 🎉 Your Coaching Guide")
                
                # 결과 박스 표시
                st.markdown(f'<div class="result-box">{response_text}</div>', unsafe_allow_html=True)
                
                st.markdown("""
                    <div style="text-align: center; font-size: 0.75rem; color: #6B7280; margin-top: 30px; margin-bottom: 50px;">
                        ⚠️ <b>Disclaimer:</b> This tool supports parents but does not replace teachers.
                    </div>
                """, unsafe_allow_html=True)