# Vidify 🎥🤖
**Automate short-form video creation from Reddit posts — with TTS, animated (bouncy) captions, random “satisfying” background clips, and one-click YouTube uploads.**

---

## ✨ What it does
- **Fetches Reddit posts** (configurable: subreddit, count, type)
- **Generates audio (TTS)** + **word-timed captions** with a bouncy effect
- **Cuts & stitches** random 3s background clips to match audio duration
- **Renders full videos** via FFmpeg/MoviePy
- **Stores & lists videos** (via DB + storage layer)
- **Uploads to YouTube** with **Google OAuth**
- **Simple dashboard** (React + Vite) to generate, list, delete, and upload videos

---

## 🧱 Architecture (high-level)

```
frontend (React/Vite)  <---->  backend (Flask)
                                 ├── Reddit fetch (components/post_fetch.py)
                                 ├── TTS + captions (modules/audio_gen.py, modules/captions.py)
                                 ├── Video render (modules/video_gen.py)
                                 ├── YouTube upload (modules/yt_uploader.py, components/youtube_auth.py)
                                 └── DB / storage helpers (video_db.py, db.py)
```

---

## 🧰 Tech Stack

**Backend**
- **Flask** (REST API)
- **FFmpeg**, **MoviePy**, **pydub** (rendering)
- **Google OAuth + YouTube Data API** (uploading)
- **Azure Blob/CosmosDB** (see `video_db.py`)

**Frontend**
- **React** + **Vite**

---


## ⚙️ Setup

### 1) Backend (Flask)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt

# Set your Flask app (if needed)
export FLASK_APP=app.py
export FLASK_ENV=development

flask run  # runs on http://127.0.0.1:5000
```

### 2) Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev  # runs on http://localhost:5173 by default
```
