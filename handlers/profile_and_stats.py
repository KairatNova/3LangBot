import aiosqlite
from datetime import datetime
from aiogram import F, types, Router
from aiogram.filters import  Command, or_f
from database.models import DB_NAME
from handlers import user_private


profile_and_stats_router = Router()


@profile_and_stats_router.message(or_f(Command("profile"), (F.text.lower() == "профиль")))
async def cmd_profile(message: types.Message):
    # Обновляем время последней активности
    await user_private.update_last_active(message.from_user.id)
    
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            # Получаем данные пользователя
            cursor = await db.execute(
                "SELECT * FROM users WHERE telegram_id = ?",
                (message.from_user.id,)
            )
            user_data = await cursor.fetchone()
            
            if not user_data:
                await message.answer("❌ Профиль не найден. Пожалуйста, зарегистрируйтесь через /start")
                return
            
            # Форматируем даты для лучшего отображения
            reg_date = datetime.strptime(user_data[4], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y в %H:%M")
            last_active = datetime.strptime(user_data[5], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y в %H:%M")
            
            profile_text = (
                "👤 <b>Ваш профиль</b>\n\n"
                f"🆔 <b>ID:</b> <code>{user_data[0]}</code>\n"
                f"👁️ <b>Username:</b> @{user_data[2] if user_data[2] else 'не указан'}\n"
                f"📛 <b>Имя:</b> {user_data[1]}\n"
                #f"🌐 <b>Язык:</b> {user_data[3].upper()}\n"
                f"📅 <b>Регистрация:</b> {reg_date}\n"
                f"🕒 <b>Последняя активность:</b> {last_active}\n\n"
                f"<i>Используйте бота для изучения языков!</i>"
            )
            
            await message.answer(profile_text, parse_mode="HTML")
            
    except aiosqlite.Error as e:
        print(f"Ошибка базы данных: {e}")
        await message.answer("⚠️ Произошла ошибка при загрузке профиля. Попробуйте позже.")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        await message.answer("⚠️ Произошла непредвиденная ошибка. Попробуйте позже.")

