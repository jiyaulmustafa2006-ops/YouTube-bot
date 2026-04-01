from datetime import datetime
import os
from logger import logger
from script_generator import generate_script
from tts_generator import generate_audio
from media_fetcher import fetch_stock_videos, fetch_stock_images
from video_editor import create_shorts, create_long_video
from uploader import upload_video
from pytrends.request import TrendReq
import requests
from PIL import Image, ImageDraw, ImageFont

def get_trending_topic():
    pytrends = TrendReq(hl='hi-IN', tz=330)
    trending_searches = pytrends.trending_searches(pn='india')
    topic = trending_searches[0][0] if len(trending_searches) > 0 else "आज की खबर"
    return topic

def generate_thumbnail(topic, image_urls, output_path):
    if not image_urls:
        return None
    try:
        img_data = requests.get(image_urls[0]).content
        with open("temp_thumb.jpg", "wb") as f:
            f.write(img_data)
        img = Image.open("temp_thumb.jpg")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("NotoSansDevanagari-Regular.ttf", 40)
        except:
            font = ImageFont.load_default()
        draw.text((50, 50), topic, fill="white", font=font, stroke_width=2, stroke_fill="black")
        img.save(output_path)
        logger.info(f"Thumbnail generated: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Thumbnail generation failed: {e}")
        return None

def generate_video(topic=None, is_short=None, upload=True, progress_callback=None):
    if progress_callback:
        progress_callback("Starting video generation...")

    if is_short is None:
        today = datetime.now().strftime("%A")
        is_short = today != "Sunday"
    video_type = "Short" if is_short else "Long"
    logger.info(f"Generating {video_type} video on topic: {topic}")

    if topic is None:
        topic = get_trending_topic()
        if progress_callback:
            progress_callback(f"Trending topic: {topic}")

    if progress_callback:
        progress_callback("Generating script...")
    script = generate_script(topic, is_short=is_short)
    if not script:
        return {"status": "failed", "reason": "Script generation failed"}

    if progress_callback:
        progress_callback("Generating audio...")
    audio_dir = "audio"
    os.makedirs(audio_dir, exist_ok=True)
    audio_file = os.path.join(audio_dir, f"{topic.replace(' ', '_')}.mp3")
    audio_path = generate_audio(script, audio_file)
    if not audio_path:
        return {"status": "failed", "reason": "Audio generation failed"}

    if progress_callback:
        progress_callback("Fetching stock media...")
    orientation = "portrait" if is_short else "landscape"
    video_urls = fetch_stock_videos(topic, per_page=5, orientation=orientation)
    image_urls = fetch_stock_images(topic)

    if progress_callback:
        progress_callback("Creating video...")
    output_dir = "shorts" if is_short else "long"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
    subtitles = script[:200] if script else None
    if is_short:
        create_shorts(audio_path, video_urls, output_file, subtitles=subtitles)
    else:
        create_long_video(audio_path, video_urls, output_file, subtitles=subtitles)

    if progress_callback:
        progress_callback("Generating thumbnail...")
    thumbnail_path = output_file.replace(".mp4", "_thumb.jpg")
    thumbnail = generate_thumbnail(topic, image_urls, thumbnail_path)

    video_id = None
    if upload:
        if progress_callback:
            progress_callback("Uploading to YouTube...")
        title = f"{topic} | {'Shorts' if is_short else 'लॉन्ग वीडियो'}"
        description = f"इस वीडियो में जानिए {topic} के बारे में। {script[:300]}..."
        tags = [topic, "हिंदी", "trending", "viral"]
        if is_short:
            tags.append("#shorts")
        video_id = upload_video(output_file, title, description, tags, privacy_status="public")
        if progress_callback:
            progress_callback(f"Uploaded! https://youtu.be/{video_id}")

    return {
        "status": "success",
        "video_path": output_file,
        "video_id": video_id,
        "topic": topic,
        "type": video_type
    }

def run_daily_task():
    result = generate_video(upload=True)
    if result["status"] != "success":
        logger.error(f"Daily task failed: {result.get('reason')}")
    else:
        logger.info("Daily task completed successfully.")
