# Youtube GPT: Converse with Youtube video
![resized_speed_up](https://github.com/shivamarora1/youtube-gpt/assets/28146775/0d5fb99d-b3f6-4e2e-a8bb-d12e515ec71f)

This [Streamlit](https://streamlit.io/) application helps you in summarizing YouTube videos, making it easier to digest content efficiently. Additionally, it allows users to pose follow-up questions related to the video, and the application generates pertinent responses, enhancing engagement and understanding.

### Steps to run on local:
---
1. Create and activate virtual environment
```
python3 -m venv .venv
source .venv
```
2. Download all dependencies
```
pip install -r requirements.txt
```
3. Run application
```
streamlit run main.py 
```

### App overview
---
1. Enter Youtube video link in left side bar.
2. Using Youtube Transcription api application will fetch transcriptions of Youtube video.
3. Fetched transcriptions are sent to `Mistral-7B-instruction` model for summarization.
4. Embeddings of transcriptions are generated using `all-MiniLM-L6-v2` model
5. Generated embeddings are stored in `Qdrant` in memory vector database.
6. When you follow question relevant similar Youtube video context is fetched from vector database and that context is sent to `Mistral-7B-instruction` model along with question.
7. `Mistral-7B-instruction` uses fetched background context and gives answer of asked question. 
<br><br>

    #### Limitations
    1. Youtube videos larger that 30 minutes length are not supported.
    2. Youtube video only in english language are only supported.

### Architecture diagram



ToDo:
- Architecture blog
- Make the summary according to the length of video. i.e if length is small then summary should be small but if length is big then summary should be big.
- LIKE Button (So that we can measure its accuracy)
- Video on LinkedIn

In Github application:
- Alive pipeline

Before making app public:
- Set alarm in AWS.

Limitation:
1. Chunking is not proper because we don't have information about the punctuation.
2. Eliminate incomplete summaries.

Depricate AI Youtube Summarizer in GPT Github.


