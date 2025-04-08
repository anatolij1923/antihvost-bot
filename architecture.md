### Архитектура бота

antihvost_bot/
│
├── bot.py                     # Точка входа — запуск бота
├── config.py                  # Конфигурации: токены, настройки БД и пр.
│
├── .env                       # Файл для хранения токена, конфиденциальной инфы
│
├── requirements.txt           # Зависимости проекта
│
├── handlers/                  # Обработчики команд
│   ├── __init__.py
│   ├── start.py               # /start, авторизация
│   ├── menu.py                # Главное меню
│   ├── labs.py                # Работа с лабораторными
│   ├── homework.py            # Работа с домашками
│   ├── rating.py              # Рейтинговая таблица
│
├── keyboards/                 # Клавиатуры (Reply и Inline)
│   ├── __init__.py
│   ├── main_menu.py
│   ├── labs_menu.py
│   └── rating_menu.py
│
├── states/                    # Состояния FSM (машины состояний)
│   ├── __init__.py
│   ├── auth_states.py         # Состояния для авторизации
│   ├── lab_states.py          # Состояния для ввода лаб
│   └── homework_states.py
│
├── database/                  # Работа с базой данных
│   ├── __init__.py
│   ├── models.py              # Описание таблиц (если SQLAlchemy)
│   ├── queries.py             # Основные SQL-запросы
│   └── db.py                  # Подключение к БД
│
├── utils/                     # Вспомогательные функции
│   ├── __init__.py
│   ├── validators.py          # Валидация ввода
│   ├── formatters.py          # Форматирование текста
│   └── logger.py              # Логирование
│
└── data/
    └── static/                # Фиксированные тексты, 3мотивации, анекдоты, хохотульки
