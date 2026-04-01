# 🚀 Automated YouTube Content System (Hindi) – Free & Ready to Use

A fully automated YouTube content creation system that generates and uploads **YouTube Shorts (6 days/week)** and **Long videos (1 day/week)** in **Hindi**. It runs daily at **9:00 AM IST** and can also be triggered manually via a **Telegram bot**. All tools used are **free** with no credit card required.

## ✨ Features

- ✅ **Daily Scheduler** – Uploads automatically at 9:00 AM IST  
  - **Monday–Saturday** → YouTube Shorts (30–60 sec, 9:16)  
  - **Sunday** → Long video (5–10 min, 16:9)  
- ✅ **Trending Topic Fetcher** – Uses Google Trends (India)  
- ✅ **AI Script Generator** – Groq API (Llama 3) – Hindi scripts with hook in first 3 seconds (Shorts) or storytelling (Long)  
- ✅ **Ultra‑Realistic Hindi Male Voice** – Edge TTS (free, no API key)  
- ✅ **Stock Media** – Pexels API (videos & images, free tier)  
- ✅ **Video Editing** – MoviePy + FFmpeg, with subtitles (optional)  
- ✅ **Thumbnail Generator** – Simple text overlay on a stock image  
- ✅ **Metadata Generation** – SEO‑optimized title, description, tags in Hindi  
- ✅ **YouTube Upload** – YouTube Data API v3 (free tier, OAuth2)  
- ✅ **Telegram Bot** – Manual trigger with `/shorts` or `/long` – super fast generation in background  
- ✅ **Caching & Error Handling** – Reduces API calls, retries on failure, full logging  

## 🧱 Architecture Overview

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Scheduler     │      │   Telegram Bot   │      │   Core Engine   │
│ (daily at 9AM)  │      │ (manual trigger) │      │ (video creation)│
└────────┬────────┘      └────────┬─────────┘      └────────┬────────┘
         │                        │                         │
         └────────────────────────┼─────────────────────────┘
                                  │
                     ┌────────────▼────────────┐
                     │   generate_video()      │
                     │   (scheduler.py)        │
                     └────────────┬────────────┘
                                  │
        ┌─────────────┬───────────┼───────────┬─────────────┐
        ▼             ▼           ▼           ▼             ▼
  Script Gen     TTS Gen     Media Fetch   Video Edit    Upload
   (Groq)       (Edge TTS)    (Pexels)     (MoviePy)    (YouTube)
```

## 📋 Prerequisites

- **Python 3.8+** installed  
- **FFmpeg** installed and in system PATH (required by MoviePy)  
  - Ubuntu/Debian: `sudo apt install ffmpeg`  
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH  
  - macOS: `brew install ffmpeg`  
- A **Telegram account** (to create the bot)  
- **Groq API key** – free from [console.groq.com](https://console.groq.com)  
- **Pexels API key** – free from [pexels.com/api](https://www.pexels.com/api/)  
- **Google Cloud Project** with YouTube Data API v3 enabled and OAuth 2.0 credentials (desktop app)

## 🛠️ Setup Instructions

### 1. Clone the repository and install dependencies

```bash
git clone https://github.com/yourusername/youtube-automation.git
cd youtube-automation
pip install -r requirements.txt
```

### 2. Create folder structure

The code expects the following directories (created automatically if missing):

```
youtube-automation/
├── shorts/       # Shorts videos will be saved here
├── long/         # Long videos will be saved here
├── audio/        # Temporary audio files
├── cache/        # API response cache
├── output/       # (optional) unused
├── .env
├── client_secrets.json   # YouTube OAuth2 credentials
└── ... (all .py files)
```

### 3. Set up API keys and tokens

Create a `.env` file in the project root with:

```
GROQ_API_KEY=your_groq_api_key
PEXELS_API_KEY=your_pexels_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

#### YouTube OAuth2 credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable **YouTube Data API v3**.
3. Create **OAuth 2.0 Client ID** for **Desktop application**.
4. Download the JSON file and rename it to `client_secrets.json`.
5. Place it in the project root.

#### Telegram Bot
1. Open Telegram and start a chat with [@BotFather](https://t.me/botfather).
2. Send `/newbot` and follow the instructions to create a new bot.
3. Copy the bot token and paste it into `.env` as `TELEGRAM_BOT_TOKEN`.

### 4. First‑time YouTube authentication

Run `uploader.py` once to generate the `token.json` file:

```bash
python uploader.py
```

A browser window will open asking you to log in to your Google account and grant permission. After successful authorization, `token.json` will be created. You can close the script after that.

## 🚀 Running the System

### Start the full system (scheduler + Telegram bot)

```bash
python main.py
```

- The scheduler will wait for 9:00 AM IST and run the daily task.
- The Telegram bot will start and respond to commands.

### Run only once (for testing)

```bash
python scheduler.py   # Generates video based on current day and uploads
```

### Stop the system

Press `Ctrl+C` in the terminal to stop both the scheduler and the bot.

## 🤖 Telegram Bot Commands

| Command               | Description |
|-----------------------|-------------|
| `/start`              | Shows welcome message with available commands |
| `/shorts [topic]`     | Generates a YouTube Short (30‑60 sec) on the given topic (or trending topic if omitted) |
| `/long [topic]`       | Generates a long video (5‑10 min) on the given topic (or trending topic) |
| `/status`             | Checks if a video is currently being generated |
| `/cancel`             | Placeholder – currently does not interrupt a running job (due to threading limitations) |

When a video is generated, the bot replies with the final YouTube link.

## ⚙️ Customisation

- **Script language**: Change `script_generator.py` prompt to generate in any language.
- **Voice**: Edit `tts_generator.py` to use different Edge TTS voices (e.g., `hi-IN-SwaraNeural` for female).
- **Thumbnail font**: Download a Devanagari font (e.g., Noto Sans Devanagari) and place in the root; the code will try to use it.
- **Video duration**: Adjust `create_shorts` and `create_long_video` by changing audio duration – the video will automatically match the audio length.

## 📝 Important Notes

- **Free tier limits**:
  - Groq: 30 requests/minute for Llama 3 8B, 10 for 70B. The system includes retries.
  - Pexels: 200 requests/hour – cache reduces calls.
  - YouTube API: 10,000 units/day – enough for daily uploads.
  - Edge TTS: unlimited, no quota.
- **Subtitles**: Currently a single line at the bottom for the first 200 characters of the script. For full subtitles, you would need to split the script into timed sentences.
- **Media queries**: The script uses the topic directly for Pexels searches. For better results, you may translate Hindi topics to English using a library like `googletrans`.
- **Error handling**: All failures are logged in `automation.log`. The system will retry script generation (up to 3 times) and abort if critical steps fail.

## 🧪 Troubleshooting

- **FFmpeg not found**: Make sure FFmpeg is installed and in your PATH. Test with `ffmpeg -version`.
- **YouTube upload fails**: Check that `token.json` is valid and the account has permission to upload. Delete `token.json` and re‑run `uploader.py` to re‑authorise.
- **Telegram bot doesn't respond**: Verify the token in `.env` and that the bot is not blocked. Ensure your Python script has internet access.
- **No trending topic**: `pytrends` may occasionally fail; the system falls back to a default topic ("आज की खबर").

## 📄 License

This project is open‑source and free to use. No warranty is provided.

---

**Enjoy automating your YouTube channel in Hindi!** If you encounter any issues, feel free to open an issue or contribute improvements.
