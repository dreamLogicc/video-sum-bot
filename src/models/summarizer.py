from huggingface_hub import InferenceClient


class Summarizer:

    def __init__(self, hf_key: str, model: str = "Qwen/Qwen2.5-72B-Instruct"):
        self.client = InferenceClient(api_key=hf_key)
        self.model = model

    def set_model(self, model: str):
        self.model = model

    def summarize(self, text: str) -> str:
        messages = [
            {
                "role": "system",
                "content": """Вы комментатор. Ваша задача – написать отчет по тексту.
                    Когда вам представят текст, придумайте интересные вопросы и ответьте на каждый из них.
                    После этого объедините всю информацию и напишите отчет в Markdown формате."""
            },

            {"role": "user",
             "content":
                 f"""
                    # Текст:
                    {text}

                    # Инструкции:
                    ## Подведем итоги:
                    Ясным и кратким языком изложите ключевые моменты и темы, представленные в тексте.

                    ## Интересные вопросы:
                    Придумайте три отдельных и заставляющих задуматься вопроса, которые можно задать по поводу содержания текста. По каждому вопросу:
                    - После «Q:» опишите проблему
                    - После «А:» дайте подробное объяснение проблемы, затронутой в вопросе.

                    ## Написать отчет
                    Используя краткое содержание текста и ответы на интересующие вопросы, создайте подробный отчет в формате Markdown
                 """
             },
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return completion.choices[0].message.content
