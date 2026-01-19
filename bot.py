import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import yt_dlp

BOT_TOKEN = os.getenv("8383539672:AAHrMHQobXR8LptpiLpdD5kDwPsUxV2rQIU")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def ydl_opts(video=True):
    opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        "concurrent_fragment_downloads": 8,
    }
    if video:
        opts["format"] = "bestvideo+bestaudio/best"
        opts["merge_output_format"] = "mp4"
    else:
        opts["format"] = "bestaudio"
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    return opts

def download(url, video=True):
    with yt_dlp.YoutubeDL(ydl_opts(video)) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("🎬 Video downloader bot\nLink yuboring")

@dp.message_handler(lambda m: m.text.startswith("http"))
async def choose(msg: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🎥 Video", callback_data=f"v|{msg.text}"),
        InlineKeyboardButton("🎧 MP3", callback_data=f"a|{msg.text}")
    )
    await msg.answer("Tanlang:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith(("v|","a|")))
async def handle(call: types.CallbackQuery):
    t, url = call.data.split("|")
    await call.message.edit_text("⏳ Yuklanmoqda...")

    loop = asyncio.get_event_loop()
    path = await loop.run_in_executor(None, download, url, t == "v")

    if t == "v":
        await bot.send_document(call.message.chat.id, open(path,"rb"))
    else:
        await bot.send_audio(call.message.chat.id, open(path,"rb"))

    os.remove(path)

if __name__ == "__main__":
    executor.start_polling(dp)
