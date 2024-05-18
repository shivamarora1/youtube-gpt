import re
import nltk
import time
from youtube_transcript_api import YouTubeTranscriptApi
import botocore
import boto3
import streamlit as st
from llm import prompt_llm
from streamlit.logger import get_logger
import streamlit as st

logger = get_logger(__name__)

MAX_DURATION_SECONDS = 60*30


@st.cache_data(show_spinner=False)
def download_nltk_punkt():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
 
def bedrock_client():
    client = boto3.client(service_name='bedrock-runtime', region_name=st.secrets["AWS_DEFAULT_REGION"],
                          aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"], aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"])
    return client


def replace_text_in_square_brackets(text):
    pattern = r'\[([^\[\]]*)\]'

    def replace(match):
        return ''
    result = re.sub(pattern, replace, text)
    return result


def is_valid_youtube_url(url):
    pattern = r'^(https?:\/\/)?(www\.)?(youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    return bool(re.match(pattern, url))


def get_youtube_video_id(url):
    match = re.search(r'[?&]v=([^&]+)', url)
    return match.group(1) if match else None


def streamed_response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def fetch_yt_transcription(yt_link):
    result = YouTubeTranscriptApi.get_transcript(
        get_youtube_video_id(yt_link))
    overall_txt = ""
    for item in result:
        overall_txt = overall_txt+" "+item['text']
    overall_txt = replace_text_in_square_brackets(overall_txt)
    return overall_txt


def summarize(transcription):
    try:
        b_client = bedrock_client()
        query = f"""Summarize given Youtube video transcription. Summarization should not be more than 250 characters. Summarize should be in points. Highlights important keywords using tag.
Below is transcription: 
{transcription}"""
        logger.info(query)
        result = prompt_llm(b_client, query)
        return result
    except botocore.exceptions.ClientError as error:
        logger.error("error in calling bedrock: ", str(error))
        return "Error in summarizing video. Pls try again"
    except Exception as e:
        logger.error("error in calling bedrock: ", str(e))
        return "Error in summarizing video. Pls try again"


def ask_from_context(context, question):
    try:
        b_client = bedrock_client()
        query = f"""Considering below context:
{context}

Answer this question:
{question}"""
        result = prompt_llm(b_client, query)
        return result
    except botocore.exceptions.ClientError as error:
        logger.error("error in calling bedrock: ", str(error))
        return "Error in summarizing video. Pls try again"
    except Exception as e:
        logger.error("error in calling bedrock: ", str(e))
        return "Error in summarizing video. Pls try again"


def highlight_nouns(txt):
    spt = txt.split("\n")
    i = 0
    while i < len(spt):
        sent = spt[i]
        tagged_pos = nltk.pos_tag(nltk.word_tokenize(sent))
        nouns = [word for word, tag in tagged_pos if tag ==
                 "NNP" or tag == "NNPS"]
        for noun in nouns:
            sent = sent.replace(noun, f"**{noun}**", -1)
        spt[i] = sent
        i = i+1
    return ('\n').join(spt)


def yt_transcription_error(duration, yt_link):
    """will check if there is some error while getting 
    transcription for video duration should be in seconds"""
    try:
        result = YouTubeTranscriptApi.get_transcript(
            get_youtube_video_id(yt_link))
        total_duration = (result[len(result)-1]['start'] +
                          result[len(result)-1]['duration'])
        return f"Youtube video length should be less than {round(MAX_DURATION_SECONDS/60)} minutes" if total_duration > duration else ""
    except Exception as e:
        return str(e)
