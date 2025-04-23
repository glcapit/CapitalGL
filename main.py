import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHAT_IDS = list(map(int, os.getenv("SOURCE_CHAT_IDS").split(",")))
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Бот работает! Репост сообщений активен.")

# Репост сообщений из источников в целевой чат
@dp.message_handler(lambda message: message.chat.id in SOURCE_CHAT_IDS)
async def forward_message(message: types.Message):
    try:
        await message.copy_to(chat_id=TARGET_CHAT_ID)
        print(f"✅ Репост из {message.chat.id} в {TARGET_CHAT_ID}")
    except Exception as e:
        print(f"❌ Ошибка при пересылке из {message.chat.id}: {e}")

# Запуск бота
if __name__ == "__main__":
    print("🔁 Бот запущен. Источники:", SOURCE_CHAT_IDS)
    executor.start_polling(dp, skip_updates=True)
