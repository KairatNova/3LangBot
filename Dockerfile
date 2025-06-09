# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Переменные окружения
ENV PYTHONUNBUFFERED=1

# Запуск бота
CMD ["python", "bot.py"]
