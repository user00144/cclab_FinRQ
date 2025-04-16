from utils.api import API_KEY, HF_TOKEN
from config import MODEL_NAME
from openai import OpenAI
import torch
from transformers import pipeline
from huggingface_hub import login

HF_MODEL_DICT = {
    "llama" : "", # llama
    "phi" : "microsoft/phi-4" # phi-4 : 13b
}


if MODEL_NAME in ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o"] :
    client = OpenAI(api_key = API_KEY)
elif MODEL_NAME in ["llama", "phi"] :
    login(HF_TOKEN)
    client = pipeline("text-generation",
    model=HF_MODEL_DICT[MODEL_NAME],
    model_kwargs={"torch_dtype": "auto"},
    device_map="auto")


def request(system_define, prompt) :
    if MODEL_NAME in ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o"] :
        response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": system_define},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2048,
                    temperature=0
                )

        return response.choices[0].message.content
    elif MODEL_NAME in ["llama", "phi"] :
        messages=[
                        {"role": "system", "content": system_define},
                        {"role": "user", "content": prompt}
        ]
        outputs = client(messages, max_new_tokens = 2048)
        response = outputs[0]["generated_text"][-1]
        if MODEL_NAME == "phi" :
            return response["content"]
        else :
            return response