import asyncio
import os
import logging
import sys

from aiogram import Bot, Dispatcher, types, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv

from middleware.private_chat import IgnoreGroupMiddleware

load_dotenv(find_dotenv())


from handlers.user_private import user_private
from handlers.learn_words import learn_words_router
from keyboards.bot_cmd_list import private
from handlers.profile_and_stats import profile_and_stats_router
from services.google_translate import translator_router

from services.ai_chat import ai_chat_router
from services.define_word import define_router
from handlers.help_and_feedback import help_and_feedback_router

from database.ai_database import AsyncAIDatabase
from database.translate_db import translate_db
from database.models import user_data_db
from database.feedback import feedback_data 

bot = Bot(
    token=os.getenv('TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
dp.include_router(help_and_feedback_router)
dp.include_router(define_router)
dp.include_router(learn_words_router)
dp.include_router(user_private)
dp.include_router(ai_chat_router)
dp.include_router(profile_and_stats_router)
dp.include_router(translator_router)

dp.message.middleware(IgnoreGroupMiddleware())
db = AsyncAIDatabase()



logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

async def main():
    await user_data_db()
    await translate_db()
    await db.ai_init_db()
    await db.reset_daily_limits()
    await feedback_data()
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())

    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())