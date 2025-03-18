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
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

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

# Основной цикл работы ассистента
def main():
    speak("Hello! I'm your voice assistant. How can I help you?")
    
    # Инициализация истории диалога
    chat_history_ids = None

    while True:
        query = listen()

        if "exit" in query or "bye" in query:
            speak("Goodbye!")
            break

        # Токенизация входного запроса
        new_input_ids = tokenizer.encode(query + tokenizer.eos_token, return_tensors="pt")

        # Добавление нового запроса к истории диалога
        if chat_history_ids is None:
            chat_history_ids = new_input_ids
        else:
            chat_history_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)

        # Генерация ответа
        response_ids = model.generate(
            chat_history_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=2,
            top_p=0.92,
            top_k=50,
            temperature=0.7
        )

        # Декодирование ответа
        response = tokenizer.decode(response_ids[:, chat_history_ids.shape[-1]:][0], skip_special_tokens=True)

        # Обновление истории диалога
        chat_history_ids = response_ids

        # Ответ пользователю
        speak(response)

if __name__ == "__main__":
    main()