import asyncio

import requests
import telegram

from config import TELEGRAM_API_TOKEN, TELEGRAM_CHAT_ID, LONG_POLLING_URL, HEADERS


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
    timeout = None
    while True:
        try:
            payload = {'timestamp': timeout}
            response = requests.get(LONG_POLLING_URL, headers=HEADERS, params=payload)
            response.raise_for_status()
            timeout = response.json().get("timestamp_to_request")
            if not timeout:
                timeout = response.json().get("timestamp")
            status = response.json().get("status")
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
            continue
        if status == 'found':
            await get_review(response)


async def send_message(msg: str):
    bot = telegram.Bot(TELEGRAM_API_TOKEN)
    async with bot:
        await bot.send_message(text=msg, chat_id=TELEGRAM_CHAT_ID)


if __name__ == '__main__':
    asyncio.run(main())
