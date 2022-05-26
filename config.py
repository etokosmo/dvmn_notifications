import os

from environs import Env

env = Env()
env.read_env()

BASE_DIR = os.path.dirname(__file__) or '.'
PATH_TO_LOGS = os.path.join(BASE_DIR, 'logs', 'logs.log')
TELEGRAM_API_TOKEN = env("TELEGRAM_API_TOKEN")
TELEGRAM_CHAT_ID = env("TELEGRAM_CHAT_ID")
DEVMAN_API_TOKEN = env("DEVMAN_API_TOKEN")
LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'
SLEEP_TIME = env.int('SLEEP_TIME', 90)
HEADERS = {
    "Authorization": f"Token {DEVMAN_API_TOKEN}"
}
