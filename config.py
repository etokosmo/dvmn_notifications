from environs import Env

env = Env()
env.read_env()

TELEGRAM_API_TOKEN = env("TELEGRAM_API_TOKEN")
TELEGRAM_CHAT_ID = env("TELEGRAM_CHAT_ID")
DEVMAN_API_TOKEN = env("DEVMAN_API_TOKEN")
LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'
HEADERS = {
    "Authorization": f"Token {DEVMAN_API_TOKEN}"
}
