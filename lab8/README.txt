1.Построение базового REST API:
•Реализуйте сервер, поддерживающий маршруты:
•GET /users — получение списка пользователей.
•GET /users/{id} — получение информации о конкретном пользователе.
•POST /users — добавление нового пользователя.
•PUT /users/{id} — обновление информации о пользователе.
•DELETE /users/{id} — удаление пользователя.

2.Подключение базы данных:
•Добавьте базу данных (например, PostgreSQL или MongoDB) для хранения информации о пользователях.
•Модифицируйте сервер для взаимодействия с базой данных.

3.Обработка ошибок и валидация данных:
•Реализуйте централизованную обработку ошибок.
•Добавьте валидацию данных при создании и обновлении пользователей.

4.Пагинация и фильтрация:
•Добавьте поддержку пагинации и фильтрации по параметрам запроса (например, поиск пользователей по имени или возрасту).

5.Тестирование API:
•Реализуйте unit-тесты для каждого маршрута.
•Проверьте корректность работы при различных вводных данных.

6.Документация API:
•Создайте документацию для разработанного API с описанием маршрутов, методов, ожидаемых параметров и примеров запросов.

Запуск:
Скачать папку, открыть Visual Studio Code, ПКМ по папке с файлами и нажать открыть консоль, ввести команду go run названиефайла.go

///////Маршруты
Первая команда для командной строки, вторая для VSCode

1. Все пользователи (можно указать номер страницы и ограничение на кол-во вывода на странице)
curl -X GET http://localhost:8080/users
& "C:\Windows\System32\curl.exe" -X GET http://localhost:8080/users
& "C:\Windows\System32\curl.exe" -X GET "http://localhost:8080/users?page=2&limit=10"


2. Получить информацию о пользователе по его ID (вместо 1 писать id пользователя)
curl -X GET http://localhost:8080/users/1
& "C:\Windows\System32\curl.exe" -X GET http://localhost:8080/users/1

3. Создать нового пользователя (Все данные полей можно заменить на свои)
curl -X POST http://localhost:8080/users -H "Content-Type: application/json" -d "{\"fname\": \"Михаил\", \"sname\": \"Зубенко\", \"age\": 30, \"email\": \"mikhailzubenko@example.com\"}"
& "C:\Windows\System32\curl.exe" -X POST http://localhost:8080/users -H "Content-Type: application/json" -d '{\"fname\": \"Михаил\", \"sname\": \"Зубенко\", \"age\": 30, \"email\": \"mikhailzubenko@example.com\"}'

4. Обновить информацию пользователя по id (вместо 1 пишется id пользователя)
curl -X PUT http://localhost:8080/users/1 -H "Content-Type: application/json" -d "{\"fname\": \"Алексей\", \"sname\": \"Алексеев\", \"age\": 31, \"email\": \"alexeyalexeev@example.com\"}"
& "C:\Windows\System32\curl.exe" -X PUT http://localhost:8080/users/1 -H "Content-Type: application/json" -d '{\"fname\": \"Алексей\", \"sname\": \"Алексеев\", \"age\": 31, \"email\": \"alexeyalexeev@example.com\"}'

5. Удалить пользователя по id (вместо 1 пишется id пользователя)
curl -X DELETE http://localhost:8080/users/1
& "C:\Windows\System32\curl.exe" -X DELETE http://localhost:8080/users/1