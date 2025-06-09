from datetime import datetime
import aiosqlite

DB_NAME = "data/userdata.db"

async def user_data_db():
    """Инициализация БД при старте приложения"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                first_name TEXT,
                username TEXT,
                language TEXT DEFAULT 'ru',
                registration_date TEXT,
                last_active TEXT
            )
        """)
        await db.commit()

async def create_or_update_user(telegram_id: int, first_name: str, username: str, language: str = 'ru') -> bool:
    """Создает или обновляет пользователя"""
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Проверяем существование пользователя
            cursor = await db.execute(
                "SELECT 1 FROM users WHERE telegram_id = ?", 
                (telegram_id,))
            
            if await cursor.fetchone():
                # Обновляем данные существующего пользователя
                await db.execute(
                    """UPDATE users SET 
                    first_name = ?,
                    username = ?,
                    last_active = ?
                    WHERE telegram_id = ?""",
                    (first_name, username, now, telegram_id)
                )
            else:
                # Создаем нового пользователя
                await db.execute(
                    """INSERT INTO users 
                    (telegram_id, first_name, username, language, registration_date, last_active) 
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (telegram_id, first_name, username, language, now, now)
                )
            
            await db.commit()
            return True
            
    except aiosqlite.Error as e:
        print(f"Database error: {e}")
        return False

async def get_user_language(telegram_id: int) -> str:
    """Получает язык пользователя"""
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute(
                "SELECT language FROM users WHERE telegram_id = ?", 
                (telegram_id,))
            result = await cursor.fetchone()
            return result[0] if result else 'ru'
    except aiosqlite.Error as e:
        print(f"Language query error: {e}")
        return 'ru'

async def update_user_language(telegram_id: int, language: str) -> bool:
    """Обновляет язык пользователя"""
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                "UPDATE users SET language = ? WHERE telegram_id = ?",
                (language, telegram_id))
            await db.commit()
            return True
    except aiosqlite.Error as e:
        print(f"Language update error: {e}")
        return False

async def update_last_active(telegram_id: int) -> bool:
    """Обновляет время последней активности"""
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await db.execute(
                "UPDATE users SET last_active = ? WHERE telegram_id = ?",
                (now, telegram_id))
            await db.commit()
            return True
    except aiosqlite.Error as e:
        print(f"Last active update error: {e}")
        return False
    

