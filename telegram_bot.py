import os
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from logger import logger
from scheduler import generate_video

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

running_job = None
job_lock = threading.Lock()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste! I'm your YouTube automation bot.\n"
        "Commands:\n"
        "/shorts <topic> - Generate a Short video (topic optional)\n"
        "/long <topic> - Generate a Long video (topic optional)\n"
        "/status - Check if a video is being generated\n"
        "/cancel - Cancel current generation (if running)"
    )

async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE, is_short=True):
    global running_job
    with job_lock:
        if running_job is not None and running_job.is_alive():
            await update.message.reply_text("A video is already being generated. Please wait or use /cancel.")
            return

    topic = " ".join(context.args) if context.args else None
    msg = await update.message.reply_text(f"Starting {'Short' if is_short else 'Long'} video generation...")

    def worker():
        nonlocal running_job
        try:
            result = generate_video(topic=topic, is_short=is_short, upload=True)
            import asyncio
            async def send_result():
                if result["status"] == "success":
                    await msg.edit_text(
                        f"✅ Video generated successfully!\n"
                        f"Topic: {result['topic']}\n"
                        f"Type: {result['type']}\n"
                        f"YouTube: https://youtu.be/{result['video_id']}"
                    )
                else:
                    await msg.edit_text(f"❌ Failed: {result.get('reason', 'Unknown error')}")
            asyncio.run_coroutine_threadsafe(send_result(), context.bot._loop)
        except Exception as e:
            logger.exception("Worker error")
            import asyncio
            async def send_error():
                await msg.edit_text(f"❌ Error: {str(e)}")
            asyncio.run_coroutine_threadsafe(send_error(), context.bot._loop)
        finally:
            with job_lock:
                running_job = None

    thread = threading.Thread(target=worker)
    thread.start()
    with job_lock:
        running_job = thread

async def shorts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await generate_command(update, context, is_short=True)

async def long_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await generate_command(update, context, is_short=False)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with job_lock:
        if running_job and running_job.is_alive():
            await update.message.reply_text("A video is currently being generated. Please wait.")
        else:
            await update.message.reply_text("No video is being generated at the moment.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancellation is not supported mid-way. Please wait for current job to finish.")

def run_bot():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("shorts", shorts))
    app.add_handler(CommandHandler("long", long_video))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("cancel", cancel))
    logger.info("Telegram bot started.")
    app.run_polling()
