import os
import io
import sys
import json
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from statsmodels.tsa.seasonal import seasonal_decompose
from telegram import Bot

# Аргументы переданные из главного сценария
chat_id = int(sys.argv[1])
bot_token = sys.argv[2]

# Загрузка данных
with open('chat_history.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Подсчет количества сообщений по датам
date_message_count = defaultdict(int)
date_format = "%Y-%m-%d"
for message in data['messages']:
    timestamp = message.get('date')
    if timestamp:
        # Преобразование временной метки в объект datetime
        date = datetime.fromisoformat(timestamp)
        # Форматирование даты
        formatted_date = date.strftime(date_format)
        date_message_count[formatted_date] += 1

# Сортировка по датам
sorted_counts = sorted(date_message_count.items())
dates, message_counts = zip(*sorted_counts)

# Проверка наличия достаточного количества данных
if len(message_counts) >= 14:
    # Декомпозиция временного ряда
    result = seasonal_decompose(message_counts, model='additive', period=7)

    # Построение графиков
    plt.figure(figsize=(10, 8))

    plt.subplot(411)
    plt.plot(result.trend)
    plt.xlabel('Время')
    plt.ylabel('Тренд')
    plt.title('Тренд: Как меняется активность чата со временем')

    plt.subplot(412)
    plt.plot(result.seasonal)
    plt.xlabel('Время')
    plt.ylabel('Сезонность')
    plt.title('Сезонность: Регулярные изменения активности (например, по дням недели)')

    plt.subplot(413)
    plt.plot(result.resid)
    plt.xlabel('Время')
    plt.ylabel('Остатки')
    plt.title('Остатки: Нерегулярные изменения, не объясненные трендом и сезонностью')

    plt.tight_layout()

    # Save the chart to a bytes buffer
    image_buffer = io.BytesIO()
    plt.savefig(image_buffer, format='png')
    image_buffer.seek(0)

    # Send the chart
    bot = Bot(token=bot_token)
    bot.send_photo(chat_id=chat_id, photo=image_buffer)
else:
    print("Недостаточно данных для анализа сезонности.")