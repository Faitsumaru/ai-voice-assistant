import speech_recognition as sr
import pyttsx3
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Инициализация движка для синтеза речи
engine = pyttsx3.init()

# Настройка голоса (опционально)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Выбор мужского голоса (по умолчанию)

# Функция для озвучивания текста
def speak(text):
    if text.strip():  # Проверяем, что текст не пустой
        print(f"Assistant: {text}")
        engine.say(text)
        engine.runAndWait()
    else:
        speak("Sorry, I couldn't generate a response.")

# Функция для распознавания речи
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-US")
            print(f"User: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please repeat.")
            return ""
        except sr.RequestError:
            speak("Sorry, there was an issue with speech recognition.")
            return ""

# Загрузка модели DialoGPT и токенизатора
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Функция для выполнения математических операций
def calculate_expression(expression):
    try:
        result = eval(expression)  # Выполняем математическое выражение
        return str(result)
    except Exception:
        return "I'm sorry, I couldn't calculate that."

# Основной цикл работы ассистента
def main():
    speak("Hello! I'm your voice assistant. How can I help you?")
    
    # Инициализация истории диалога
    chat_history_ids = None  # Будем хранить тензор истории диалога
    max_length = 512         # Максимальная длина последовательности для модели

    while True:
        query = listen()

        if "exit" in query or "bye" in query:
            speak("Goodbye!")
            break

        # Проверка на математическое выражение
        if any(op in query for op in ["+", "-", "*", "/"]):
            response = calculate_expression(query)
            speak(response)
            continue

        # Токенизация нового запроса
        new_input_ids = tokenizer.encode(query + tokenizer.eos_token, return_tensors="pt")

        # Объединение нового запроса с историей диалога
        if chat_history_ids is None:
            chat_history_ids = new_input_ids
        else:
            chat_history_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)

        # Обрезка истории до максимальной длины
        if chat_history_ids.shape[-1] > max_length:
            chat_history_ids = chat_history_ids[:, -max_length:]

        # Генерация ответа
        response_ids = model.generate(
            chat_history_ids,
            max_length=max_length,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            top_p=0.92,
            top_k=50,
            temperature=0.7,
            do_sample=True
        )

        # Декодирование ответа
        response = tokenizer.decode(response_ids[0], skip_special_tokens=True)

        # Извлечение только нового ответа (без повторения истории)
        new_response = response[len(tokenizer.decode(chat_history_ids[0], skip_special_tokens=True)):]
        new_response = new_response.strip()

        # Фильтрация некорректных ответов
        if not new_response or len(new_response.split()) < 2:
            new_response = "I'm sorry, I didn't understand that."

        # Обновление истории диалога
        chat_history_ids = response_ids

        # Ответ пользователю
        speak(new_response)

if __name__ == "__main__":
    main()