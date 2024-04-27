import botocore.exceptions
from llm import prompt_llm
import streamlit as st
import botocore
from utils import is_valid_youtube_url, streamed_response_generator,fetch_yt_transcription,summarize,logger,bedrock_client


if 'chat_input_disabled' not in st.session_state:
    st.session_state.chat_input_disabled = True

if "yt_link_txt" not in st.session_state:
    st.session_state.yt_link_txt = ""

if "side_bar_error" not in st.session_state:
    st.session_state.side_bar_error = ""

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Enter Youtube video link in left side bar..."}]


def valid_yt_link_entered(yt_link):
    st.session_state.chat_input_disabled = False
    st.session_state.yt_link_txt = yt_link
    st.session_state.side_bar_error = ""

    # * fetching summary and adding it.
    summary = fetch_and_summarize_yt_transcription(yt_link)
    st.session_state.chat_messages = [
        {"role": "assistant", "content": summary}]


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

# ! Cache this
def fetch_and_summarize_yt_transcription(yt_link):
    transcription = fetch_yt_transcription(yt_link)
    summary = summarize(transcription)
    return summary

# ! cache this
def ask_yt_gpt(query):
    try:
        b_client = bedrock_client()
        result = prompt_llm(b_client, query)
        return result
    except botocore.exceptions.ClientError as error:
        logger.error("error in calling bedrock: ", str(error))
        return "Pls try again later. Error in AWS service"
    except Exception as e:
        logger.error("error in calling bedrock: ", str(error))
        return "Pls try again later."


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
