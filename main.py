import asyncio

import requests
import telegram
from loguru import logger

from config import TELEGRAM_API_TOKEN, TELEGRAM_CHAT_ID, LONG_POLLING_URL, HEADERS, PATH_TO_LOGS, SLEEP_TIME


async def get_review(response):
    content = response.json().get("new_attempts")[0]
    is_negative = content.get("is_negative")
    lesson_title = content.get("lesson_title")
    lesson_url = content.get("lesson_url")
    valid_review_message = "К сожалению в работе нашлись ошибки." if is_negative else "Преподавателю все понравилось. \
    Можно приступать к следующему уроку."
    message = f"У Вас проверили работу '{lesson_title}'.\n\n{valid_review_message}\nСсылка на урок: {lesson_url}"
    await send_message(message)


async def main():
    timestamp = None
    while True:
        try:
            payload = {'timestamp': timestamp}
            response = requests.get(LONG_POLLING_URL, headers=HEADERS, params=payload)
            response.raise_for_status()
            timestamp = response.json().get("timestamp_to_request")
            status = response.json().get("status")
        except requests.exceptions.ReadTimeout:
            logger.debug(f'Сервер не ответил...Ждем и посылаем запрос еще раз.')
            await asyncio.sleep(SLEEP_TIME)
            continue
        except requests.exceptions.ConnectionError:
            logger.debug(f'Потеряно соединение...Ждем подключения.')
            await asyncio.sleep(SLEEP_TIME)
            continue
        if status == 'found':
            timestamp = response.json().get("new_attempts")[0].get("timestamp")
            await get_review(response)


async def send_message(msg: str):
    bot = telegram.Bot(TELEGRAM_API_TOKEN)
    async with bot:
        await bot.send_message(text=msg, chat_id=TELEGRAM_CHAT_ID)


if __name__ == '__main__':
    logger.add(PATH_TO_LOGS, level='DEBUG')
    asyncio.run(main())
