# Yatube API

## Описание
Yatube API — это RESTful API для социальной сети Yatube, предоставляющее удобные инструменты для работы с постами, комментариями, группами и подписками. Основные возможности:
- CRUD для постов (создание, чтение, обновление, удаление).
- Управление комментариями.
- Просмотр групп и их описаний.
- Подписки на пользователей.

API защищен с помощью JWT-аутентификации и возвращает данные в формате JSON.

## Установка и запуск

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/Davmgiz/api_final_yatube.git
   cd api_final_yatube
   ```
2. Создайте и активируйте виртуальное окружение:
  ```bash
  python -m venv venv
  venv\Scripts\activate     # Для Windows
  source venv/bin/activate  # Для Linux/MacOS
  ```
3. Установите зависимости:
  ```bash
  pip install -r requirements.txt
  ```
4. Примените миграции:
  ```bash
  python manage.py migrate
  ```
5. Запустите сервер:
  ```bash
  python manage.py runserver
  ```

