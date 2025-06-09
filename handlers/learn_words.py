
import json
import os
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData




learn_words_router = Router()

with open("data/words.json", "r", encoding="utf-8") as f:
    words_data = json.load(f)

# Подкатегории по категориям
subcategories = {
    "pronouns": [
        "Личные местоимения", "Притяжательные местоимения", "Указательные местоимения",
        "Вопросительные местоимения", "Возвратное местоимение"
    ],
    "prepositions": [
        "Пространственные предлоги", "Временные предлоги", "Предлоги причины и цели", "Прочие предлоги"
    ],
    "adverbs": [
        "Наречия времени", "Наречия места", "Образа действия", "Наречия степени", "Вопросительные"
    ],
    "questions": [
        "Вопросительные слова", "Примеры простых вопросов"
    ],
    "nouns": [
        "Люди", "Природа и явления", "Вещи и предметы", "Животные", "Места", "Абстрактные понятия"
    ],
    "verbs": [
        "Повседневные действия", "Движение", "Чувства и эмоции", "Мыслительные процессы", "Речь и общение", "Прочие важные глаголы"
    ],
    "adjectives": [
        "Качество и состояние", "Размер и количество", "Цвета", "Форма и структура", "Вкус и ощущения", "Характер и настроение"
    ]
}

# Команда /learn_words
@learn_words_router.message(F.text == "/learn_words")
async def learn_words_command(message: types.Message):
    await message.answer("Выберите раздел:", reply_markup=get_main_menu())

# Инлайн-кнопка "Учить слова"
@learn_words_router.callback_query(F.data == "learn_words")
async def learn_words_button(callback: CallbackQuery):
    await callback.message.edit_text("Выберите раздел:", reply_markup=get_main_menu())

# Главное меню с категориями
def get_main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="Местоимения", callback_data="subcategories_pronouns")
    kb.button(text="Предлоги", callback_data="subcategories_prepositions")
    kb.button(text="Наречия", callback_data="subcategories_adverbs")
    kb.button(text="Вопросы", callback_data="subcategories_questions")
    kb.button(text="Существительные", callback_data="subcategories_nouns")
    kb.button(text="Глаголы", callback_data="subcategories_verbs")
    kb.button(text="Прилагательные", callback_data="subcategories_adjectives")
    kb.adjust(2)
    return kb.as_markup()

# Подкатегории (открываются сразу при выборе категории)
@learn_words_router.callback_query(F.data.startswith("subcategories_"))
async def show_subcategories(callback: CallbackQuery):
    cat = callback.data.split("_")[1]
    subs = subcategories.get(cat, [])
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=sub, callback_data=f"words_{cat}_{i}")]
            for i, sub in enumerate(subs, start=1)
        ] + [[InlineKeyboardButton(text="⬅ Назад", callback_data="learn_words")]]
    )
    await callback.message.edit_text(f"🔸 Подразделы: *{cat.capitalize()}*", reply_markup=markup, parse_mode="Markdown")

# Отображение слов
@learn_words_router.callback_query(F.data.startswith("words_"))
async def show_words(callback: CallbackQuery):
    _, cat, idx = callback.data.split("_")
    idx = int(idx)
    sub_name = subcategories.get(cat, [])[idx - 1]
    words = words_data.get(cat, {}).get(sub_name, [])

    if not words:
        text = "⚠️ Слова для этого раздела пока не добавлены."
    else:
        text = f"📚 *{sub_name}*\n\n"
        text += "\n".join([f"{r} —— {e} —— {k}" for r, e, k in words])

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад", callback_data=f"subcategories_{cat}")]
        ]
    )
    await callback.message.edit_text(text, reply_markup=markup, parse_mode="Markdown")