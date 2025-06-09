import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, or_f
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


define_router = Router()

# Состояния
class DefineStates(StatesGroup):
    choosing_language = State()
    entering_word = State()


@define_router.callback_query(F.data == "define")
async def cmd_difine_callback(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="English", callback_data="lang_en")],
    [InlineKeyboardButton(text="Русский", callback_data="lang_ru")],
    [InlineKeyboardButton(text="Кыргызча", callback_data="lang_ky")],
    ])
    await callback.message.answer("🌐 Выберите язык слова:", reply_markup=keyboard)
    await state.set_state(DefineStates.choosing_language)

# Команда /define
@define_router.message(Command("define"))
async def cmd_define(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="English", callback_data="lang_en")],
    [InlineKeyboardButton(text="Русский", callback_data="lang_ru")],
    [InlineKeyboardButton(text="Кыргызча", callback_data="lang_ky")],
    ])
    await message.answer("🌐 Выберите язык слова:", reply_markup=keyboard)
    await state.set_state(DefineStates.choosing_language)

# Обработка выбора языка
@define_router.callback_query(F.data.startswith("lang_"))
async def process_language(callback: CallbackQuery, state: FSMContext):
    lang_code = callback.data.split("_")[1]
    await state.update_data(language=lang_code)
    if lang_code == "ru" or lang_code == "ky":
        await callback.message.reply("❗ Определение для этого языка пока не поддерживается. Будет добавлено позже.")
    else:
        await callback.message.answer("✍️ Введите слово для определения:")
    await state.set_state(DefineStates.entering_word)

# Получение слова и отправка определения
@define_router.message(DefineStates.entering_word)
async def process_word(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language")
    word = message.text.strip()
    
    
    await message.answer("🔎 Ищу определение...")

    definition = await get_definition(word, lang)

    if definition:
        await message.answer(f"📖 Значение слова *{word}*:\n{definition}", parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer(f"❌ Не удалось найти значение слова *{word}*.")

    await state.clear()

# Функция получения определения
async def get_definition(word: str, language: str) -> str | None:
    if language in ["ru", "ky"]:
        return "❗ Определение для этого языка пока не поддерживается. Будет добавлено позже."

    url = f"https://api.dictionaryapi.dev/api/v2/entries/{language}/{word}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                try:
                    meanings = data[0]["meanings"]
                    parts = []
                    for m in meanings:
                        part = m["partOfSpeech"]
                        defs = [d["definition"] for d in m["definitions"][:2]]
                        parts.append(f"*{part}*: " + "; ".join(defs))
                    return "\n".join(parts)
                except Exception:
                    return None
            return None
