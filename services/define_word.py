import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup

define_router = Router()

# Состояния
class DefineStates(StatesGroup):
    choosing_language = State()
    entering_word = State()

# Кнопки выбора языка
@define_router.callback_query(F.data == "define")
async def cmd_difine_callback(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="English", callback_data="lang_en")],
        [InlineKeyboardButton(text="Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="Кыргызча", callback_data="lang_ky")],
    ])
    await callback.message.answer("🌐 Выберите язык слова:", reply_markup=keyboard)
    await state.set_state(DefineStates.choosing_language)

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
    await callback.message.answer("✍️ Введите слово для определения:")
    await state.set_state(DefineStates.entering_word)

# Получение слова и отправка значения
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

# Функция получения значения (обновлённая)
async def get_definition(word: str, language: str) -> str | None:
    if language in ["ru", "ky"]:
        lang_name = "Русский" if language == "ru" else "Кыргызский"
        url = f"https://ru.wiktionary.org/wiki/{word}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    return None
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                section = soup.find("span", id=lang_name)
                if not section:
                    return f"⚠️ Раздел языка '{lang_name}' не найден."

                definitions = []
                for tag in section.find_all_next():
                    if tag.name == 'ol':
                        for li in tag.find_all('li', recursive=False):
                            definitions.append(li.text.strip())
                        break
                    if tag.name == 'h2':
                        break

                if not definitions:
                    return "ℹ️ Определений не найдено."
                return "\n".join(f"{i+1}. {d}" for i, d in enumerate(definitions))
    
    # Для английского
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
