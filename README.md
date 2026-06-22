# 🎓 University Lecture Summarizer

I built this project to tackle a classic engineering student problem: trying to transcribe or review fast-paced, 60-minute technical lectures. Instead of re-listening to massive audio files for hours, this tool lets you drop a lecture recording (`.mp3` or `.wav`), extracts the core formulas and concepts, and translates them directly into a target language of your choice (like Hindi or Tamil).

The entire system is written from scratch using **HTML, CSS, and vanilla JavaScript** for the UI dashboard, paired with a lightweight **Python Flask backend** to handle multipart file streams and talk safely to the Gemini API.

---

## 🏗️ Core Architecture & System Flow

To ensure security, the application splits the presentation layer from the core server logic. This keeps the private API credentials completely safe on your local machine rather than exposing them to the client browser.

* **Frontend:** A responsive dark-themed dashboard built with clean CSS flexbox rules. JavaScript intercepts the submit trigger, builds a `FormData` object to stream the heavy audio binary, handles dynamic loading state indicators, and inserts the generated markdown elements into the DOM without triggering a browser refresh.
* **Backend:** A localized Flask API listening on port 5001. It catches the incoming audio stream, commits it to a local temporary cache file, uploads it to the Gemini storage layer, requests a localized technical summary template via the model, and cleanly purges the temporary files from both local storage and the cloud.

---

## 🛠️ Tech Stack & File Blueprint

* **Frontend:** Semantic HTML5, Custom CSS3 Layouts, Vanilla JavaScript (Asynchronous Fetch APIs)
* **Backend:** Python 3.14, Flask, Flask-CORS (handles cross-origin request policies between local ports)
* **AI Core:** Google GenAI SDK (`gemini-2.5-flash`)
* **Environment Configuration:** Python-Dotenv

---

## 🏃‍♂️ Local Installation & Blueprint

### 1. Configure the Runtime Environment
Set up your clean Python environment and install the required dependencies:
```bash
python3 -m venv .venv
./.venv/bin/pip install flask flask-cors google-genai python-dotenv