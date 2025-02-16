1.Создание TCP-сервера:
•Реализуйте простой TCP-сервер, который слушает указанный порт и принимает входящие соединения.
•Сервер должен считывать сообщения от клиента и выводить их на экран.
•По завершении работы клиенту отправляется ответ с подтверждением получения сообщения.

2.Реализация TCP-клиента:
•Разработайте TCP-клиента, который подключается к вашему серверу.
•Клиент должен отправлять сообщение, введённое пользователем, и ожидать ответа.
•После получения ответа от сервера клиент завершает соединение.

3.Асинхронная обработка клиентских соединений:
•Добавьте в сервер многопоточную обработку нескольких клиентских соединений.
•Используйте горутины для обработки каждого нового соединения.
•Реализуйте механизм graceful shutdown: сервер должен корректно завершать все активные соединения при остановке.

4.Создание HTTP-сервера:
•Реализуйте базовый HTTP-сервер с обработкой простейших GET и POST запросов.
•Сервер должен поддерживать два пути:
•GET /hello — возвращает приветственное сообщение.
•POST /data — принимает данные в формате JSON и выводит их содержимое в консоль.

5.Добавление маршрутизации и middleware:
•Реализуйте обработку нескольких маршрутов и добавьте middleware для логирования входящих запросов.
•Middleware должен логировать метод, URL, и время выполнения каждого запроса.

6.Веб-сокеты:
•Реализуйте сервер на основе веб-сокетов для чата.
•Клиенты должны подключаться к серверу, отправлять и получать сообщения.
•Сервер должен поддерживать несколько клиентов и рассылать им сообщения, отправленные любым подключённым клиентом.

Запуск:
Скачать папку, открыть Visual Studio Code, ПКМ по папке с файлами и нажать открыть консоль, ввести команду go run названиефайла.go
Перед тем как запустить файл клиента нужно запустить файл сервера!


GET-запросы:

curl http://localhost:8080/hello
curl http://localhost:8080/goodbye


POST-запрос:

$headers = @{
    "Content-Type" = "application/json"
}
$data = @{
    "key" = "value"
    "message" = "Hello, server!"
} | ConvertTo-Json
$response = Invoke-WebRequest -Uri "http://localhost:8080/data" -Method Post -Headers $headers -Body $data
$response.Content