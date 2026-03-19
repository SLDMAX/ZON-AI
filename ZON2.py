import streamlit as st
from groq import Groq
from PIL import Image

# --- 🖼️ LOGO එක පැහැදිලිව LOAD කිරීම ---
def get_favicon():
    try:
        # image_2.png එක විවෘත කිරීම
        img = Image.open("image_2.png")
        # Favicon එකක් සඳහා හොඳම ප්‍රමාණය (32x32 හෝ 64x64) ලෙස Resize කිරීම
        img = img.resize((64, 64)) 
        return img
    except:
        return "🤖"

favicon_img = get_favicon()

# --- පිටුවේ සැකසුම් (Page Config) ---
st.set_page_config(
    page_title="ZON AI - ZON Corporation",
    page_icon=favicon_img, # මෙතනට Resize කළ පින්තූරය ලබා දුන්නා
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 🚀 CUSTOM CSS (Premium Look) ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #101010 0%, #1e3a5f 100%);
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    .title-font {
        font-size: 55px;
        font-weight: 800;
        color: #00d2ff;
        text-shadow: 0 0 15px #00d2ff, 0 0 30px #00d2ff;
        margin-bottom: 5px;
        letter-spacing: 2px;
    }
    .subtitle-font {
        color: #b0b0b0;
        font-size: 16px;
        text-align: right;
    }
    .stButton>button {
        background-color: transparent;
        color: #00d2ff;
        border: 2px solid #00d2ff;
        border-radius: 25px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #00d2ff;
        color: black;
        box-shadow: 0 0 20px #00d2ff;
    }
    .stChatMessage {
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 🎨 SIDEBAR SETUP ---
with st.sidebar:
    st.image("image_2.png", use_container_width=True) 
    st.markdown('<p class="title-font" style="font-size: 30px; text-align: center;">ZON AI</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.write("Developed by **ZON Corporation**")
    st.info("සිංහල සහ ඉංග්‍රීසි භාෂා දෙකෙන්ම උදව් කිරීමට සූදානම්.")
    st.markdown("---")
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("©️ 2024 ZON Corporation.")

# --- 🚀 GROQ API CONNECTION ---
client = Groq(api_key="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")

# --- 🚀 CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main UI Title
col1, col2 = st.columns([4, 1])
col1.markdown('<p class="title-font">ZON AI</p>', unsafe_allow_html=True)
col2.markdown('<p class="subtitle-font">Developed by<br><b>ZON Corporation</b></p>', unsafe_allow_html=True)
st.markdown("---")

# --- 🎨 CHAT HISTORY පෙන්වීම (අතීත පණිවිඩ වලටත් Logo එක පෙන්වයි) ---
for message in st.session_state.messages:
    current_avatar = "image_2.png" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=current_avatar):
        st.markdown(message["content"])

# --- 🚀 නව පණිවිඩ ලබා ගැනීම (Chat Input) ---
if prompt := st.chat_input("ZON AI ගෙන් ඕනෑම දෙයක් අසන්න..."):
    # User පණිවිඩය Save කිරීම සහ පෙන්වීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # AI පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant", avatar="image_2.png"):
        try:
            response_container = st.empty()
            full_response = ""

            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are ZON AI, a helpful assistant created by ZON Corporation. Answer in the language the user uses."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=True,
            )
            
            # Typewriter effect එක පෙන්වීම
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    response_container.markdown(full_response + "▌")
            
            response_container.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")