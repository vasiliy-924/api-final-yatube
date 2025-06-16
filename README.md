# Yatube API

**Документация к API проекта Yatube (v1)**

## Описание
Проект **Yatube** — это простая социальная сеть для публикации текстовых постов, комментариев и подписок на авторов. Пользователи могут создавать публикации, комментировать их, подписываться на других авторов и просматривать контент в различных сообществах.

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/yatube-api.git
   cd yatube-api
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

## Примеры запросов
### Получение списка постов с пагинацией
```bash
curl -X GET "http://localhost:8000/api/v1/posts/?limit=5&offset=10"      -H "Authorization: Bearer <your_access_token>"
```

### Создание нового поста
```bash
curl -X POST "http://localhost:8000/api/v1/posts/"      -H "Authorization: Bearer <your_access_token>"      -H "Content-Type: application/json"      -d '{ "text": "Hello, Yatube!", "group": 1 }'
```

### Добавление комментария к публикации
```bash
curl -X POST "http://localhost:8000/api/v1/posts/5/comments/"      -H "Authorization: Bearer <your_access_token>"      -H "Content-Type: application/json"      -d '{ "text": "Great post!" }'
```

### Подписка на автора
```bash
curl -X POST "http://localhost:8000/api/v1/follow/"      -H "Authorization: Bearer <your_access_token>"      -H "Content-Type: application/json"      -d '{ "following": "author_username" }'
```

---

## Эндпоинты API

### Публикации (Posts)

- **GET /api/v1/posts/**  
  Получить список публикаций с поддержкой `limit` и `offset`.  
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
  Ответ: массив объектов Comment или `404`.

- **POST /api/v1/posts/{post_id}/comments/**  
  Добавить комментарий. Только авторизованные.  
  Body: `{ "text": "..." }`. Ответы: `201`, `400`, `401`, `404`.

- **GET/PUT/PATCH/DELETE /api/v1/posts/{post_id}/comments/{id}/**  
  Операции над комментарием. PUT/PATCH/DELETE — только автор.

### Сообщества (Groups)

- **GET /api/v1/groups/**  
  Список сообществ.

- **GET /api/v1/groups/{id}/**  
  Информация о сообществе по ID.

### Подписки (Follow)

- **GET /api/v1/follow/**  
  Список подписок текущего пользователя. `?search=<username>` для поиска по `following__username`.  
  Ответ: массив объектов Follow.

- **POST /api/v1/follow/**  
  Подписаться на пользователя.  
  Body: `{ "following": "username" }`.  
  Ответы: `201`, `400`, `401`.

### Аутентификация (JWT)

- **POST /api/v1/jwt/create/** — получить `access` и `refresh`.  
- **POST /api/v1/jwt/refresh/** — обновить `access`.  
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
