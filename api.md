# Изменения
Документ на данный момент является черновиком и будет обновляться по мере изменения API.
# Введение
API данного видеосервиса организовано следующим образом:
1. REST API  
    > Все запросы, адресуемые через REST API всегда идут по пути: `/api/v1/...`  
    > Далее запросы организованны по следующей структуре:
    > |          | Цель воздействия | Свойство воздействия | Действие |
    > |:--------:|:----------------:|:--------------------:|:--------:|
    > | /api/v1/ |      user/       |        name/         |  update  |
1. GraphQL
    > Для GraphQL существует 2 кроневых пути запросов:
    > * Для обычных запросов: `/api/v1/graphql`
    > * Для пакетных запросов: `/api/v1/graphql/batch`
    > Подробнее о схеме и структуре GraphQL запросов будет рассмотренно в [позднее](#GraphQL).


# REST API
Как было сказанно выше все запросы к REST API следуют стандартному паттерну:
|          | Цель воздействия | Свойство воздействия | Действие |
| :------: | :--------------: | :------------------: | :------: |
| /api/v1/ |      user/       |        name/         |  update  |

Следственно можно разделить запросы в группы по цели воздействия.
## Формат возвращаемых данных
Данные возвращаемые запросами имеют следующий формат:
```json
{
    "ok": true, // true - запрос выполнен успешно, false - произошла ошибка
    "msg": "string", // Дополнительная информация при успешном завершении запроса, если нет другой информации
    "error": "string", // Дополнительная информация при ошибке
    "exception": "string", // Редкий случай, когда произошла ошибка в коде, которая не была обработана
    ... // Любая другая информация в зависимости от запроса
}
```
При описании запроса в большинстве случаев будет приводится только положительный ответ и список взоможных ошибок, так как ошибки всегда имеют одинаковый формат.

## Группы запросов
Гапросы к REST API можно разделить на следующие группы:
1. [User](#user)  
    > Данная группа напрямую связанна с взаимодействием с данными полтзователя.
2. [Streaming](#streaming)  
    > Данная группа предназначена для функционала взаимодействия со стримом.
3. [Services](#services) 
    > Данная группа напрямую связанна с взаимодействием с небольшими фронтенд сервисами стрима.
4. [Bot](#bot)
    > Данная группа предназначена для удаленного входа по REST API. Методы данного раздела предназначены только для работы через API и не используются в фронтенде.
### User
1. #### **Авторизация**  
    ```http
    POST /api/v1/user/auth
    CSRF-Token: <token> // Csrf токен для защиты от CSRF атак
    Body: {
        "username": "username or email",
        "password": "password"
    }
    ``` 
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "msg": "User log in successfully!"
    }
    ```
    Возможные ошибки:
    * User not exists! - Пользователь не существует
    * Invalid password! - Неверный пароль
2. #### **Выход**  
    ```http
    POST /api/v1/user/exit
    CSRF-Token: <token> // Csrf токен для защиты от CSRF атак
    ``` 
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "msg": "User log out successfully!"
    }
    ```
    Ошибок для данного метода не предусмотрено.
3. #### **Регистрация**  
     ```http
     POST /api/v1/user/create
     CSRF-Token: <token> // Csrf токен для защиты от CSRF атак
     Body: {
          "username": "username",
          "email": "email",
          "password": "password"
     }
     ``` 
     В случае успеха возврашается сообщение:
     ```json
     {
          "ok": true,
          "msg": "User created successfully!"
     }
     ```
     Возможные ошибки:
     * Registration error! - Произошла ошибка регистрации. При данной ошибке в сообщении есть exception с информацией о том, что именно пошло не так. (пока так, пока не будет переписано api на neo4j)
4. #### **Изменение пароля**  
     ```http
     PATCH /api/v1/user/password/update
     Body: {
          "old_password": "old password",
          "new_password": "new password"
     }
     ``` 
     В случае успеха возврашается сообщение:
     ```json
     {
          "ok": true,
          "msg": "User password changed successfully!"
     }
     ```
     Возможные ошибки:
     * User not authorized! - Пользователь не авторизован
     * Invalid old password! - Неверный старый пароль
     * User password changing error! - Произошла ошибка изменения пароля. При данной ошибке в сообщении есть exception с информацией о том, что именно пошло не так. (пока так, пока не будет переписано api на neo4j)
5. #### **Изменение имени пользователя**  
     ```http
     PATCH /api/v1/user/username/update
     Body: {
          "username": "new username"
     }
     ``` 
     В случае успеха возврашается сообщение:
     ```json
     {
          "ok": true,
          "msg": "Username changed successfully!"
     }
     ```
     Возможные ошибки:
     * User not authorized! - Пользователь не авторизован
     * Username changing error! - Произошла ошибка изменения имени. При данной ошибке в сообщении есть exception с информацией о том, что именно пошло не так. (пока так, пока не будет переписано api на neo4j)
6. #### **Изменение email**  
     ```http
     PATCH /api/v1/user/email/update
     Body: {
          "email": "new email"
     }
     ``` 
     В случае успеха возврашается сообщение:
     ```json
     {
          "ok": true,
          "msg": "Email changed successfully!"
     }
     ```
     Возможные ошибки:
     * User not authorized! - Пользователь не авторизован
     * Email changing error! - Произошла ошибка изменения email. При данной ошибке в сообщении есть exception с информацией о том, что именно пошло не так. (пока так, пока не будет переписано api на neo4j)
7. #### **Создание профиля стримера**  
     ```http
     POST /api/v1/user/profile/create
     Body: {
          "stream_name": "name"
     }
     ``` 
     В случае успеха возврашается сообщение:
     ```json
     {
          "ok": true,
          "msg": "Streamer profile created successfully!"
     }
     ```
     Возможные ошибки:
     * User not authorized! - Пользователь не авторизован
     * Stream without name! - В аргументе не указано имя стрима
     * Streamer profile error! - Произошла ошибка создания профиля стримера. При данной ошибке в сообщении есть exception с информацией о том, что именно пошло не так. (пока так, пока не будет переписано api на neo4j)
8. #### **Получение токена стримера**
    ```http
    GET /api/v1/user/profile/token
    ``` 
    В случае успеха возврашается сообщение:
    ```json
    {
       "ok": true,
        "token": "<token>"
    }
    ```
    Возможные ошибки:
    * User not authorized! - Пользователь не авторизован
    * User not a streamer! - Профиль стримера не существует
9. #### **Регенерация токена стримера**
    ```http
    POST /api/v1/user/profile/token/regenerate
    ``` 
    В случае успеха возврашается сообщение:
    ```json
    {
       "ok": true,
       "msg": "Token regenerated successfully!"
    }
    ```
    Возможные ошибки:
    * User not authorized! - Пользователь не авторизован
    * User not a streamer! - Профиль стримера не существует
10. #### **Обновление имени стрима**
    ```http
    PATCH /api/v1/user/profile/name/update
    Body: {
        "stream_name": "new name"
    }
    ``` 
    В случае успеха возврашается сообщение:
    ```json
    {
       "ok": true,
       "msg": "Stream name changed successfully!"
    }
    ```
    Возможные ошибки:
    * User not authorized! - Пользователь не авторизован
    * Stream without name! - В аргументе не указано имя стрима
    * Stream name change error! - Произошла ошибка обновления имени стрима. При данной ошибке в сообщении есть exception с информацией о том, что именно пошло не так. (пока так, пока не будет переписано api на neo4j)
11. #### **Список подписок пользователя**
    ```http
        GET /api/v1/user/subscriptions
    ```
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "subscriptions": [
            "username1",
            "username2"
        ]
    }
    ```
    Возможные ошибки:
    * User not authorized! - Пользователь не авторизован
12. #### **Список ботов пользователя**
    ```http
        GET /api/v1/user/bots
    ```
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "bots": [
            "username1",
            "username2"
        ]
    }
    ```
    Возможные ошибки:
    * User not authorized! - Пользователь не авторизован
### Streaming
1. **Подписан ли пользователь**
    ```http
        GET /api/v1/stream/<streamer>/subscribers/contains
    ```
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "subscribed": true // true - подписан, false - не подписан
    }
    ```
    Возможные ошибки:
    * Streamer does not exist! - Стримера не существует
2. **Количество подписанных пользователей**
    ```http
        GET /api/v1/stream/<streamer>/subscribers/count
    ```
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "count": 10 // Количество подписанных пользователей
    }
    ```
    Возможные ошибки:
    * Streamer does not exist! - Стримера не существует
3. **Подписка на стримера**
    ```http
        POST /api/v1/stream/<streamer>/subscribers/subscribe
    ```
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "msg": "Subscribed!"
    }
    ```
    Возможные ошибки:
    * Streamer does not exist! - Стримера не существует
    * User not authorized! - Пользователь не авторизован
4. **Отписка от стримера**
    ```http
        POST /api/v1/stream/<streamer>/subscribers/unsubscribe
    ```
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "msg": "Unsubscribed!"
    }
    ```
    Возможные ошибки:
    * Streamer does not exist! - Стримера не существует
    * User not authorized! - Пользователь не авторизован
5. **Подключение к стриму**
    ```http
        POST /api/v1/stream/<streamer>/viewers/connect
    ```
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "msg": "Connected!"
    }
    ```
    Возможные ошибки:
    * Streamer does not exist! - Стримера не существует
6. **Отключение от стрима**
    ```http
        POST /api/v1/stream/<streamer>/viewers/disconnect
    ```
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "msg": "Disconnected!"
    }
    ```
    Возможные ошибки:
    * Streamer does not exist! - Стримера не существует
