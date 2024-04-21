import streamlit as st
import time


def streamed_response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


with st.sidebar:
    st.text_input(label=":red[Youtube] video link", key="yt_link",
                  placeholder="https://www.youtube.com/watch?v=TSzYstGdvDQ")
    st.button(label="Submit", key="submit_yt_link",
              disabled=False, type="primary")
    st.video(data="https://www.youtube.com/watch?v=TSzYstGdvDQ")

st.header("Youtube GPT 🤖")
st.markdown("##### 🗣️ Converse with 📼 Youtube videos")

st.divider()

with st.chat_message("assistant"):
    response = st.write_stream(streamed_response_generator(
        "Enter Youtube video link in left side bar..."))

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

# Verify Youtube video link on button click.
# Error message.
# Button hide when valid video found.
