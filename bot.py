import asyncio
import subprocess
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("8383539672:AAHrMHQobXR8LptpiLpdD5kDwPsUxV2rQIU")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("🎥 Video link yuboring (YouTube / TikTok / Instagram)")

@dp.message()
async def download(message: types.Message):
    url = message.text.strip()
    await message.answer("⏳ Yuklanmoqda...")

    try:
        cmd = [
            "yt-dlp",
            "-f", "mp4",
            "-o", "video.mp4",
            url
        ]
        subprocess.run(cmd, check=True)

        await message.answer_video(types.FSInputFile("video.mp4"))
        os.remove("video.mp4")

    except Exception:
        await message.answer("❌ Video yuklab bo‘lmadi")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
