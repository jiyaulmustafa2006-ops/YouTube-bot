import requests
import os
from dotenv import load_dotenv
from cache import get_cache, set_cache
from logger import logger

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"
PEXELS_PHOTO_URL = "https://api.pexels.com/v1/search"

def fetch_stock_videos(query, per_page=5, orientation="portrait"):
    cache_key = f"videos_{query}_{orientation}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "per_page": per_page,
        "orientation": orientation,
        "size": "medium"
    }
    try:
        response = requests.get(PEXELS_VIDEO_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        videos = data.get("videos", [])
        video_urls = [v["video_files"][0]["link"] for v in videos if v["video_files"]]
        set_cache(cache_key, video_urls)
        return video_urls
    except Exception as e:
        logger.error(f"Failed to fetch videos: {e}")
        return []

def fetch_stock_images(query, per_page=3):
    cache_key = f"images_{query}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page}
    try:
        response = requests.get(PEXELS_PHOTO_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        images = data.get("photos", [])
        image_urls = [img["src"]["original"] for img in images]
        set_cache(cache_key, image_urls)
        return image_urls
    except Exception as e:
        logger.error(f"Failed to fetch images: {e}")
        return []
