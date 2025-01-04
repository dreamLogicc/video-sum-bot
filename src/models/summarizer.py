from huggingface_hub import InferenceClient


class Summarizer:

    def __init__(self, hf_key: str, model: str ="Qwen/Qwen2.5-72B-Instruct"):
        self.client = InferenceClient(api_key=hf_key)
        self.model = model

    def set_model(self, model: str):
        self.model = model

    def summarize(self, text: str) -> str:
        messages = [
            {"role": "system", "content": "Ты — ИИ-помощник. Твоя задача - суммаризация текста"},
            {"role": "user", "content": 'Сократи текст, выдели основные моменты: ' + text},
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return completion.choices[0].message.content
