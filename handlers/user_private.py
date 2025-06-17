import asyncio
from datetime import datetime
from aiogram import F, types, Router
from aiogram.filters import  Command, or_f
import aiosqlite
from keyboards.kbds import   inline_markup,  menu_kb_add
from database.models import DB_NAME
from datetime import datetime

from database.models import update_last_active


DB_NAME = "data/userdata.db"
user_private = Router()

@user_private.message(Command("start"))
async def cmd_start(message: types.Message):
    user = message.from_user
    # Проверяем и добавляем пользователя в БД
    is_new_user = await check_and_create_user(
        telegram_id=user.id,
        first_name=user.first_name,
        username=user.username,
        language="ru"  # Язык по умолчанию
    )
    # Обновляем время последней активности
    await update_last_active(user.id)
    
    # Формируем приветственное сообщение
    if is_new_user is None:
        await message.answer("⚠️ Произошла ошибка при обработке вашего запроса")
        return
    
    if is_new_user:
        welcome_text = (
            f" Добро пожаловать, {user.first_name}!\n\n"
            "Я ваш персональный языковой помощник.\n"
            "Вот что я умею:\n"
            "• Переводчик с поддержкой 3 языков\n"
            "• Доступ к ИИ\n"
            "• Нужные слова для изучения\n\n"
            "Начните с команды /menu или выберите действие ниже👇"
        )
    else:
        welcome_text = (
            f"👋 С возвращением, {user.first_name}!\n\n"
            "Рад видеть вас снова! Чем могу помочь?\n"
            "Используйте /menu для доступа ко всем функциям."
        )
    
    await message.answer(
        welcome_text,
        reply_markup=menu_kb_add.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Выберите действие..."
        )
    )

async def check_and_create_user(telegram_id: int, first_name: str, username: str, language: str) -> bool:
    """
    Проверяет существование пользователя и создает нового при необходимости
    Возвращает:
    - True если пользователь новый
    - False если пользователь уже существовал
    - None при ошибке
    """
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            # Проверяем существование пользователя
            cursor = await db.execute(
                "SELECT 1 FROM users WHERE telegram_id = ?",
                (telegram_id,)
            )
            
            if await cursor.fetchone() is not None:
                return False  # Пользователь уже существует
            
            # Создаем нового пользователя
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await db.execute(
                """INSERT INTO users 
                (telegram_id, first_name, username, language, registration_date, last_active) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (telegram_id, first_name, username or "", language, now, now)
            )
            await db.commit()
            return True  # Новый пользователь
        
    except Exception as e:
        print(f"Ошибка в check_and_create_user: {str(e)}")
        return None

async def update_last_active(telegram_id: int) -> bool:
    """Обновляет время последней активности пользователя"""
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await db.execute(
                "UPDATE users SET last_active = ? WHERE telegram_id = ?",
                (now, telegram_id)
            )
            await db.commit()
            return True
    except Exception as e:
        print(f"Ошибка при обновлении last_active: {str(e)}")
        return False

@user_private.message(or_f(Command("menu"), (F.text.lower() == "меню")))
async def menu_kbd_cmd(message: types.Message):
    """Обработчик команды меню"""
    await message.answer(
        "📋 Главное меню:",
        reply_markup=inline_markup
    )