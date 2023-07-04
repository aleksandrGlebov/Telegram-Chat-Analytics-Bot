import json
import matplotlib.pyplot as plt
import sys
from collections import defaultdict
from datetime import datetime
from io import BytesIO
from telegram import Bot

def create_and_send_chart(data, chat_id, bot_token, title, is_max=True):
    date_message_count = defaultdict(int)
    date_format = "%Y-%m-%d"
    for message in data['messages']:
        timestamp = message.get('date')
        if timestamp:
            date = datetime.fromisoformat(timestamp)
            formatted_date = date.strftime(date_format)
            date_message_count[formatted_date] += 1

    sorted_counts = sorted(date_message_count.items(), key=lambda x: (-x[1] if is_max else x[1]))[:5]
    top_dates = [date for date, _ in sorted_counts]
    message_counts = [count for _, count in sorted_counts]

    plt.figure(figsize=(12, 6))
    plt.bar(top_dates, message_counts)
    plt.xlabel('Дата')
    plt.ylabel('Количество сообщений')
    plt.title(title)

    plt.tight_layout()
    
    # Save the chart to a byte buffer
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png')
    image_buffer.seek(0)
    
    # Send the chart
    bot = Bot(token=bot_token)
    bot.send_photo(chat_id=chat_id, photo=image_buffer)


if __name__ == "__main__":
    chat_id = int(sys.argv[1])
    bot_token = sys.argv[2]

    with open('chat_history.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create and send the chart for maximum messages
    create_and_send_chart(data, chat_id, bot_token, 'Топ 5 дат с наибольшим количеством сообщений', is_max=True)
    
    # Create and send the chart for minimum messages
    create_and_send_chart(data, chat_id, bot_token, 'Топ 5 дат с наименьшим количеством сообщений', is_max=False)