import aiosqlite
from datetime import datetime

class AsyncAIDatabase:
    def __init__(self, db_path: str = 'data/ai_tokens.db'):
        self.db_path = db_path

    async def ai_init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            # Обновленная таблица user_tokens
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_tokens (
                    user_id INTEGER PRIMARY KEY,
                    user_name TEXT,
                    first_name TEXT,
                    date TEXT NOT NULL,
                    used_tokens INTEGER DEFAULT 0
                )
            """)
            
            # Обновленная таблица user_queries
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    user_name TEXT,
                    first_name TEXT,
                    query TEXT NOT NULL,
                    response TEXT,
                    tokens_used INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES user_tokens(user_id)
                )
            """)
            await db.commit()

    async def update_user_info(self, user_id: int, user_name: str = None, first_name: str = None):
        """Обновляет информацию о пользователе в обеих таблицах"""
        async with aiosqlite.connect(self.db_path) as db:
            # Обновляем user_tokens
            await db.execute(
                """
                INSERT INTO user_tokens (user_id, user_name, first_name, date, used_tokens)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    user_name = excluded.user_name,
                    first_name = excluded.first_name
                """,
                (user_id, user_name, first_name, datetime.now().strftime('%Y-%m-%d'), 0)
            )

            await db.commit()

    async def get_user_tokens(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT date, used_tokens FROM user_tokens WHERE user_id = ?",
                (user_id,)
            )
            result = await cursor.fetchone()
            return (datetime.now().date(), 0) if result is None else (
                datetime.strptime(result[0], '%Y-%m-%d').date(),
                result[1]
            )

    async def update_tokens(self, user_id: int, tokens: int, user_name: str = None, first_name: str = None):
        today = datetime.now().strftime('%Y-%m-%d')
        async with aiosqlite.connect(self.db_path) as db:
            # Обновляем с информацией о пользователе
            await db.execute(
                """
                INSERT INTO user_tokens (user_id, user_name, first_name, date, used_tokens)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    date = excluded.date,
                    used_tokens = used_tokens + excluded.used_tokens
                """,
                (user_id, user_name, first_name, today, tokens)
            )
            await db.commit()

    async def log_query(self, user_id: int, query: str, response: str, tokens: int, 
                       user_name: str = None, first_name: str = None):
        async with aiosqlite.connect(self.db_path) as db:
            # Добавляем новый запрос с информацией о пользователе
            await db.execute(
                """
                INSERT INTO user_queries 
                (user_id, user_name, first_name, query, response, tokens_used, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, user_name, first_name, query, response, tokens, datetime.now().isoformat())
            )
            # Проверяем количество запросов
            cursor = await db.execute(
                "SELECT COUNT(*) FROM user_queries WHERE user_id = ?",
                (user_id,)
            )
            count = (await cursor.fetchone())[0]
            
            # Удаляем старые запросы, если больше 10
            if count > 10:
                await db.execute(
                    """
                    DELETE FROM user_queries 
                    WHERE id IN (
                        SELECT id FROM user_queries 
                        WHERE user_id = ? 
                        ORDER BY timestamp ASC
                        LIMIT ?
                    )
                    """,
                    (user_id, count - 10)
                )
            
            await db.commit()

    async def get_user_queries(self, user_id: int, limit: int = 10):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                SELECT query, response, tokens_used, timestamp 
                FROM user_queries 
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (user_id, limit)
            )
            return await cursor.fetchall()

    async def reset_daily_limits(self):
        today = datetime.now().strftime('%Y-%m-%d')
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE user_tokens SET date = ?, used_tokens = 0 WHERE date != ?",
                (today, today)
            )
            await db.commit()