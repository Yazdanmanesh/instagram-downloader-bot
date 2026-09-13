import os
import asyncio
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "YOUR_BOT_TOKEN"

async def download_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "instagram.com/reel/" not in url and "instagram.com/reels/" not in url:
        await update.message.reply_text("لینک ریلز اینستاگرام بفرست.")
        return

    await update.message.reply_text("⏳ در حال دانلود...")

    filename = f"reel_{update.message.message_id}.mp4"

    try:
        ydl_opts = {
            "outtmpl": filename,
            "format": "best[ext=mp4]/best",
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(filename, "rb") as video:
            await update.message.reply_video(
                video=video,
                caption="✅ دانلود شد"
            )

    except Exception as e:
        await update.message.reply_text("❌ دانلود انجام نشد.")

    finally:
        if os.path.exists(filename):
            os.remove(filename)


async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, download_reel)
    )

    print("Bot is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
