import streamlit as st
from groq import Groq
import time

# --- පිටුවේ සැකසුම් (Page Config) ---
st.set_page_config(
    page_title="ZON AI - KD MUSIC",
    page_icon="image_2.png", # අපි කලින් හැදූ Logo එක මෙතනට දාන්න
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 🚀 CUSTOM CSS (පෙනුම ලස්සන කිරීමට) ---
st.markdown("""
<style>
    /* මුළු පිටුවේම පෙනුම */
    .stApp {
        background: linear-gradient(135deg, #101010 0%, #1e3a5f 100%); /* Blue-to-Black Gradient */
        color: white;
        font-family: 'Poppins', sans-serif;
    }

    /* ZON AI Title එක Neon Blue වලින් දිලිසීමට */
    .title-font {
        font-size: 55px;
        font-weight: 800;
        color: #00d2ff; /* Bright Cyan */
        text-shadow: 0 0 15px #00d2ff, 0 0 30px #00d2ff, 0 0 45px #00d2ff;
        margin-bottom: 5px;
        letter-spacing: 2px;
    }

    /* Subtitle සහ "Developed by..." */
    .subtitle-font {
        color: #b0b0b0;
        font-size: 16px;
        text-align: right;
    }

    /* Sidebar එකේ පෙනුම */
    .css-1d391kg { /* This might vary, better to use generic selectors */
        background-color: rgba(30, 30, 30, 0.9) !important;
        border-right: 1px solid #333;
    }

    /* Buttons ලස්සන කිරීමට */
    .stButton>button {
        background-color: transparent;
        color: #00d2ff;
        border: 2px solid #00d2ff;
        border-radius: 25px;
        padding: 10px 25px;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #00d2ff;
        color: black;
        border-color: #00d2ff;
        box-shadow: 0 0 20px #00d2ff;
    }

    /* Chat Messages ලස්සන කිරීමට */
    .stChatMessage {
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .stChatMessage.stAssistant {
        background-color: #262626;
        border-left: 5px solid #00d2ff;
    }
    .stChatMessage.stUser {
        background-color: #1e3a5f;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# --- 🎨 SIDEBAR SETUP ---
with st.sidebar:
    # ZON AI Logo එක පෙන්වීම
    st.image("image_2.png", use_container_width=True) # කලින් හදපු Logo File එකේ නම
    st.markdown('<p class="title-font" style="font-size: 30px; text-align: center;">ZON AI</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("Developed by **KD MUSIC**")
    st.info("මෙම AI සහායකයා ඔබට සිංහල සහ ඉංග්‍රීසි භාෂා දෙකෙන්ම උදව් කිරීමට සූදානම්.")
    st.markdown("---")

    # Options (උදා: Clear Chat)
    col1, col2 = st.columns(2)
    if col1.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    if col2.button("💡 About ZON"):
        st.toast("ZON AI is a personalized AI assistant powered by Groq and Llama technology.", icon="🤖")

    st.markdown("---")
    st.write("©️ 2024 KD MUSIC. All rights reserved.")

# --- 🚀 GROQ API CONNECTION ---
client = Groq(api_key=st.secrets["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"]) # Secrets හරහා API Key එක ලබා ගන්න

# --- 🚀 CHAT LOGIC ---

# Chat History එක තබා ගැනීමට
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main UI Area - Title
col1, col2 = st.columns([4, 1])
col1.markdown('<p class="title-font">ZON AI</p>', unsafe_allow_html=True)
col2.markdown('<p class="subtitle-font">Developed by<br><b>KD MUSIC</b></p>', unsafe_allow_html=True)
st.markdown("---")

# කලින් කළ කතාබස් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# පරිශීලකයාගෙන් ප්‍රශ්න ලබා ගැනීම
if prompt := st.chat_input("ZON AI ගෙන් ඕනෑම දෙයක් අසන්න..."):
    # පරිශීලකයාගේ පණිවිඩය Save කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        try:
            # Typewriter effect එකක් සඳහා placeholder එකක් හැදීම
            response_container = st.empty()
            full_response = ""
            
            # AI එකෙන් පිළිතුර ලබා ගැනීම (Stream=True)
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are ZON AI, a helpful assistant created by KD MUSIC. Answer in the language the user uses (Sinhala or English)."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=True, # Typewriter effect එකක් සඳහා මෙය True කරන්න
            )
            
            # Stream එක කියවලා Typewriter effect එකක් පෙන්වීම
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    response_container.markdown(full_response + "▌") # ▌ cursor එක පෙන්වයි
            
            # සම්පූර්ණ පිළිතුර පෙන්වීම
            response_container.markdown(full_response)
            # පිළිතුර Save කිරීම
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")
