# API для опросов


### Инструменты разработки

**Стек:**
- Python >= 3.9
- Django >= 3.2.7
- Postgres

## Старт

#### 1) В корне проекта создать .env

    DEBUG=1
    SECRET_KEY=vyug78g87gt67g8
    ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=polls_db
    SQL_USER=polls-user
    SQL_PASSWORD=admin123
    SQL_HOST=db
    SQL_PORT=5432
    DATABASE=postgres

#### 2) В корне проекта создать .env.db

    POSTGRES_DB=polls_db
    POSTGRES_USER=polls-user
    POSTGRES_PASSWORD=admin123

#### 3) Создать образ

    docker-compose build

#### 4) Запустить контейнер

    docker-compose up
    
#### 5) Перейти по адресу

    http://127.0.0.1:8000/swagger/

## Документация

#### Метод /api/polls/

Тип: GET

Метод возвращает все активные опросы

Параметры ответа:

| Параметр | Тип | Описание |
| ------------- | ------------------ | ----- |
| id | int | ID опроса |
| name |string | Название опроса |
| start_date | string | Дата старта |
| end_date | string | Дата окончания |
| description | string | Описание |

### Метод /api/polls/{poll_id}/questions/{id}/answer/

Тип: POST

Метод создает ответ для вопроса

Параметры запроса:

| Параметр | Тип | Обязательный | Описание |
| ------------- | ------------------ | ----- | ----- |
| user_id |int | Да | ID пользователя |
| answer | string | Нет | Ответ в виде текста |
| selected_answers | array | Нет | Выбранные ответы |

Параметры ответа:

| Параметр | Тип | Описание |
| ------------- | ------------------ | ----- |
| id | int | ID ответа |
| user_id |int | ID пользователя |
| answer | string | Ответ в виде текста |
| selected_answers | array | Выбранные ответы |

### Метод /api/polls/users/{user_id}/answers/

Тип: GET

Метод возвращает все ответы определенного пользователя

Параметры ответа:

| Параметр | Тип | Описание |
| ------------- | ------------------ | ----- |
| id | int | ID ответа |
| user_id |int | ID пользователя |
| answer |string | Ответ в виде текста |
| selected_answers | array | Выбранные ответы |
| question |obj | Объект вопроса |