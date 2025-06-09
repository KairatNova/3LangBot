import os
from aiogram import Router, F, types
from aiogram.filters import Command, or_f, StateFilter
import aiosqlite
import google.generativeai as genai

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database.ai_database import AsyncAIDatabase
from handlers.config import Model, prompt

from dotenv import load_dotenv
from database.models import DB_NAME

load_dotenv()

ai_chat_router = Router()
db = AsyncAIDatabase()
# Конфигурация API ключа для Google Generative AI (API key configuration for Google Generative AI)
gemini_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = gemini_api_key)

# Модель и промпт для генеративного AI (Model and prompt for generative AI)
model = Model
chat = prompt


class WaitingForMessage(StatesGroup):
    CaptureMessages = State()
    NonCaptureMessages = State()

async def check_tokens_limit(user_id: int, new_tokens: int) -> bool:
    current_date, used_tokens = await db.get_user_tokens(user_id)
    if used_tokens + new_tokens > 2000:
        return False
    return True

async def get_remaining_tokens(user_id: int) -> int:
    current_date, used_tokens = await db.get_user_tokens(user_id)
    return 2000 - used_tokens
''
async def get_user_language(user_id: int) -> str:
    """Получает язык пользователя из базы данных"""
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute(
                "SELECT language FROM users WHERE telegram_id = ?", 
                (user_id,)
            )
            result = await cursor.fetchone()
            return result[0] if result else "ru"  # По умолчанию русский
    except Exception as e:
        print(f"Ошибка при получении языка: {e}")
        return "ru"''

async def command_chatgpt_intro(target, state: FSMContext):
    user_id = target.from_user.id if hasattr(target, 'from_user') else target.chat.id

    
    text = ("""
🇬🇧 <b>Привет! Я Английский Языковой Помощник</b> 🇺🇸
Чем я могу вам помочь?
🎓 <b>Совет</b>: Занимайтесь регулярно по 15-20 минут для лучшего результата!
""")
    await target.answer(text.strip(), parse_mode="HTML")
    await state.set_state(WaitingForMessage.CaptureMessages)

async def callback_chatgpt_intro(target, state: FSMContext):
    user_id = target.from_user.id if hasattr(target, 'from_user') else target.chat.id

    
    text = ("""
🇬🇧 <b>Английский Языковой Помощник chatgpt</b> 🇺🇸

✨ <b>Лимиты использования</b>  
- 2000 токенов в день (~2000 символов)  
- Лимит обновляется каждые 24 часа  
""")
    await target.answer(text.strip(), parse_mode="HTML")
    await state.set_state(WaitingForMessage.CaptureMessages)

@ai_chat_router.message(Command("chatgpt"))
async def handle_chatgpt_command(message: types.Message, state: FSMContext):
    await command_chatgpt_intro(message, state)

@ai_chat_router.callback_query(F.data == "chatgpt")
async def handle_chatgpt_button(callback: types.CallbackQuery, state: FSMContext):
    await callback_chatgpt_intro(callback.message, state)
    await callback.answer()

@ai_chat_router.message(WaitingForMessage.CaptureMessages)
async def bot_answer(message: types.Message, state: FSMContext):
    user_lang = await get_user_language(message.from_user.id)
    
    kb = [[types.KeyboardButton(text="stop⛔")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    if message.text == ("stop⛔"):
        await state.set_state(WaitingForMessage.NonCaptureMessages)
        await message.answer(
            ("Чат остановлен. Чтобы начать снова, введите /chatgpt"),
            reply_markup=types.ReplyKeyboardRemove()
        )
        return

    user_id = message.from_user.id
    remaining_tokens = await get_remaining_tokens(user_id)
    
    if remaining_tokens <= 0:
        await message.answer("⚠️ Вы израсходовали дневной лимит токенов (2000). Попробуйте завтра.")
        return

    waitforanswer = await message.answer("Generating answer⌛")
    
    try:
        if message.text:
            question = message.text
            response = chat.send_message(question, safety_settings={
                'HATE': 'BLOCK_NONE',
                'HARASSMENT': 'BLOCK_NONE',
                'SEXUAL': 'BLOCK_NONE',
                'DANGEROUS': 'BLOCK_NONE'
            })
            response_text = response.text
        elif message.photo:
            photos_dir = "photos"
            os.makedirs(photos_dir, exist_ok=True)
            file_name = f"{photos_dir}/{message.photo[-1].file_id}.jpg"
            await message.bot.download(message.photo[-1], destination=file_name)
            sample_file = genai.upload_file(path=file_name, display_name="UserPhoto")
            response = model.generate_content(("Опишите изображение" ), [sample_file])
            response_text = response.text
            os.remove(file_name)
        else:
            await message.answer("Этот тип сообщения не поддерживается")
            return

        # Примерный расчет токенов (1 токен ≈ 4 символа)
        tokens_used = len(response_text) // 4 + len(message.text or "") // 4
        
        if not await check_tokens_limit(user_id, tokens_used):
            await message.answer("⚠️ Превышен лимит токенов для этого запроса")
            return

        await db.update_tokens(user_id, tokens_used)
        await db.log_query(user_id, message.text or "[photo]", response_text, tokens_used)
        
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=waitforanswer.message_id
        )
        
        response_message = (
            f"{response_text}\n\n"
            f"{('ℹ️ Использовано токенов: {used} (Осталось: {remaining})').format(used=tokens_used, remaining=2000 - (await get_remaining_tokens(user_id)))}"
        )
        
        await message.answer(response_message, reply_markup=keyboard)

    except Exception as e:
        await message.answer(
            ("⚠️ Произошла ошибка: {error}").format(error=str(e))
        )