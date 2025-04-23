import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = "/webhook"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 5000))

SOURCE_CHAT_IDS = list(map(int, os.getenv("SOURCE_CHAT_IDS").split(",")))
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Команда /start
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("✅ Webhook-бот работает!")

# Репост сообщений
@dp.message_handler(lambda message: message.chat.id in SOURCE_CHAT_IDS)
async def repost(message: types.Message):
    try:
        await message.copy_to(chat_id=TARGET_CHAT_ID)
        print(f"🔁 Репост из {message.chat.id}")
    except Exception as e:
        print(f"❌ Ошибка при пересылке: {e}")

# Запуск webhook
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    print("🚀 Webhook установлен:", WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()
    print("🔻 Webhook удалён")

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
