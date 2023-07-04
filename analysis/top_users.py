import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
from io import BytesIO
import sys
from telegram import Bot

def generate_and_send_chart(chat_id: int, bot_token: str) -> None:
    with open('chat_history.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_message_count = defaultdict(int)
    for message in data['messages']:
        user = message.get('from', message.get('actor', 'Неизвестный'))
        user_message_count[user] += 1

    top_users = sorted(user_message_count.items(), key=lambda x: -x[1])[:20]

    users = []
    message_counts = []
    for user, count in top_users:
        if user is not None and count is not None:
            users.append(user)
            message_counts.append(count)

    # Check if message_counts is empty
    if not message_counts:
        return

    plt.figure(figsize=(10, 10))
    plt.barh(users, message_counts, color='skyblue')
    plt.xlabel('Количество сообщений')
    plt.ylabel('Пользователи')
    plt.title('Топ-20 пользователей по количеству сообщений')
    plt.gca().invert_yaxis()

    # Save the chart to a byte buffer
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png')
    image_buffer.seek(0)

    # Send the chart
    bot = Bot(token=bot_token)
    bot.send_photo(chat_id=chat_id, photo=image_buffer)

if __name__ == '__main__':
    chat_id = sys.argv[1]
    bot_token = sys.argv[2]
    generate_and_send_chart(chat_id, bot_token)