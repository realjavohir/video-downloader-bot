import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import yt_dlp

BOT_TOKEN = "8383539672:AAHrMHQobXR8LptpiLpdD5kDwPsUxV2rQIU"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_video(url: str):
    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "socket_timeout": 30,
        "concurrent_fragment_downloads": 8,  # ⚡ tez yuklash
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        return file_path


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer(
        "🎬 Video Download Bot\n\n"
        "TikTok / Instagram / YouTube link yuboring\n"
        "Katta videolarni ham tez yuklab beraman 🚀"
    )


@dp.message_handler(lambda m: m.text.startswith("http"))
async def handle_link(msg: types.Message):
    await msg.answer("⏳ Video yuklanmoqda, kuting...")

    try:
        loop = asyncio.get_event_loop()
        file_path = await loop.run_in_executor(None, download_video, msg.text)

        if os.path.getsize(file_path) > 49 * 1024 * 1024:
            await msg.answer("❗ Video juda katta (50MB+). Fayl sifatida yuborilmoqda")
            await bot.send_document(msg.chat.id, open(file_path, "rb"))
        else:
            await bot.send_video(msg.chat.id, open(file_path, "rb"))

        os.remove(file_path)

    except Exception as e:
        await msg.answer(f"❌ Xatolik:\n{e}")


if __name__ == "__main__":
    executor.start_polling(dp)
