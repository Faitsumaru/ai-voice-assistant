import pyttsx3

# Инициализация движка
engine = pyttsx3.init()

# Настройка голоса (опционально)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Функция для озвучивания текста
def speak(text):
    print(f"Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

# Проверка работы
speak("Hello, dude")