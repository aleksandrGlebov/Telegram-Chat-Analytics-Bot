import json
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import matplotlib.pyplot as plt
from telegram import Bot
from io import BytesIO
import sys

# Загрузка данных
with open('chat_history.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Сбор всех сообщений в одну строку
all_messages = " ".join(message['text'] for message in data['messages'] if isinstance(message.get('text'), str))

# Преобразование сообщений в нижний регистр
all_messages = all_messages.lower()

# Удаление знаков препинания и других символов
all_messages = re.sub(r'\W', ' ', all_messages)

# Токенизация слов
words = word_tokenize(all_messages)

# Удаление стоп-слов
stop_words = set(stopwords.words('russian'))
words = [word for word in words if word not in stop_words]

# Подсчет частоты слов
word_count = Counter(words)

# Получение 10 наиболее часто встречающихся слов
most_common_words = word_count.most_common(10)

# Создание графика
words, frequencies = zip(*most_common_words)
plt.figure(figsize=(10, 6))
plt.barh(words, frequencies, color='skyblue')
plt.xlabel("Частота")
plt.title("Топ-10 самых часто употребляемых слов")
plt.gca().invert_yaxis()

# Сохранение графика в буфер
image_buffer = BytesIO()
plt.savefig(image_buffer, format='png')
image_buffer.seek(0)

# Отправка графика
chat_id = sys.argv[1]
bot_token = sys.argv[2]
bot = Bot(token=bot_token)
bot.send_photo(chat_id=chat_id, photo=image_buffer)