7. **Количество зрителей на стриме**
    ```http
        GET /api/v1/stream/<streamer>/viewers/count
    ```
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "count": 10 // Количество зрителей на стриме
    }
    ```
    Возможные ошибки:
    * Streamer does not exist! - Стримера не существует
8. **Список сообщений в чате**
    ```http
        GET /api/v1/stream/<streamer>/chat/list?limit=<limit>&end_timestamp=<timestamp>&start_timestamp=<timestamp>
    ```
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "messages": [
            {
                "user": "username",
                "content": "message",
                "timestamp": "timestamp" // Время отправки сообщения в формате я хз какой
            },
            {
                "user": "username",
                "content": "message",
                "timestamp": "timestamp" // Время отправки сообщения в формате я хз какой
            }
        ]
    }
    ```
    Возможные ошибки:
    * Streamer does not exist! - Стримера не существует
9. **Отправка сообщения в чат**
    ```http
        POST /api/v1/stream/<streamer>/chat/send
        Body: {
            "message": "message"
        }
    ```
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "msg": "Message sent!",
        "timestamp": "timestamp" // Время отправки сообщения в формате я хз какой
    }
    ```
    Возможные ошибки:
    * Streamer does not exist! - Стримера не существует
    * User not authorized! - Пользователь не авторизован
    * Content field is required! - Поле message обязательно для заполнения
### Services
Это еще не сделано. Когда будет сделано, то появится здесь и в изменениях.
### Bot
1. **Авторизация бота**  
    ```http
    POST /api/v1/bot/auth
    X-Api-Key: <api-key> // Api ключ для авторизации бота
    ``` 
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "msg": "Bot log in successfully!"
    }
    ```
    Возможные ошибки:
    * Bot not exists! - Бот не существует
