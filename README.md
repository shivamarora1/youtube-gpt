# youtube-gpt
Youtube GPT


3lit run script.py


1. Side bar Youtube Video Path.
2. Just bottom of that Video embed.
3. First message should be info.
4. After entering video. First there would be summarization and then Option would be enabled for chatting.

Inspiration: https://www.youtube.com/watch?v=JLVsFIXtvKE

Streaming looks cool.

* Breakdown large transcriptions into small one and send them in pieces. Considering context of LLM. But need to hard limit video may be 30 minutes.
* See AWS Bill
* Write a blog of setting up Mistral in AWS. Also write how we can use Cloudwatch to view its usage.

Feature:
- Mistral AI for summarization.
- Proper Nouns are highlighted.
- Supported upto 30 min video.

RAG:
- Breakdown and store them into in memory vector DB.
- Fetch it from in memory vector DB.
- Send retrieved context and question to LLM. 