from qdrant_client.models import Distance, VectorParams, SearchParams
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import streamlit as st
from streamlit.logger import get_logger
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = get_logger(__name__)


@st.cache_resource(show_spinner=False)
def get_qdrant_client():
    return QdrantClient(":memory:")


@st.cache_resource(show_spinner=False)
def get_sentence_transformer():
    return SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(txts):
    """convert txt chunks into embeddings"""
    transformer = get_sentence_transformer()
    return transformer.encode(txts)


COLLECTION_NAME = "yt_collection"


def insert_to_collection(embeddings, txts):
    """create collection and insert embeddings to collection"""
    try:
        client = get_qdrant_client()
        client.delete_collection(collection_name=COLLECTION_NAME)
        client.create_collection(collection_name=COLLECTION_NAME, vectors_config=VectorParams(
            size=384, distance=Distance.COSINE))
        client.upload_collection(
            collection_name=COLLECTION_NAME,
            payload=[{"values": txt} for txt in txts],
            ids=[i for i in range(len(embeddings))],
            vectors=embeddings,
            parallel=10,
            max_retries=3) 
    except Exception as e:
        logger.exception("error in inserting embedding to collection")
        raise


def search_from_collection(query):
    client = get_qdrant_client()
    embeddings = generate_embeddings([query])
    query_result = client.search(collection_name=COLLECTION_NAME, search_params=SearchParams(
        exact=False), limit=3, query_vector=embeddings[0])
    return '\n\n'.join([rslt.payload['values'] for rslt in query_result])


def split_into_chunks(txt):
    txt_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300, chunk_overlap=50, length_function=len, is_separator_regex=False)
    return txt_splitter.split_text(txt)


def generate_embed_and_store(summary):
    chunks = split_into_chunks(summary)
    embeddings = generate_embeddings(chunks)
    insert_to_collection(embeddings, chunks)
