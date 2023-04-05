# Скрипт для отправки уведомления о проверке работ

## Цели проекта

* С помощью API получать сообщение о проверке работ.
* Отправлять с помощью Telegram бота уведомление о проверке работ.

> Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

## Конфигурации

* Python version: 3.10
* Libraries: requirements.txt

## Запуск

- Скачайте код
- Установите библиотеки командой:

```bash
pip install -r requirements.txt
```

- Запишите переменные окружения в файле `.env` в формате `КЛЮЧ=ЗНАЧЕНИЕ`

```bash
TELEGRAM_API_TOKEN=... #Токен полученный на https://telegram.me/BotFather
TELEGRAM_CHAT_ID=... #Chat id канала @someone_chat
DEVMAN_API_TOKEN=... #Персональный токен dvmn.org https://dvmn.org/api/docs/
SLEEP_TIME=... #Время задержки между повторным запросом в случае ошибки
```

- Запустить скрипт

```bash
python3 main.py
```

## Run with Docker

- Download code
- Set environment variables in `.env` file in current directory in `KEY=VALUE` format
- Build an image from a Dockerfile:
```bash
docker build -t dvmn_notifications .
```
- Create and run a new container from an image:
```bash
docker run dvmn_notifications # you can add -d option to run container in background and print container ID
```
P.S.
- To show list of containers:
```bash
docker ps # you can copy id
```
- To stop container
```bash
docker stop [OPTIONS] CONTAINER [CONTAINER...]
```

## Деплой
Деплой можно осуществить на [heroku](https://id.heroku.com/login).

Для этого там необходимо: 
* Зарегестировать аккаунт и создать приложение. 
* Интегрировать код из собственного репозитория на GitHub.
* В репозитории необходим файл `Procfile` в котором прописано:
```bash
bot: python3 main.py
```
* Во вкладке `Settings` -> `Config Vars` прописать переменные окружения из `.env`.
* Во вкладке `Deploy` произвести деплой.
* Для удобства отслеживания логов можно установить `Heroku CLI`.
* Для подключения приложения в `CLI` прописать 
```bash
heroku login
heroku git:remote -a app_name
heroku logs --tail
```

## Deploy with Docker

* Go to the directory where you place main.py
* Login with command:
```bash
heroku login
heroku container:login
```
* Build and push an image with command:
```bash
heroku container:push --app <HEROKU_APP_NAME> worker
```
* Create a new release with command:
```bash
heroku container:release --app <HEROKU_APP_NAME> worker
```
* In `Resources` on `Heroku` activate worker with your Dynos
* Watch logs with command:
```bash
heroku logs --tail --app <HEROKU_APP_NAME>
```