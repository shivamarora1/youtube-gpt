from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st
import time
import re

if 'chat_input_disabled' not in st.session_state:
    st.session_state.chat_input_disabled = True

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


def get_youtube_video_id(url):
    match = re.search(r'[?&]v=([^&]+)', url)
    return match.group(1) if match else None


def valid_yt_link_entered(yt_link):
    st.session_state.chat_input_disabled = False
    st.session_state.yt_link_txt = yt_link
    st.session_state.side_bar_error = ""

    # * fetching summary and adding it.
    result = fetch_yt_transcription(yt_link)
    st.session_state.chat_messages = [{"role": "assistant", "content": result}]


def invalid_yt_link_entered():
    st.session_state.chat_input_disabled = True
    st.session_state.yt_link_txt = ""
    st.session_state.side_bar_error = "Youtube link is not valid."
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Enter Youtube video link in left side bar..."}]


def enter_youtube_link():
    yt_link = st.session_state['yt_link']
    if is_valid_youtube_url(yt_link):
        valid_yt_link_entered(yt_link)
    else:
        invalid_yt_link_entered()


def fetch_yt_transcription(yt_link):
    result = YouTubeTranscriptApi.get_transcript(
        get_youtube_video_id(yt_link))
    overall_txt = ""
    for item in result:
        overall_txt = overall_txt+" "+item['text']
    return overall_txt


def ask_yt_gpt(query):
    time.sleep(15)
    return f"The answer for {query} is Blah Blah Blah Blah Blah Blah"


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


if prompt := st.chat_input("Please enter Youtube video link..." if st.session_state.chat_input_disabled else "Ask question...",
                           key="txt_msg", disabled=st.session_state.chat_input_disabled):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_messages.append({"role": "user", "content": prompt})

    # ! send prompt here to backend for processing.
    response = ask_yt_gpt(prompt)

    with st.chat_message("assistant"):
        # ! after receiving the result store it in history and display it to user.
        st.write_stream(streamed_response_generator(response))
    st.session_state.chat_messages.append(
        {"role": "assistant", "content": response})


# Download transcription and show its summary.
# Disable chat input.
# Summarization
