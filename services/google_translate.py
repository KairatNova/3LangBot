from datetime import datetime
import os
from aiogram import F, Router, types, html
from aiogram.filters import Command

from google.cloud import translate_v2 as translate
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from dotenv import find_dotenv, load_dotenv
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, or_f
from aiogram.types import CallbackQuery
from database.translate_db import save_translation
from handlers.config import LANGUAGES
from keyboards import kbds
from keyboards.kbds import get_language_keyboard, get_main_keyboard


load_dotenv(find_dotenv())
translator_router = Router()

# Инициализация клиента перевода
translate_client = translate.Client(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

# Состояния пользователей
user_states = {}  # True - переводчик включен, False - выключен
user_target_languages = {}  # Хранит выбранные языки

DetectorFactory.seed = 0  

@translator_router.callback_query(F.data == "translate")
async def activate_translator_callback(callback: CallbackQuery):
    user_states[callback.from_user.id] = True
    await callback.message.edit_reply_markup(reply_markup=None)  # если хочешь убрать кнопки
    await callback.message.answer(
        "Выберите язык для перевода:",
        reply_markup=get_language_keyboard(),
        input_field_placeholder='На какой язык хотите перевести?'
    )
    await callback.answer()

@translator_router.message(or_f(Command("translate"), F.text.lower() == "переводчик"))
async def activate_translator_text(message: Message):
    user_states[message.from_user.id] = True
    await message.answer(
        "Выберите язык для перевода:",
        reply_markup=get_language_keyboard(),
        placeholder='На какой язык хотите перевести?'
    )

#@translator_router.message(F.text == "🔁 Включить переводчик")
#async def enable_translator(message: types.Message):
#    """Включение переводчика через кнопку"""
#    user_states[message.from_user.id] = True
#    await message.answer(
#        "Выберите язык для перевода:",
#        reply_markup=get_language_keyboard()
#    )
@translator_router.message(F.text == "🚫 Выключить переводчик")
async def disable_translator(message: types.Message):
    """Выключение переводчика"""
    user_states[message.from_user.id] = False
    await message.answer(
        "Переводчик выключен. Нажмите /translate или кнопку для активации.",
        reply_markup=get_main_keyboard()
    )

@translator_router.message(F.text == "🔙 Назад")
async def back_to_main(message: types.Message):
    """Возврат в главное меню"""
    await message.answer(
        "Выберите действие:",
        reply_markup=get_main_keyboard()
    )


LANGUAGE_CODES = {v: k for k, v in LANGUAGES.items()}

@translator_router.message(F.text.in_(LANGUAGES.keys()))
async def set_target_language(message: types.Message):
    """Установка целевого языка"""
    lang_name = message.text
    lang_code = LANGUAGES[lang_name]
    user_target_languages[message.from_user.id] = lang_code
    await message.answer(
        f"Язык перевода установлен: {lang_name}\n"
        "Отправьте текст для перевода или нажмите '🔙 Назад'",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔙 Назад")],

            ],
            resize_keyboard=True
        )
    )


