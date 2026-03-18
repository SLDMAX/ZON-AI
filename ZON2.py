import streamlit as st
from groq import Groq

# 
client = Groq(api_key="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")

st.set_page_config(page_title="ZON", page_icon="🤖")
st.title("🤖 ZON ")

#
if "messages" not in st.session_state:
    st.session_state.messages = []

# 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI එකෙන් පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile", # ඉතා වේගවත් සහ නොමිලේ දෙන මාදිලියක්
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")