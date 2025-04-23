import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.webhook import get_new_configured_app
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # например: https://yourbot.onrender.com/webhook
SOURCE_CHAT_IDS = list(map(int, os.getenv("SOURCE_CHAT_IDS").split(",")))
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 5000))  # Render предоставляет PORT автоматически

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# 📍 Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("✅ Webhook-бот работает!\nРепост активен.")

# 🔁 Репост сообщений из SOURCE_CHAT_IDS в TARGET_CHAT_ID
@dp.message_handler(lambda message: message.chat.id in SOURCE_CHAT_IDS)
async def forward_message(message: types.Message):
    try:
        await message.copy_to(chat_id=TARGET_CHAT_ID)
        print(f"✅ Репост из {message.chat.id} в {TARGET_CHAT_ID}")
    except Exception as e:
        print(f"❌ Ошибка при пересылке: {e}")

# Установка Webhook при старте
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    print(f"🚀 Webhook установлен: {WEBHOOK_URL}")

# Удаление Webhook при остановке
async def on_shutdown(app):
    await bot.delete_webhook()
    print("🔻 Webhook удалён")

# Создание и запуск aiohttp-приложения
app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# Обработка входящих webhook-запросов
app.router.add_post("/webhook", get_new_configured_app(dispatcher=dp, bot=bot))

# Точка входа
if __name__ == "__main__":
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
