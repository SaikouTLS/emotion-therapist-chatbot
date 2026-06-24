# Emotion-Aware Therapist Chatbot

A full-stack web application that uses real-time facial emotion detection to power an AI chatbot that responds with empathy based on how the user is feeling.

Built as a senior capstone project at Morgan State University.

---

## What It Does

1. The user logs in and opens the emotion detection page
2. Their webcam feed is analyzed in real time using DeepFace to detect facial emotions (happy, sad, angry, fearful, disgusted, surprised, neutral)
3. The detected emotion is passed as context to a GPT-3.5-powered chatbot
4. The chatbot responds with empathetic, emotion-aware suggestions tailored to the user's current state

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Emotion Detection | DeepFace, OpenCV, NumPy |
| AI Chatbot | OpenAI GPT-3.5 Turbo |
| Auth & Sessions | Flask sessions, SQLite |
| Frontend | HTML, CSS, JavaScript |

---

## Features

- User account creation and login with session management
- Live webcam emotion detection via browser (no desktop app needed)
- Real-time emotion confidence scores for 7 emotional states
- Emotion-context-aware AI chatbot responses
- Crisis support page accessible without login
- REST API endpoints for emotion analysis and chat

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/emotion-therapist-chatbot.git
cd emotion-therapist-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

```
OPENAI_API_KEY=your-openai-api-key-here
SECRET_KEY=any-random-string-here
```

### 4. Run the app

```bash
python app.py
```

Open your browser to `http://localhost:5001`

---

## Project Structure

```
project/
├── app.py                  # Flask backend, API routes
├── Emotion_Protoype.py     # Standalone webcam emotion detection script
├── requirements.txt
├── .env.example
├── static/
│   └── styles.css
└── templates/
    ├── page1.html          # Landing / login page
    ├── create_account.html
    ├── login.html          # Dashboard after login
    ├── camera.html         # Live emotion detection
    └── chatbot.html        # AI chat interface
```

---

## Requirements

- Python 3.8+
- Webcam
- OpenAI API key (get one at platform.openai.com)

---

## Course

COSC 458 – Morgan State University, Fall 2024
