import logging
import json
import os
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import matplotlib
matplotlib.use('Agg')

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define constants for the different states in the conversation
UPLOAD_CHAT_HISTORY, END = range(2)

def get_bot_token_from_config_file(config_file='config.json'):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
            return config.get('bot_token')
    except Exception as e:
        print(f"An error occurred while reading the config file: {e}")
        return None

def start(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("Привет! Я бот, который анализирует статистику чата. Пожалуйста, экспортируйте историю вашего чата в формате JSON и отправьте мне файл с помощью команды /upload.")
    return UPLOAD_CHAT_HISTORY

def upload_chat_history(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("Ожидаю файл истории чата в формате JSON.")
    return UPLOAD_CHAT_HISTORY

def handle_chat_history(update: Update, context: CallbackContext, bot_token: str) -> int:
    if update.message.document.mime_type == "application/json":
        file = update.message.document.get_file()
        file.download('chat_history.json')
        update.message.reply_text("Файл истории чата успешно загружен. Обрабатываю...")
        
        # Запускаем сабпроцессы
        try:
            subprocess.run(["python", "top.py", str(update.effective_chat.id), bot_token], check=True)
            subprocess.run(["python", "days_stats.py", str(update.effective_chat.id), bot_token], check=True)
            subprocess.run(["python", "time_series_analysis.py", str(update.effective_chat.id), bot_token], check=True)
            subprocess.run(["python", "top_words.py", str(update.effective_chat.id), bot_token], check=True)
        except subprocess.CalledProcessError:
            update.message.reply_text("Произошла ошибка при обработке данных.")
            return END
        
        # Удаляем файл после того как все сабпроцессы завершились
        os.remove('chat_history.json')
        
    else:
        update.message.reply_text("Пожалуйста, загрузите файл в формате JSON.")
    return END

def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("Операция отменена.")
    return END

def main():
    # Get the bot token from config file
    bot_token = get_bot_token_from_config_file()

    if bot_token is None:
        print("Bot token not found. Please ensure the config file contains the bot token.")
        return
    
    try:
        # Create the Updater, pass it your bot's token.
        updater = Updater(bot_token)
    except Exception as e:
        print(f"An error occurred while initializing the bot: {e}")
        return

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with states
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        UPLOAD_CHAT_HISTORY: [
            CommandHandler('upload', upload_chat_history),
            CommandHandler('cancel', cancel),
            MessageHandler(Filters.document.mime_type("application/json"), lambda update, context: handle_chat_history(update, context, bot_token)),
        ],
        END: [
            CommandHandler('upload', upload_chat_history),
            CommandHandler('cancel', cancel),
        ],
    },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)

    # Log errors
    dp.add_error_handler(logger.error)

    # Start the Bot
    updater.start_polling()

    logger.info("Bot started. Listening for updates...")

    # Run the bot until you send a signal with Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
