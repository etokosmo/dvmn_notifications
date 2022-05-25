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
```

- Запустить скрипт

```bash
python3 main.py
```