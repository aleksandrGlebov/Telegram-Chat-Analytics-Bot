import json
import matplotlib.pyplot as plt
from collections import defaultdict

with open('result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

user_message_count = defaultdict(int)
for message in data['messages']:
    user = message.get('from', message.get('actor', 'Неизвестный')) 
    user_message_count[user] += 1

top_users = sorted(user_message_count.items(), key=lambda x: -x[1])[:20]
users, message_counts = zip(*top_users)

plt.figure(figsize=(10, 10))
plt.barh(users, message_counts, color='skyblue')
plt.xlabel('Количество сообщений')
plt.ylabel('Пользователи')
plt.title('Топ-20 пользователей по количеству сообщений')
plt.gca().invert_yaxis()  # чтобы наиболее активные пользователи были вверху
plt.show()