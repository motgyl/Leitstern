# Messenger с Chat, Tasks и AI

Полнофункциональное приложение для общения, управления задачами и взаимодействия с ИИ.

## Структура

После авторизации доступны:
- **Chat** - общее общение между пользователями
- **Tasks** - управление задачами (создание, решение, отслеживание статусов)
- **AI Chat** - личный чат с ИИ (Groq API)

## Запуск

### Сервер
```bash
# Установить зависимости (опционально для AI)
pip install -r requirements.txt

# Установить Groq API ключ (опционально)
export GROQ_API_KEY="ваш_ключ"

# Запустить сервер
python3 server.py
```

### Клиент (интерактивный)
```bash
python3 client.py localhost:7002
```

Или через netcat:
```bash
nc localhost 7002
```

## Команды

### Авторизация (без входа)
- `register <username> <password>` - регистрация
- `login <username> <password>` - вход
- `help` - справка
- `quit` - выход

### Chat (после входа)
- `chat send <message>` - отправить сообщение
- `chat view [count]` - просмотреть сообщения

### Tasks (после входа)
- `task create <title>` - создать задачу
- `task list` - список задач
- `task view <id>` - просмотр задачи
- `task add-desc <id>` - добавить описание
- `task add-sol <id>` - добавить решение
- `task status <id> <status>` - изменить статус (pending/in_progress/solved)
- `task delete <id>` - удалить задачу

### AI Chat (после входа)
- `ai <message>` - отправить сообщение AI
- `ai clear` - очистить историю AI

## Статусы задач

- **pending** - не решена
- **in_progress** - решается кем-то
- **solved** - решена

## Хранение данных

Все данные сохраняются в папке `data/`:
- `users.json` - пользователи и пароли
- `chat.json` - сообщения чата
- `tasks.json` - задачи
- `ai_chat.json` - история AI чатов по пользователям

## AI интеграция

Для работы AI необходимо:
1. Установить пакет: `pip install groq`
2. Получить API ключ на https://console.groq.com/
3. Установить переменную окружения: `export GROQ_API_KEY="ваш_ключ"`

AI использует свободную модель `mixtral-8x7b-32768` и хранит личную историю для каждого пользователя.

## Примеры использования

### Регистрация и вход
```
register alice password123
login alice password123
```

### Создание и решение задачи
```
task create "Написать документацию"
task list
task view <task_id>
task add-desc <task_id>
(введите описание, END на новой строке)
task status <task_id> in_progress
task add-sol <task_id>
(введите решение, END на новой строке)
task status <task_id> solved
```

### Чат
```
chat send "Привет всем!"
chat view 10
```

### AI Chat
```
ai "Что такое машинное обучение?"
ai clear
```
