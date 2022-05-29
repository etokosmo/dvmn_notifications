import asyncio
import os

import requests
import telegram
from environs import Env
from loguru import logger

BASE_DIR = os.path.dirname(__file__) or '.'
PATH_TO_LOGS = os.path.join(BASE_DIR, 'logs', 'logs.log')


async def get_review(processed_response: dict, telegram_api_token: str, telegram_chat_id: str):
    content = processed_response.get("new_attempts")[0]
    is_negative = content.get("is_negative")
    lesson_title = content.get("lesson_title")
    lesson_url = content.get("lesson_url")
    valid_review_message = "К сожалению в работе нашлись ошибки." if is_negative else "Преподавателю все понравилось. \
    Можно приступать к следующему уроку."
    message = f"У Вас проверили работу '{lesson_title}'.\n\n{valid_review_message}\nСсылка на урок: {lesson_url}"
    await send_message(message, telegram_api_token, telegram_chat_id)


async def main():
    env = Env()
    env.read_env()

    telegram_api_token = env("TELEGRAM_API_TOKEN")
    telegram_chat_id = env("TELEGRAM_CHAT_ID")
    devman_api_token = env("DEVMAN_API_TOKEN")
    long_polling_url = 'https://dvmn.org/api/long_polling/'
    sleep_time = env.int('SLEEP_TIME', 90)
    headers = {
        "Authorization": f"Token {devman_api_token}"
    }
    timestamp = None

    while True:
        try:
            payload = {'timestamp': timestamp}
            response = requests.get(long_polling_url, headers=headers, params=payload)
            response.raise_for_status()
            checks = response.json()
            timestamp = checks.get("timestamp_to_request")
            status = checks.get("status")
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            logger.debug(f'Потеряно соединение...Ждем подключения.')
            await asyncio.sleep(sleep_time)
            continue
        if status == 'found':
            timestamp = checks.get("last_attempt_timestamp")
            await get_review(checks, telegram_api_token, telegram_chat_id)


async def send_message(msg: str, telegram_api_token: str, telegram_chat_id: str):
    bot = telegram.Bot(telegram_api_token)
    async with bot:
        await bot.send_message(text=msg, chat_id=telegram_chat_id)


if __name__ == '__main__':
    logger.add(PATH_TO_LOGS, level='DEBUG')
    asyncio.run(main())
