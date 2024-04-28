import json
from streamlit.logger import get_logger

logger = get_logger(__name__)


def prompt_llm(bedrock_client, prompt):
    body = json.dumps({
        "prompt": f"<s>[INST]{prompt}[/INST]",
        "max_tokens": 250,
        "temperature": 1,
        "top_p": 0.7,
        "top_k": 50,
    })

    modelId = 'mistral.mistral-7b-instruct-v0:2'

    response = bedrock_client.invoke_model(body=body, modelId=modelId)

    response_body = json.loads(response.get('body').read())

    outputs = response_body.get('outputs')
    logger.info("output %s", json.dumps(outputs, indent=1))
    completions = [output["text"] for output in outputs]

    return ''.join(completions)
