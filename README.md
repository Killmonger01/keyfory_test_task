# 👤 User Management API

RESTful API для управления пользователями, созданный с использованием асинхронного стека: Litestar, SQLAlchemy и PostgreSQL.  
Проект полностью контейнеризирован с помощью Docker и запускается одной командой.

---

## 🚀 Стек технологий

- [Litestar](https://docs.litestar.dev/latest/) — асинхронный Python веб-фреймворк
- [SQLAlchemy (Async)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) — ORM для работы с БД
- [PostgreSQL](https://www.postgresql.org/) — реляционная СУБД
- [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/) — контейнеризация приложения
- [Msgspec](https://jcristharif.com/msgspec/) — валидация и сериализация данных

---

## 📦 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/user-management-api.git
cd user-management-api
```
### 2. Настройка переменных окружения
Создайте файл .env в корне проекта со следующим содержимым:
```
DB_DRIVER=postgresql+asyncpg
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=user_db

HOST=0.0.0.0
PORT=8000
```
### 3. Запуск приложения
```bash
docker-compose up --build
```
---

> 💡 **Примечание для разработчиков**

Все зависимости автоматически устанавливаются внутри Docker-контейнера при сборке, поэтому локальная установка не требуется.

Однако, если вы хотите посмотреть код и иметь подсветку типов то 

можно создать виртуальное окружение вручную и установить зависимости из `requirements.txt`:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 🧾 Swagger-документация
Доступна по адресу:
👉 http://localhost:8000/schema/swagger
### 📚 Описание эндпоинтов

| Метод   | URL                | Описание                        |
|---------|--------------------|----------------------------------|
| `GET`   | `/api/users`       | Получить список пользователей   |
| `GET`   | `/api/users/{id}`  | Получить пользователя по ID     |
| `POST`  | `/api/users`       | Создать нового пользователя     |
| `PUT`   | `/api/users/{id}`  | Обновить пользователя           |
| `DELETE`| `/api/users/{id}`  | Удалить пользователя            |