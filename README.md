# **_Voice Assistant with Neural Networks (DialoGPT)_**

## About
This project demonstrates a voice assistant built using Python and powered by the DialoGPT neural network model for natural language processing.  
The assistant uses speech recognition to listen to user queries, processes them using the DialoGPT model, and generates spoken responses using text-to-speech synthesis.  
It is designed to handle conversational dialogue in English.

---

### Key Features:
* **Speech Recognition** : Utilizes Google Speech-to-Text API for accurate English speech recognition.
* **Natural Language Processing** : Employs the DialoGPT model from Hugging Face's Transformers library for generating context-aware responses.
* **Text-to-Speech** : Uses `pyttsx3` for offline text-to-speech synthesis.
* **Context Awareness** : Maintains conversation history to provide coherent and contextually relevant responses.
* **Customizable** : Supports adjustments to voice, speed, and other parameters for a personalized experience.
* **Multimedia Integration** :
  * Searches for images using **Unsplash API**.
  * Finds videos on **YouTube** via YouTube Data API.
  * Plays local music files with playback controls (`play`, `pause`, `next`).
* **Mathematical Operations** : Performs simple arithmetic calculations.
* **Wikipedia Integration** : Provides summaries of topics using Wikipedia API.

> version: Mar 2025, created by Gleb 'Faitsuma' Kiryakov

---

## Project Structure

### Code Overview
1. **Speech Recognition** :
    * The program uses the `speech_recognition` library to capture audio input from the microphone.
    * Google Speech-to-Text API is employed for English speech recognition with the `language="en-US"` parameter.

2. **Model Architecture** :
    * The **DialoGPT-medium** model is loaded using Hugging Face's `transformers` library.
    * A tokenizer preprocesses user input into tokenized sequences, which are fed into the model for response generation.
    * The model supports multi-turn conversations by maintaining a history of dialogues (`chat_history_ids`).

3. **Text-to-Speech** :
    * The `pyttsx3` library is used to synthesize and vocalize the generated responses.
    * Supports system voices, with options to customize voice, speed, and volume.

4. **Multimedia Integration** :
    * **Unsplash API**: Searches for images based on user queries.
    * **YouTube Data API**: Finds and provides links to relevant videos.
    * **Music Playback**: Plays local MP3 files with playback controls (`play`, `pause`, `next`).

5. **Utility Functions** :
    * `listen()`: Captures and processes user speech.
    * `speak()`: Converts text responses into spoken output.
    * `main()`: Manages the main loop of the assistant, handling user input and generating responses.

---