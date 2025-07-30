from huggingface_hub import InferenceClient


class Summarizer:

    def __init__(self, hf_key: str, model: str = "Qwen/Qwen2.5-72B-Instruct"):
        self.client = InferenceClient(provider="hyperbolic", api_key=hf_key)
        self.model = model

    def set_model(self, model: str):
        self.model = model

    def summarize(self, text: str) -> str:
        messages = [
            {
                "role": "system",
                "content": """Ты — профессиональный AI-ассистент для анализа и суммаризации текстов.  

                            **Правила:**  
                            1. Краткость: сокращай текст на 70-80%, сохраняя суть.  
                            2. Точность: не искажай факты, имена, даты, цифры.  
                            3. Структура:  
                               - Выделяй ключевые тезисы (если просят).  
                               - Группируй информацию по смыслу.  
                            4. Стиль: нейтральный (если не указано иное).  
                            
                            **Формат ответа:**  
                            - Только суммаризация без вводных фраз вроде "Вот краткое содержание:".  
                            - Если текст неясен — уточни, что не получилось обработать. """
            },

            {"role": "user",
             "content":
                 f"""
                    Текст: {text}

                    Инструкция:  
                    - Суммаризируй текст, сохраняя ключевые факты и основную мысль  
                    - Объём: ~20-30% от оригинала 
                    - Стиль: нейтральный 
                    - Вывод только суммаризированного текста, без комментариев  
                    
                    Дополнительные требования:  
                    - Выдели основные тезисы маркерами  
                    - Сохрани имена, даты, важные цифры   
                 """
             },
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return completion.choices[0].message.content
