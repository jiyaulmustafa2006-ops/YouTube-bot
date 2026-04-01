import json
import os
import time

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache(key, ttl=3600):
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            data = json.load(f)
            if time.time() - data['timestamp'] < ttl:
                return data['value']
    return None

def set_cache(key, value):
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    with open(cache_file, 'w') as f:
        json.dump({'timestamp': time.time(), 'value': value}, f)
