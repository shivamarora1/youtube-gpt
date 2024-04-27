import re
import time
from youtube_transcript_api import YouTubeTranscriptApi
import botocore
import boto3
import streamlit as st
from llm import prompt_llm
from streamlit.logger import get_logger

logger = get_logger(__name__)


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
        query = f"""Summarize following Youtube video transcription: 
        {transcription}"""
        logger.info("prompt %s", query)
        result = prompt_llm(b_client, query)
        return result
    except botocore.exceptions.ClientError as error:
        logger.error("error in calling bedrock: ", str(error))
        return "Error in summarizing video. Pls try again"
    except Exception as e:
        logger.error("error in calling bedrock: ", str(error))
        return "Error in summarizing video. Pls try again"
