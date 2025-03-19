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

## How to Use

### Prerequisites
* Install the required dependencies:
```
pip install speechrecognition pyttsx3 transformers torch pygame wikipedia requests
```

### Running the Code
1. Clone this repository:
```
git clone https://github.com/Faitsumaru/ai-voice-assistant
cd ai-voice-assistant
```
2. Set up API keys:
    * Replace `"your_api_key"` for _YouTube_ and `"your_api_key"` for _Unsplash_ in the code with your actual API keys.
    * Ensure the `music_folder` variable points to your local folder containing MP3 files.

3. Run the script:
```
python main.py
```
4. Interact with the Assistant:
    * Speak into your microphone to ask questions or give commands.
    * The assistant will respond verbally and maintain context throughout the conversation.

---

## Example Interaction

Here are some examples of how the assistant interacts with users:

* **Basic Introduction** :
    * User says: "Hello!"
    * Assistant responds: "Hello! How can I assist you today?"

* **Name Inquiry** :
    * User says: "What is your name?"
    * Assistant responds: "My name is Assistant. Nice to meet you!"

* **Joke Request** :
    * User says: "Tell me a joke."
    * Assistant responds: "Why don't scientists trust atoms? Because they make up everything!"

* **Weather Inquiry** :
    * User says: "What is the weather like today?"
    * Assistant responds: "I'm not sure about the current weather, but I hope it's sunny and pleasant where you are!"

* **Mathematical Question** :
    * User says: "What is 5 plus 7?"
    * Assistant responds: "The answer is 12."

* **Philosophical Question** :
    * User says: "What is the meaning of life?"
    * Assistant responds: "That's a deep question! Some say it's 42, while others believe it's about finding purpose and happiness."

* **Personalized Conversation** :
    * User says: "How was your day?"
    * Assistant responds: "I don't experience days like humans, but I'm always here and ready to help you!"

* **Goodbye Interaction** :
    * User says: "Goodbye!"
    * Assistant responds: "Goodbye! Have a great day!"

* **Multi-Turn Dialogue** :
    * User says: "Do you like movies?"
    * Assistant responds: "I don't watch movies, but I can recommend some if you're interested!"
    * User says: "Sure, recommend one."
    * Assistant responds: "If you enjoy science fiction, I recommend 'Interstellar.' It's thought-provoking and visually stunning!"

* **Creative Storytelling** :
    * User says: "Tell me a short story."
    * Assistant responds: "Once upon a time, there was a curious robot who wanted to explore the world. Along the way, it learned about kindness, friendship, and the beauty of nature."

* **Multimedia Requests** :
    * User says: "Find image of a cat."
    * Assistant responds: "Here is an image related to a cat."
    * Console logs the URL:
      ```
      Image URL: [https://images.unsplash.com/cat-photo](https://images.unsplash.com/photo-1633638924593-77d118795863?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3MjU0NzV8MHwxfHNlYXJjaHwxfHxhJTIwY2F0fGVufDB8fHx8MTc0MjM4MzE4OXww&ixlib=rb-4.0.3&q=80&w=400)
      ```

    * User says: "Find video of John Cena trashes the WWE"
    * Assistant responds: "Here is a YouTube video related to John Cena trashes the wwe"
    * Console logs the URL:
      ```
      YouTube Video URL: https://www.youtube.com/watch?v=ExQYm6gintE
      ```

* **Music Playback** :
    * User says: "Play music Skillet Hero."
    * Assistant responds: "Playing: Skillet - Hero.mp3"
    * User says: "Next song."
    * Assistant responds: "Playing next song: Bohemian Rhapsody.mp3"

---