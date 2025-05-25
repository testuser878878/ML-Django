from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from ml_model.model_module import predict_glucose_level

import os

load_dotenv(dotenv_path="property.env")

# Создаём папку для временного хранения документов
os.makedirs("temp_docs", exist_ok=True)

# Функция приветствия
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помогу предсказать риск диабета. Просто отправь уровень глюкозы в крови (например, 110)."
    )


# Функция обработки текста
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        glucose_level = float(update.message.text)  # Преобразуем текст в число
        result = predict_glucose_level(glucose_level)  # Получаем результат от модели
        await update.message.reply_text(f"Прогноз: {result}")  # Отправляем результат пользователю
    except ValueError:
        await update.message.reply_text("Пожалуйста, отправь число, представляющее уровень глюкозы.")


if __name__ == "__main__":
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Обработчик команды /start
    app.add_handler(MessageHandler(filters.Command("start"), start))

    # Обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
