import aiosqlite
import pandas as pd, openpyxl
from datetime import datetime
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

from aiogram.filters import Command, or_f




from database.feedback import check_feedback_limits, save_feedback

help_and_feedback_router = Router()


ADMIN_ID = 647302816  # Замени на свой Telegram ID
DB_NAME = "data/feedback.db"


class FeedbackForm(StatesGroup):
    waiting_for_feedback = State()



@help_and_feedback_router.message(or_f(Command("help"), (F.text.lower() == "help" )))
async def help_command(message: types.Message):
    await message.answer(''' 
📌 Описание и функции команд:\n
🟢 /start — запуск бота и выбор языка  
👤 /profile — ваш профиль  
📋 /menu — главное меню с сервисами  
🤖 /chatgpt — доступ к ИИ-помощнику (ChatGPT)  
📚 /define — узнать значение английских слов  
🌐 /translate — переводчик Google (фразы, предложения)  
🧠 /learn_words — изучение слов по темам на 3 языках (🇷🇺 RU / 🇺🇸 EN / 🇰🇬 KG) \n                
 💡 Что умеет бот:\n
1️⃣ Переводить слова и предложения между русским, английским и кыргызским языками.  
2️⃣ Отвечать на любые вопросы через ChatGPT  
   (ограничение — 2000 токенов в день, 1 токен ≈ 2–3 символа).  
3️⃣ Присылать определения слов по команде ( доступно только на английском).  
4️⃣ Предоставлять тематические списки слов на 3 языках для изучения.\n

✍️Чтобы написать отзыв нажмите на эту команду ---> /feedback\n
                         
Для поддержки автора и на развитие бота 
VISA - 
''')
# Модифицированный хендлер
@help_and_feedback_router.message(or_f(Command("feedback"), (F.text == "Оставить отзыв" )))
async def feedback_command(message: Message, state: FSMContext):
    # Проверяем лимиты
    allowed, error_msg = await check_feedback_limits(message.from_user.id)
    if not allowed:
        await message.answer(error_msg)
        return
    
    await message.answer("✍️ Напиши свой отзыв.")
    await state.set_state(FeedbackForm.waiting_for_feedback)

@help_and_feedback_router.message(FeedbackForm.waiting_for_feedback)
async def handle_feedback(message: Message, state: FSMContext):
    # Еще раз проверяем лимиты (на случай, если пользователь долго писал отзыв)
    allowed, error_msg = await check_feedback_limits(message.from_user.id)
    if not allowed:
        await message.answer(error_msg)
        await state.clear()
        return
    
    await state.clear()
    username = message.from_user.username or message.from_user.full_name
    await save_feedback(user_id=message.from_user.id, username=username, message=message.text)

    await message.answer("✅ Спасибо за ваш отзыв!")

    # Уведомить админа
    await message.bot.send_message(
        ADMIN_ID,
        f"📬 <b>Новый отзыв</b>\n"
        f"👤 От: @{username} (ID: <code>{message.from_user.id}</code>)\n"
        f"💬 <i>{message.text}</i>\n\n"
        f"Ответьте /reply_{message.from_user.id} чтобы ответить.",
        parse_mode="HTML"
    )






async def export_feedback_to_excel(filename: str = "feedback_export.xlsx"):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id, username, message, created_at FROM feedback") as cursor:
            rows = await cursor.fetchall()

    # Список словарей для DataFrame
    data = [
        {
            "User ID": row[0],
            "Username": row[1],
            "Message": row[2],
            "Date": row[3]
        }
        for row in rows
    ]

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename


@help_and_feedback_router.message(Command("export_feedback"))
async def export_feedback_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ У вас нет доступа.")

    filename = await export_feedback_to_excel()
    await message.answer_document(
        document=FSInputFile(filename),
        caption="📊 Все отзывы в Excel"
    )
