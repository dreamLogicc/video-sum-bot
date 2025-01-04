import requests

class Transcriber:
    def __init__(self, hf_key: str):
        self.API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
        self.headers = {"Authorization": f"Bearer {hf_key}", "language": "ru"}

    def transcribe(self, filename: str) -> dict:

        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(self.API_URL, headers=self.headers, data=data)
        return response.json()