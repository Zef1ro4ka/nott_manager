from dotenv import load_dotenv
import os, logging, asyncio
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramAPIError

from app.disp import router

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    @dp.errors()
    async def handle_errors(update, error):
        logger.exception(f"Exception while handling update: {error}")
        return True

    try:
        logger.info("Бот запущено")
        await dp.start_polling(bot)
    except TelegramAPIError as e:
        logger.error(f"Telegram API Error: {e}")
    except Exception as e:
        logger.exception(f"Інша помилка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        print("Work is start")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Work is end")