# TeamFinder — Платформа для поиска команд

Сервис, который помогает разработчикам и дизайнерам находить друг друга для совместной работы над пет-проектами. Здесь можно запитчить свою идею, собрать команду или просто присоединиться к существующему проекту.

## Основные возможности

*   **Система навыков**: Добавление и удаление навыков в профиле через AJAX.
*   **Умный поиск**: Подсказки при вводе навыков и возможность создания новых на лету.
*   **Фильтрация участников**: Поиск пользователей по технологиям.
*   **Управление проектами**: Создание, редактирование и закрытие проектов.
*   **Авто-аватарки**: Генерация аватарок с первой буквой имени при регистрации.
*   **Админ-панель**: Расширенная настройка для управления пользователями, проектами и навыками.

## Стек технологий

*   **Backend**: Python 3.x, Django 5.x
*   **Database**: PostgreSQL
*   **Frontend**: HTML5, CSS3, JavaScript (AJAX)
*   **Tools**: Docker, Docker Compose, Pillow (генерация аватаров)

## Как запустить проект

### 1. Подготовка

Клонируйте репозиторий и создайте виртуальное окружение:

```bash
git clone https://github.com/5belman5/team-finder-ad-main.git
cd team-finder-ad-main
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
# или
venv\Scripts\activate  # Для Windows
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

### 2. База данных

Проект настроен на работу с PostgreSQL через Docker. Запустите контейнеры:

```bash
docker-compose up -d
```

### 3. Настройки окружения

Создайте файл `.env` в корне проекта на основе `.env_example`:

```env
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=team_finder
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 4. Запуск

Примените миграции и запустите сервер:

```bash
python manage.py migrate
python manage.py runserver
```

Проект будет доступен по адресу: http://127.0.0.1:8000/

## Автор

**Иван Мещеряков**
*   GitHub: [5belman5](https://github.com/5belman5)
*   Email: [belvanic2000@gmail.com](mailto:belvanic2000@gmail.com)
