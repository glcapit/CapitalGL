import os
import json
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
USERS_FILE = "subscribers.json"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# ✅ Подписка — сохранить user_id
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    subscribers = load_subscribers()
    if user_id not in subscribers:
        subscribers.append(user_id)
        save_subscribers(subscribers)
    await message.answer("✅ Вы подписались на репосты из групп!")

# 🔁 Репост в лички всех подписчиков
@dp.message_handler(lambda message: message.chat.id in SOURCE_CHAT_IDS)
async def repost(message: types.Message):
    subscribers = load_subscribers()
    for uid in subscribers:
        try:
            await message.copy_to(chat_id=uid)
            print(f"🔁 Отправлено пользователю {uid}")
        except Exception as e:
            print(f"❌ Ошибка при отправке {uid}: {e}")

# JSON база пользователей
def load_subscribers():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_subscribers(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f)

# Webhook
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    print("🚀 Webhook установлен")

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
