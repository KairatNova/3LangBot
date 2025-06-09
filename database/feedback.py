import aiosqlite
from datetime import datetime, time
DB_NAME = 'data/feedback.db'
ADMIN = 647302816
# Инициализация БД
async def feedback_data():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                message TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()


async def check_feedback_limits(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        # Общее количество отзывов пользователя
        cursor = await db.execute(
            'SELECT COUNT(*) FROM feedback WHERE user_id = ?',
            (user_id,)
        )
        total_count = await cursor.fetchone()
        total_count = total_count[0] if total_count else 0
        if not ADMIN:

            if total_count >= 6:
                return False, "Вы исчерпали лимит отзывов (максимум 6)."
        
        # Количество отзывов за сегодня
        today = datetime.now().date()
        today_start = datetime.combine(today, time.min).strftime('%Y-%m-%d 00:00:00')
        today_end = datetime.combine(today, time.max).strftime('%Y-%m-%d 23:59:59')
        
        cursor = await db.execute(
            '''SELECT COUNT(*) FROM feedback 
               WHERE user_id = ? 
               AND date(created_at) BETWEEN date(?) AND date(?)''',
            (user_id, today_start, today_end)
        )
        today_count = await cursor.fetchone()
        today_count = today_count[0] if today_count else 0
        if not ADMIN:
            if today_count >= 2:
                return False, "Вы можете оставить только 2 отзыва в день."
    
    return True, None


# Сохранение отзыва
async def save_feedback(user_id: int, username: str, message: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO feedback (user_id, username, message)
            VALUES (?, ?, ?)
        ''', (user_id, username, message))
        await db.commit()