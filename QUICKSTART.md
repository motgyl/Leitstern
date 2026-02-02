Messenger с Chat, Tasks и AI

СТРУКТУРА:
✓ Авторизация (регистрация, вход, выход)
✓ Chat (общие сообщения)
✓ Tasks (создание, описание, решение, статусы)
✓ AI Chat (Groq API, личная история для каждого)

ЗАПУСК:
python3 server.py          # Сервер (порт 7002)
python3 client.py localhost:7002   # Клиент

ПРИМЕРЫ:
register alice password123
login alice password123
chat send "Привет!"
task create "Моя задача"
ai "Что такое Python?"

ДАННЫЕ:
data/users.json     - пользователи
data/chat.json      - сообщения
data/tasks.json     - задачи
data/ai_chat.json   - AI чаты

AI КЛЮЧ:
export GROQ_API_KEY="ваш_ключ"
pip install groq

ПОРТ: 7002