async def detect_language_safe(text: str) -> str:
    """Безопасное определение языка с улучшенной обработкой кыргызского"""
    try:
        # Сначала проверяем явные признаки кыргызского
        if is_kyrgyz_text(text):
            return 'ky'
            
        # Пробуем определить язык стандартным способом
        detected = detect(text)
        
        # Проверяем, есть ли этот язык в нашем словаре
        if detected in LANGUAGE_CODES:
            return detected
            
        # Дополнительные проверки для других языков
        if any(char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' for char in text.lower()):
            return 'ru'
        elif any(char in 'abcdefghijklmnopqrstuvwxyz' for char in text.lower()):
            return 'en'
        elif any(char in 'äöüß' for char in text.lower()):
            return 'de'
            
        return 'auto'
    except:
        return 'auto'

def is_kyrgyz_text(text: str) -> bool:
    """Проверяет, является ли текст кыргызским"""
    kyrgyz_chars = {'ң', 'ү', 'ө', 'Ң', 'Ү', 'Ө'}
    common_kyrgyz_words = { 'кандай', 'канча', 'керек','кандайсын', 'Кандайсын'
    'мен', 'сен', 'ал', 'биз', 'силер', 'алар',
    'ким', 'эмне', 'бул', 'тигил', 'кайсы', 'өз',
    'бар', 'жок', 'кел', 'кет', 'көр', 'айт', 'уг', 'бил', 'жаса',
    'тур', 'отур', 'бер', 'ал', 'жеш', 'ич', 'ойло', 'жүр', 'сүй',
    'жакшы', 'жаман', 'чоң', 'кичине', 'көп', 'аз', 'эрте', 'кеч',
    'жаңы', 'эски', 'тез', 'жай', 'ысык', 'суук', 'туура', 'туура эмес',
    'адам', 'бала', 'аял', 'эркек', 'үй', 'мектеп', 'иш', 'сөз',
    'тил', 'акча', 'күн', 'түн', 'суу', 'тамак', 'жер', 'асман',
    'дос', 'ата', 'апа', 'шаар',
    'жана', 'менен', 'же', 'үчүн', 'сыяктуу', 'да', 'дагы',
    'эмес', 'эле', 'бирок', 'анткени', 'кийин', 'мурда', 'учурда',
    'бери', 'чейин', 'болсо', 'ушундай', 
    'бүгүн', 'эртең', 'кечээ', 'азыр', 'ар дайым', 'кээде', 'эч качан',
    'бир', 'эки', 'үч', 'төрт', 'беш', 'алты', 'жети', 'сегиз', 'тогуз', 'он',
    'салам', 'кош', 'болот'}
    
    # Проверка на специфичные кыргызские символы
    if any(char in kyrgyz_chars for char in text):
        return True
        
    # Проверка на часто используемые кыргызские слова
    words = text.lower().split()
    if any(word in common_kyrgyz_words for word in words[:5]):  # Проверяем первые 5 слов
        return True
        
    return False

@translator_router.message(F.text)
async def handle_text(message: types.Message):
    """Обработка текста для перевода с улучшенной поддержкой кыргызского"""
    user_id = message.from_user.id
    
    if not user_states.get(user_id, False):
        return
    
    if user_id not in user_target_languages:
        await message.answer(
            "Сначала выберите язык перевода через /translate",
            reply_markup=get_language_keyboard()
        )
        return
    
    try:
        text = message.text
        target_lang = user_target_languages[user_id]
        
        # Явно указываем source_lang для кыргызского
        if is_kyrgyz_text(text):
            source_lang = 'ky'
        else:
            source_lang = await detect_language_safe(text)
        
        # Для перевода с кыргызского всегда явно указываем source
        if source_lang == 'ky':
            result = translate_client.translate(
                text,
                target_language=target_lang,
                source_language='ky'  # Явно указываем кыргызский
            )
        else:
            result = translate_client.translate(
                text,
                target_language=target_lang,
                source_language=source_lang if source_lang != 'auto' else None
            )
        
        # Сохраняем перевод в историю
        await save_translation(
            user_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            original_text=text,
            translated_text=result['translatedText'],
            source_lang=source_lang,
            target_lang=target_lang
        )
        
        # Форматируем ответ
        source_lang_name = LANGUAGE_CODES.get(source_lang, source_lang)
        target_lang_name = LANGUAGE_CODES.get(target_lang, target_lang)
        
        response = (
            #f"<b>Оригинал</b> ({source_lang_name}):\n"
            #f"{html.quote(text)}\n\n"
            f"<b>Перевод</b> ({target_lang_name}):\n"
            f"{html.quote(result['translatedText'])}"
        )
        
        await message.answer(response, reply_markup=get_main_keyboard())
        
    except Exception as e:
        await message.answer(f"⚠️ Ошибка перевода: {str(e)}")