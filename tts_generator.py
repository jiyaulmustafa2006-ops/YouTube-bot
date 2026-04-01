import asyncio
import edge_tts
from logger import logger

async def _generate_audio_async(script, filename):
    voice = "hi-IN-MadhurNeural"  # Male Hindi voice
    communicate = edge_tts.Communicate(script, voice)
    await communicate.save(filename)

def generate_audio(script, filename):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_generate_audio_async(script, filename))
        logger.info(f"Audio saved: {filename}")
        return filename
    except Exception as e:
        logger.error(f"Edge TTS failed: {e}")
        return None
