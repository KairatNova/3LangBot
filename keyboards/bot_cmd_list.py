from aiogram.types import BotCommand

private = [
    BotCommand(command='start', description='Запуск бота'),
    BotCommand(command="help", description='Помощь'),
    BotCommand(command='menu', description='Меню сервисов'),
    BotCommand(command='chatgpt', description='ИИ Помощник '),
    BotCommand(command='profile', description='Ваш профиль'),
    BotCommand(command="define", description='Значение слов'),
    BotCommand(command='translate', description='Переводчик'),
    BotCommand(command="learn_words", description='Учить слова'),
    BotCommand(command="feedback", description='Оставить отзыв')

]