import speech_recognition as sr
import pyttsx3
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import requests
import webbrowser
import wikipedia
import os
from pygame import mixer

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
            if is_playing:
                return ""  # Игнорируем нераспознанный ввод во время воспроизведения
            speak("Sorry, I didn't catch that. Please repeat.")
            return ""
        except sr.RequestError:
            speak("Sorry, there was an issue with speech recognition.")
            return ""

# Загрузка модели DialoGPT и токенизатора
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Функция для поиска фактов в Wikipedia
def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return "There are multiple results for this query. Can you please specify?"
    except wikipedia.exceptions.PageError:
        return "I couldn't find any information on that topic."

# Функция для поиска изображений (Unsplash API)
def search_image(query):
    access_key = "your_api_key"  # Замените на ваш ключ API Unsplash
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={access_key}"
    response = requests.get(url).json()
    if response.get("results"):
        image_url = response["results"][0]["urls"]["small"]
        print(f"Image URL: {image_url}")  # Выводим ссылку в консоль
        return f"Here is an image related to {query}."
    else:
        return "I couldn't find any images for that query."

# Функция для поиска видео на YouTube
def search_youtube_video(query):
    api_key = "your_api_key"  # Замените на ваш ключ YouTube API
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={api_key}&type=video"
    response = requests.get(url).json()
    if response.get("items"):
        video_id = response["items"][0]["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"YouTube Video URL: {video_url}")  # Выводим ссылку в консоль
        return f"Here is a YouTube video related to {query}."
    else:
        return "I couldn't find any videos for that query."

# Инициализация Pygame для воспроизведения музыки
mixer.init()

# Глобальные переменные для управления музыкой
music_folder = "C://your_folder_path"  # Укажите путь к папке с музыкой
current_song_index = -1
is_playing = False

# Функция для поиска музыки по названию
def find_music_by_name(query):
    global current_song_index
    files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
    matches = []

    # Поиск файлов, содержащих ключевые слова из запроса
    for i, file in enumerate(files):
        if query.lower() in file.lower():
            matches.append((i, file))  # Сохраняем индекс и имя файла

    if not matches:
        return None  # Ничего не найдено

    # Если найдено несколько совпадений, выбираем первое
    current_song_index = matches[0][0]
    return os.path.join(music_folder, matches[0][1])

# Функция для воспроизведения музыки
def play_music(query):
    global is_playing

    # Остановка музыки
    if "stop" in query or "pause" in query:
        if is_playing:
            mixer.music.pause()
            is_playing = False
            return "Music paused."
        else:
            return "No music is currently playing."

    # Переключение на следующую песню
    if "next" in query:
        return play_next_song()

    # Удаление команды "play music" из запроса
    query = query.replace("play music", "").replace("play song", "").strip()

    # Поиск музыки по названию
    song_path = find_music_by_name(query)
    if song_path:
        mixer.music.load(song_path)
        mixer.music.play()
        is_playing = True
        return f"Playing: {os.path.basename(song_path)}"
    else:
        return "I couldn't find any music matching your query."

# Функция для воспроизведения следующей песни
def play_next_song():
    global current_song_index, is_playing
    files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
    if not files:
        return "No music files found."

    current_song_index += 1
    if current_song_index >= len(files):
        current_song_index = 0  # Вернуться к первой песне

    next_song_path = os.path.join(music_folder, files[current_song_index])
    mixer.music.load(next_song_path)
    mixer.music.play()
    is_playing = True
    return f"Playing next song: {files[current_song_index]}"

# Основной цикл работы ассистента
def main():
    global is_playing
    speak("Hello! I'm your voice assistant. How can I help you?")
    
    while True:
        query = listen()

        # Если музыка играет, игнорируем все запросы, кроме команд управления музыкой
        if is_playing and not any(cmd in query for cmd in ["next song", "stop music", "play music"]):
            continue

        if "exit" in query or "bye" in query:
            speak("Goodbye!")
            break

        # Проверка на математическое выражение
        if any(op in query for op in ["+", "-", "*", "/"]):
            try:
                result = eval(query)
                speak(f"The answer is {result}.")
                continue
            except Exception:
                speak("I'm sorry, I couldn't calculate that.")
                continue

        # Поиск фактов в Wikipedia
        if any(word in query for word in ["what is", "who is", "tell me about", "explain"]):
            response = search_wikipedia(query)
            speak(response)
            continue

        # Поиск изображений
        if "find image of" in query or "show me an image of" in query:
            keyword = query.replace("find image of", "").replace("show me an image of", "").strip()
            response = search_image(keyword)
            speak(response)
            continue

        # Поиск видео на YouTube
        if "find video of" in query or "show me a video of" in query:
            keyword = query.replace("find video of", "").replace("show me a video of", "").strip()
            response = search_youtube_video(keyword)
            speak(response)
            continue

        # Управление музыкой
        if "play music" in query or "play song" in query:
            response = play_music(query)
            speak(response)
            continue

        if "stop music" in query or "pause music" in query:
            response = play_music("stop")
            speak(response)
            continue

        if "next song" in query:
            response = play_music("next")
            speak(response)
            continue

        # Текстовый диалог
        inputs = tokenizer(query + tokenizer.eos_token, return_tensors="pt", truncation=True, max_length=512)
        response_ids = model.generate(
            inputs["input_ids"],
            max_length=512,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            top_p=0.95,
            top_k=50,
            temperature=0.8,
            do_sample=True
        )
        response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
        new_response = response.split(tokenizer.eos_token)[-1].strip()

        # Убираем повторяющийся текст пользователя из ответа
        new_response = new_response.replace(query, "").strip()

        # Фильтрация некорректных ответов
        if not new_response or len(new_response.split()) < 2:  # Минимум 2 слова
            new_response = "I'm sorry, I didn't fully understand that. Could you clarify?"

        speak(new_response)

if __name__ == "__main__":
    main()