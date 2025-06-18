# Yatube API

**Документация к API проекта Yatube (v1)**

## Описание
Проект **Yatube** — это простая социальная сеть для публикации текстовых постов, комментариев и подписок на авторов. Пользователи могут создавать публикации, комментировать их, подписываться на других авторов и просматривать контент в различных сообществах.

## Технологический стек
- Python 3.7+
- Django 5.1.1
- Django REST Framework 3.15.2
- Djoser 2.3.1 (JWT аутентификация)
- djangorestframework-simplejwt 5.4.0
- Pillow 11.0.0 (обработка изображений)
- Pytest 8.3.3 (тестирование)
- Flake8 7.1.1 (линтинг)
- SQLite (база данных по умолчанию)

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone git@github.com:vasiliy-924/api-final-yatube.git
   cd api-final-yatube
   ```
2. Cоздайте виртуальное окружение и активируйте его:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Выполните миграции и создайте суперпользователя:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```

## Тестирование API
Для тестирования API вы можете использовать:
1. Postman-коллекцию из директории `postman_collection/`
2. curl-запросы (примеры ниже)
3. Встроенный интерфейс DRF по адресу `http://localhost:8000/api/v1/`

## Примеры запросов
### Получение списка постов с пагинацией
```bash
curl -X GET "http://localhost:8000/api/v1/posts/?limit=5&offset=10" \
     -H "Authorization: Bearer <your_access_token>"
```

### Создание нового поста
```bash
curl -X POST "http://localhost:8000/api/v1/posts/" \
     -H "Authorization: Bearer <your_access_token>" \
     -H "Content-Type: application/json" \
     -d '{ "text": "Hello, Yatube!", "group": 1 }'
```

### Добавление комментария к публикации
```bash
curl -X POST "http://localhost:8000/api/v1/posts/5/comments/" \
     -H "Authorization: Bearer <your_access_token>" \
     -H "Content-Type: application/json" \
     -d '{ "text": "Great post!" }'
```

### Подписка на автора
```bash
curl -X POST "http://localhost:8000/api/v1/follow/" \
     -H "Authorization: Bearer <your_access_token>" \
     -H "Content-Type: application/json" \
     -d '{ "following": "author_username" }'
```

---

## Эндпоинты API

### Публикации (Posts)

- **GET /api/v1/posts/**  
  Получить список публикаций с поддержкой пагинации (`limit` и `offset`).  
  Ответ:
  ```json
  {
    "count": 123,
    "next": "http://.../?offset=10&limit=5",
    "previous": null,
    "results": [
      { "id": 0, "author": "user1", "text": "...", "pub_date": "2021-10-14T...Z", "image": null, "group": null }
    ]
  }
  ```

- **POST /api/v1/posts/**  
  Создать публикацию. Только авторизованные.  
  Body:
  ```json
  { "text": "Текст", "group": 1, "image": "<binary>" }
  ```  
  Ответы: `201 Created`, `400 Bad Request`, `401 Unauthorized`.

- **GET /api/v1/posts/{id}/**, **PUT**, **PATCH**, **DELETE**  
  Операции над одной публикацией. Ограничения: анонимным запрещено писать, редактировать/удалять может только автор.

### Комментарии (Comments)

- **GET /api/v1/posts/{post_id}/comments/**  
  Получить комментарии публикации.  
  Ответ: `200 OK` - массив объектов Comment или `404 Not Found`.

- **POST /api/v1/posts/{post_id}/comments/**  
  Добавить комментарий. Только авторизованные.  
  Ответы: `201 Created`, `400 Bad Request`, `401 Unauthorized`, `404 Not Found`.

- **GET /api/v1/posts/{post_id}/comments/{id}/**  
  Получить комментарий.  
  Ответы: `200 OK`, `404 Not Found`.

- **PUT /api/v1/posts/{post_id}/comments/{id}/**  
  Обновить комментарий. Только автор.  
  Ответы: `200 OK`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`.

- **PATCH /api/v1/posts/{post_id}/comments/{id}/**  
  Частично обновить комментарий. Только автор.  
  Ответы: `200 OK`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`.

- **DELETE /api/v1/posts/{post_id}/comments/{id}/**  
  Удалить комментарий. Только автор.  
  Ответы: `204 No Content`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`.

### Сообщества (Groups)

- **GET /api/v1/groups/**  
  Список сообществ.  
  Ответ: `200 OK` - массив объектов Group.

- **GET /api/v1/groups/{id}/**  
  Информация о сообществе по ID.  
  Ответы: `200 OK`, `404 Not Found`.

### Подписки (Follow)

- **GET /api/v1/follow/**  
  Список подписок текущего пользователя.  
  Поддерживает поиск по параметру `search`.  
  Ответ: `200 OK` - массив объектов Follow или `401 Unauthorized`.

- **POST /api/v1/follow/**  
  Подписаться на пользователя.  
  Body: `{ "following": "username" }`.  
  Ответы: `201 Created`, `400 Bad Request`, `401 Unauthorized`.

### Аутентификация (JWT)

API использует JWT-аутентификацию через библиотеку djoser:

- **POST /api/v1/jwt/create/** — получить `access` и `refresh` токены.  
- **POST /api/v1/jwt/refresh/** — обновить `access` токен.  
- **POST /api/v1/jwt/verify/** — проверить токен.

---

## Компоненты (schemas)

- **Post**: `id` (int), `author` (string), `text` (string), `pub_date` (datetime), `image` (binary|null), `group` (int|null).  
- **Comment**: `id`, `author`, `text`, `created`, `post`.  
- **Group**: `id`, `title`, `slug`, `description`.  
- **Follow**: `user` (string, readOnly), `following` (string).  
- **TokenObtainPair**: `username`, `password`.  
- **Token**: `refresh`, `access`.  
- **TokenRefresh**: `refresh`.  
- **TokenVerify**: `token`.

---

## Автор
**Василий Петров** - [GitHub https://github.com/vasiliy-924](https://github.com/vasiliy-924)
