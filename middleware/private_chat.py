from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Awaitable, Any

# Мидлварь для игнорирования сообщений в группах
class IgnoreGroupMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Message, data: dict) -> Any:
        if event.chat.type != "private":
            return  # Игнорируем, если не личный чат
        return await handler(event, data)
