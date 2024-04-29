import botocore.exceptions
from llm import prompt_llm
import streamlit as st
import botocore
from utils import is_valid_youtube_url, streamed_response_generator, fetch_yt_transcription, summarize, logger, bedrock_client, highlight_nouns, yt_transcription_error, MAX_DURATION_SECONDS
from vector_db import generate_embed_and_store,search_from_collection


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
    msg = ""
    # * fetching summary and adding it.
    try:
        summary = fetch_and_summarize_yt_transcription(yt_link)
        summary_h = f"Here is summary of :red[Youtube] video: \n {summary}"
        msg = summary_h
        generate_embed_and_store(summary)

        st.session_state.chat_input_disabled = False
        st.session_state.yt_link_txt = yt_link
        st.session_state.side_bar_error = ""
    except Exception as e:
        logger.exception(e)
        msg = "Apologies, an unforeseen hiccup 🌧️ has transpired. \n Please endeavor to reconnect ⚡ later at your convenience."
    finally:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": msg}]


def invalid_yt_link_entered(error_msg):
    st.session_state.chat_input_disabled = True
    st.session_state.yt_link_txt = ""
    st.session_state.side_bar_error = error_msg
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Enter Youtube video link in left side bar..."}]


def enter_youtube_link():
    yt_link = st.session_state['yt_link']
    if is_valid_youtube_url(yt_link):
        if error_msg := yt_transcription_error(MAX_DURATION_SECONDS, yt_link):
            invalid_yt_link_entered(error_msg)
        else:
            valid_yt_link_entered(yt_link)
    else:
        invalid_yt_link_entered("Youtube link is not valid.")


@st.cache_data
def fetch_and_summarize_yt_transcription(yt_link):
    transcription = fetch_yt_transcription(yt_link)
    summary = summarize(transcription)
    highlighted_nouns = highlight_nouns(summary)
    return highlighted_nouns

@st.cache_data
def ask_yt_gpt(query):
    try:
        query_result = search_from_collection(query)
        
        # b_client = bedrock_client()
        # result = prompt_llm(b_client, query)
        result = query_result
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

    st.write(
        ":red[*] Videos longer than **30 minutes** are currently not supported.")

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
    response = ask_yt_gpt(prompt)

    with st.chat_message("assistant"):
        st.write_stream(streamed_response_generator(response))
    st.session_state.chat_messages.append(
        {"role": "assistant", "content": response})
