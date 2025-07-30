import requests
from huggingface_hub import InferenceClient


class Transcriber:
    def __init__(self, hf_key: str):
        self.API_URL = "https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3-turbo"
        self.headers = {
            "Authorization": f"Bearer {hf_key}",
        }

    def transcribe(self, filename: str) -> dict:
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(self.API_URL, headers={"Content-Type": "audio/wav", **self.headers}, data=data)
        return response.json()