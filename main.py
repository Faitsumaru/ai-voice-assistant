import speech_recognition as sr
import pyttsx3
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import wikipedia

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

# Функция для поиска фактов в Wikipedia
def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return "There are multiple results for this query. Can you please specify?"
    except wikipedia.exceptions.PageError:
        return "I couldn't find any information on that topic."

# Основной цикл работы ассистента
def main():
    speak("Hello! I'm your voice assistant. How can I help you?")
    
    # Инициализация истории диалога
    chat_history = []  # Будем хранить историю в виде списка строк
    max_length = 512   # Максимальная длина последовательности для модели
    max_history = 4    # Максимальное количество обменов в истории (2 пользователя + 2 ассистента)

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

        # Проверка на запрос фактов
        if any(word in query for word in ["what is", "who is", "tell me about", "explain"]):
            response = search_wikipedia(query)
            speak(response)
            continue

        # Добавляем запрос пользователя в историю
        chat_history.append(query)

        # Создаем входной текст для модели (ограничиваем историю до max_history)
        input_text = tokenizer.eos_token.join(chat_history[-max_history:]) + tokenizer.eos_token

        # Токенизация входного текста
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=max_length)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        # Генерация ответа
        response_ids = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=max_length,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            top_p=0.95,  # Увеличиваем разнообразие ответов
            top_k=50,
            temperature=0.8,  # Делаем ответы более естественными
            do_sample=True
        )

        # Декодирование ответа
        full_response = tokenizer.decode(response_ids[0], skip_special_tokens=True)

        # Извлечение только нового ответа
        new_response = full_response.split(tokenizer.eos_token)[-1].strip()

        # Убираем повторяющийся текст пользователя из ответа
        for user_input in chat_history[-max_history:]:
            new_response = new_response.replace(user_input, "").strip()

        # Фильтрация некорректных ответов
        if not new_response or len(new_response.split()) < 2:  # Минимум 2 слова
            new_response = "I'm sorry, I didn't fully understand that. Could you clarify?"

        # Добавляем ответ модели в историю
        chat_history.append(new_response)

        # Ответ пользователю
        speak(new_response)

if __name__ == "__main__":
    main()