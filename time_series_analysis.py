import json
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from collections import defaultdict
from datetime import datetime
from io import BytesIO
from telegram import Bot
import sys

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

# Анализ временных рядов
plt.figure(figsize=(12, 12))

# Raw Data
plt.subplot(4, 1, 1)
plt.plot(dates, message_counts, label='Сырые данные')
plt.ylabel('Количество сообщений')
plt.title('Активность чата')
x_ticks = range(0, len(dates), max(1, len(dates)//10))
plt.xticks(x_ticks, [dates[i] for i in x_ticks], rotation=45)
plt.legend()

# Trend
plt.subplot(4, 1, 2)
trend = np.convolve(message_counts, np.ones(7) / 7, mode='valid')
plt.plot(dates[3:-3], trend, label='Тренд', color='orange')
plt.ylabel('Количество сообщений')
plt.title('Трендовая составляющая')
x_ticks = range(0, len(dates), max(1, len(dates)//10))
plt.xticks(x_ticks, [dates[i] for i in x_ticks], rotation=45)
plt.legend()

# Seasonal
if len(dates) >= 14:  # Минимум 14 наблюдений для сезонного декомпозирования
    result = seasonal_decompose(message_counts, model='additive', period=7)
    plt.subplot(4, 1, 3)
    plt.plot(dates, result.seasonal, label='Сезонность', color='green')
    plt.ylabel('Количество сообщений')
    plt.title('Сезонная составляющая')
    x_ticks = range(0, len(dates), max(1, len(dates)//10))
    plt.xticks(x_ticks, [dates[i] for i in x_ticks], rotation=45)
    plt.legend()

# Residual
plt.subplot(4, 1, 4)
residual = message_counts[3:-3] - trend
plt.plot(dates[3:-3], residual, label='Остаток', color='red')
plt.ylabel('Количество сообщений')
plt.title('Остаточная составляющая')
x_ticks = range(0, len(dates), max(1, len(dates)//10))
plt.xticks(x_ticks, [dates[i] for i in x_ticks], rotation=45)
plt.legend()

plt.tight_layout()

# Сохранение графика в буфер
image_buffer = BytesIO()
plt.savefig(image_buffer, format='png')
image_buffer.seek(0)

# Отправка графика
chat_id = sys.argv[1]
bot_token = sys.argv[2]
bot = Bot(token=bot_token)
bot.send_photo(chat_id=chat_id, photo=image_buffer)