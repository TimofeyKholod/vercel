import time

from mistralai import Mistral

txt = "напиши код для работы с мистрал"
api_key = "LHsZNVrwBLFRvqVfDUQo4nCHS1l8nqSw"
client = Mistral(api_key=api_key)
t = time.time()
response = client.chat.complete(
    model="mistral-large-latest",
    messages=[
                {"role": "system", "content": "Ты голосовой помощник Джарвис. Отвечай по существу"},
                {"role": "user",
                 "content": f"Вопрос: {txt}. Отвечай на русском. Кратко и ответ только на поставленный вопрос"}
            ]
    ,temperature=0.7,
    stream=False
)
print(time.time()-t)
print(response.choices[0].message.content)