2. **Выход бота**  
    ```http
    POST /api/v1/bot/exit
    X-Api-Key: <api-key> // Api ключ для авторизации бота
    ``` 
    В случае успеха возврашается сообщение:
    ```json
    {
        "ok": true,
        "msg": "Bot log out successfully!"
    }
    ```
    Возможные ошибки:
    * Bot not exists! - Бот не существует
    * Wrong bot credentials! - Неверные учетные данные бота
3. **Создание бота**  
     ```http
     POST /api/v1/bot/create
     Body: {
          "bot_username": "username",
          "bot_password": "password"
     }
     ``` 
     В случае успеха возврашается сообщение:
     ```json
     {
          "ok": true,
          "msg": "Bot created successfully!"
     }
     ```
     Возможные ошибки:
     * User not authorized! - Пользователь не авторизован
     * Bot user not exists! - Пользователь для которого пытаются привязать бота не существует
     * Bot user password invalid! - Неверный пароль пользователя для которого пытаются привязать бота
     * Bot creation error! - Произошла ошибка создания бота. При данной ошибке в сообщении есть exception с информацией о том, что именно пошло не так. (пока так, пока не будет переписано api на neo4j)
4. **Удаление бота**  
     ```http
     POST /api/v1/bot/remove
     Body: {
          "bot_username": "username",
          "bot_password": "password"
     }
     ``` 
     В случае успеха возврашается сообщение:
     ```json
     {
          "ok": true,
          "msg": "Bot removed successfully!"
     }
     ```
     Возможные ошибки:
     * User not authorized! - Пользователь не авторизован
     * Bot user not exists! - Пользователь с которого пытаются отвязать бота
     * Bot user password invalid! - Неверный пароль пользователя с которого пытаются отвязать бота
     * Bot removing error! - Произошла ошибка удаления бота. При данной ошибке в сообщении есть exception с информацией о том, что именно пошло не так. (пока так, пока не будет переписано api на neo4j)

# GraphQL
Модуль учета лицензий – сбор, регистрация и управление данными о лицензиях, контроль сроков действия и активации лицензий.
Модуль контроля соответствия – мониторинг соблюдения лицензионных соглашений, выявление случаев несанкционированного использования ПО.Ф
Модуль управления пользователями – настройка доступа и прав пользователей, управление учетными записями лицензиатов и администраторов.
Модуль взаимодействия с клиентами – прием заявок на лицензии, обработка запросов, предоставление информации о статусе лицензий.
Модуль базы данных – хранение информации о лицензиях, пользователях, программных продуктах и их версиях, обеспечение резервного копирования.
