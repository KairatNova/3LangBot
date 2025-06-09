from aiogram import  types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove,ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton
from handlers.config import LANGUAGES


inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=" Переводчик", callback_data="translate")],
    [InlineKeyboardButton(text=" ChatGPT", callback_data="chatgpt")],
    [InlineKeyboardButton(text=" Учить слова", callback_data="learn_words")],
    [InlineKeyboardButton(text=" Значение слов", callback_data="define")],


])


# МЕНЮ КНОПОК
del_kbd = ReplyKeyboardRemove()

menu_kb = ReplyKeyboardBuilder()
menu_kb.add(
    KeyboardButton(text="Меню"),
    KeyboardButton(text="Профиль"),

)
menu_kb.adjust(2, 2)

# ДОБАВЛЕНИЕ КНОПКИ
menu_kb_add = ReplyKeyboardBuilder()
menu_kb_add.attach(menu_kb)


def get_main_keyboard():
    """Клавиатура основного меню"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🔁 Включить переводчик"))
    builder.add(KeyboardButton(text="🚫 Выключить переводчик"))

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_language_keyboard():
    """Клавиатура выбора языка с учетом языка интерфейса"""
    builder = ReplyKeyboardBuilder()
    for lang_name in LANGUAGES.keys():
        builder.add(KeyboardButton(text=lang_name))
    #builder.add(KeyboardButton(text=get_translation("back_button", lang)))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_choice_language_keyboard(lang: str = "ru"):
    """Клавиатура для выбора языка с учетом текущего языка"""
    translations = {
        "ru": {
            "russian": "🇷🇺 Русский",
            "english": "🇬🇧 English",
            "kyrgyz": "🇰🇬 Кыргызча"
        },
        "en": {
            "russian": "🇷🇺 Russian",
            "english": "🇬🇧 English",
            "kyrgyz": "🇰🇬 Kyrgyz"
        },
        "ky": {
            "russian": "🇷🇺 Орусча",
            "english": "🇬🇧 Англисче",
            "kyrgyz": "🇰🇬 Кыргызча"
        }
    }
    
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text=translations[lang]["russian"]),
        types.KeyboardButton(text=translations[lang]["english"]),
        types.KeyboardButton(text=translations[lang]["kyrgyz"])
    )
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)

