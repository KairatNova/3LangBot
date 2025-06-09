import aiosqlite
from datetime import datetime

DB_NAME = "data/translations.db"

async def translate_db():
    """Инициализация базы данных и создание таблиц"""
    async with aiosqlite.connect(DB_NAME) as db:
        # Таблица для хранения истории переводов
        await db.execute("""
            CREATE TABLE IF NOT EXISTS translation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                first_name TEXT,
                original_text TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                source_lang TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Создаем индекс для быстрого поиска по пользователю
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_history 
            ON translation_history(user_id)
        """)
        await db.commit()

async def save_translation(
    user_id: int,
    original_text: str,
    translated_text: str,
    source_lang: str,
    target_lang: str,
    username: str = None,
    first_name: str = None
):
    """Сохранение перевода в историю и очистка, если записей больше 10"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """INSERT INTO translation_history 
            (user_id, username, first_name, original_text, translated_text, source_lang, target_lang)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, username, first_name, original_text, translated_text, source_lang, target_lang)
        )
        await db.commit()

        # Удаление старых записей, если их больше 10
        await db.execute(
            """
            DELETE FROM translation_history 
            WHERE id NOT IN (
                SELECT id FROM translation_history 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT 10
            ) AND user_id = ?
            """,
            (user_id, user_id)
        )
        await db.commit()


async def get_user_history(user_id: int, limit: int = 10):
    """Получение истории переводов пользователя"""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """SELECT 
                original_text, 
                translated_text, 
                source_lang, 
                target_lang, 
                timestamp 
            FROM translation_history 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?""",
            (user_id, limit)
        )
        return await cursor.fetchall()

async def clear_user_history(user_id: int):
    """Очистка истории пользователя с подтверждением"""
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем количество записей перед удалением
        cursor = await db.execute(
            "SELECT COUNT(*) FROM translation_history WHERE user_id = ?",
            (user_id,)
        )
        count = (await cursor.fetchone())[0]
        
        if count == 0:
            return False
        
        await db.execute(
            "DELETE FROM translation_history WHERE user_id = ?",
            (user_id,)
        )
        await db.commit()
        
        # Проверяем, что записи действительно удалились
        cursor = await db.execute(
            "SELECT COUNT(*) FROM translation_history WHERE user_id = ?",
            (user_id,))
        remaining = (await cursor.fetchone())[0]
        
        return remaining == 0


    