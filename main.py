import streamlit as st
import time
import re


if "yt_link_txt" not in st.session_state:
    st.session_state.yt_link_txt = ""

if "side_bar_error" not in st.session_state:
    st.session_state.side_bar_error = ""

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Enter Youtube video link in left side bar..."}]


def streamed_response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def is_valid_youtube_url(url):
    pattern = r'^(https?:\/\/)?(www\.)?(youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    return bool(re.match(pattern, url))


def enter_youtube_link():
    yt_link = st.session_state['yt_link']
    if is_valid_youtube_url(yt_link):
        st.session_state.yt_link_txt = yt_link
        st.session_state.side_bar_error = ""
    else:
        st.session_state.yt_link_txt = ""
        st.session_state.side_bar_error = "Youtube link is not valid."


with st.sidebar:
    st.text_input(label=":red[Youtube] video link", key="yt_link",
                  placeholder="https://www.youtube.com/watch?v=TSzYstGdvDQ")
    st.button(label="Submit", key="submit_yt_link",
              disabled=False, type="primary", on_click=enter_youtube_link)

    if st.session_state.side_bar_error:
        st.error(st.session_state.side_bar_error)

    if st.session_state.yt_link_txt:
        st.video(data=st.session_state.yt_link_txt)

st.header("Youtube GPT 🤖")
st.markdown("##### 🗣️ Converse with 📼 Youtube videos")

st.divider()

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask anything about Youtube video", key="txt_msg"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        st.write_stream(streamed_response_generator(prompt))
    st.session_state.chat_messages.append(
        {"role": "assistant", "content": prompt})


# Enable chat only when valid link is entered in box.
# When youtube video entered.
# Show waiting in chat window.
# Download transcription and show its summary.
# Summary should be first message.

