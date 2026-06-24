from flask import Flask, render_template, redirect, url_for, jsonify, request, session
import sqlite3
import cv2
import numpy as np
from deepface import DeepFace
import traceback
import openai  # Added OpenAI for chatbot functionality
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key')

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Global variable to store the detected emotion
detected_emotion = None

# Initialize the database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Initialize DB when the app starts
init_db()

# Route to render create account page
@app.route("/create_account", methods=['GET'])
def create_account_page():
    return render_template('create_account.html')

# Route to handle account creation
@app.route("/create_account", methods=['POST'])
def create_account():
    username = request.form['new-username']
    password = request.form['new-password']
    confirm_password = request.form['confirm-password']

    if not username or not password:
        return jsonify({"error": "Username and password are required!"}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match!"}), 400

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return redirect(url_for('page1'))  # Redirect to login page after successful account creation
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists!"}), 400
    finally:
        conn.close()

# Route to render login page
@app.route("/", methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate user credentials
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = username  # Store username in session
            return redirect(url_for('login_page'))  # Redirect to login.html
        else:
            return jsonify({"error": "Invalid credentials!"}), 401

    return render_template('page1.html')

# Route for login.html
@app.route("/login", methods=['GET'])
def login_page():
    if 'username' in session:
        return render_template('login.html', username=session['username'])
    else:
        return redirect(url_for('page1'))  # Redirect to login page if not logged in

# Route for emotion detection page
@app.route("/emotion_detection")
def emotion_detection_page():
    if 'username' in session:
        return render_template('camera.html')  # Render the camera.html page for the browser
    else:
        return redirect(url_for('page1'))  # Redirect to login if not logged in

# Route to process video frames for emotion detection
@app.route("/analyze_emotion", methods=['POST'])
def analyze_emotion():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        file = request.files['image']
        npimg = np.frombuffer(file.read(), np.uint8)

        if npimg.size == 0:
            return jsonify({"error": "Invalid image data"}), 400

        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({"error": "Could not decode image"}), 400

        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        if isinstance(analysis, list):
            analysis = analysis[0]

        emotions = {emotion: float(value) for emotion, value in analysis["emotion"].items()}
        return jsonify({
            "dominant_emotion": analysis["dominant_emotion"],
            "emotions": emotions
        })
    except Exception as e:
        print("Error occurred:", traceback.format_exc())
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

# Route to store the detected emotion
@app.route("/set_emotion", methods=["POST"])
def set_emotion():
    global detected_emotion
    data = request.json
    detected_emotion = data.get("emotion")
    return jsonify({"success": True})

# Route to retrieve the detected emotion
@app.route("/get_emotion", methods=["GET"])
def get_emotion():
    global detected_emotion
    return jsonify({"emotion": detected_emotion})

# Chatbot route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        global detected_emotion
        emotion_context = f"The user seems to be feeling {detected_emotion}. Provide empathetic suggestions for their well-being."

        if detected_emotion == "happy":
            emotion_context += " Suggest fun or joyful activities they might enjoy."

        # Call OpenAI GPT for a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": emotion_context},
                {"role": "user", "content": user_message},
            ],
        )

        bot_reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": bot_reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

# Logout route
@app.route("/logout")
def logout():
    session.pop('username', None)  # Clear the session
    return redirect(url_for('page1'))

@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")  # Render chatbot.html

if __name__ == '__main__':
    app.run(debug=True, port=5001)
