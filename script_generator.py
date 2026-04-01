import os
from openai import OpenAI
from dotenv import load_dotenv
from logger import logger
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_script(topic, is_short=True):
    if is_short:
        prompt = f"""नीचे दिए गए विषय पर 80-120 शब्दों में एक YouTube Shorts स्क्रिप्ट लिखें। पहले 3 सेकंड में हुक डालें। भाषा हिंदी में होनी चाहिए।

विषय: {topic}

स्क्रिप्ट:"""
        max_tokens = 200
    else:
        prompt = f"""नीचे दिए गए विषय पर 800-1500 शब्दों में एक YouTube लॉन्ग-फॉर्म वीडियो स्क्रिप्ट लिखें। कहानी कहने का तरीका अपनाएं और दर्शकों को बांधे रखें। भाषा हिंदी में होनी चाहिए।

विषय: {topic}

स्क्रिप्ट:"""
        max_tokens = 1500

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "आप एक पेशेवर YouTube स्क्रिप्ट लेखक हैं। हिंदी में आकर्षक स्क्रिप्ट लिखें।"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        script = response.choices[0].message.content.strip()
        logger.info(f"Hindi script generated for {topic}")
        return script
    except Exception as e:
        logger.error(f"Script generation failed: {e}")
        return None
