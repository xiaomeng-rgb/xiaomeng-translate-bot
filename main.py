from flask import Flask
from threading import Thread
import os
import requests
import time
from translate import translate_text  # 你的翻译函数，保留你已有的逻辑

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

def telegram_bot():
    TOKEN = os.environ['TELEGRAM_TOKEN']
    URL = f'https://api.telegram.org/bot{TOKEN}/getUpdates'

    offset = None
    while True:
        try:
            res = requests.get(URL, params={'offset': offset, 'timeout': 30}).json()
            for update in res['result']:
                offset = update['update_id'] + 1
                chat_id = update['message']['chat']['id']
                text = update['message']['text']
                # 翻译逻辑
                translated = translate_text(text)
                requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                              json={'chat_id': chat_id, 'text': translated})
        except Exception as e:
            print('Error:', e)
        time.sleep(1)

if __name__ == '__main__':
    Thread(target=run).start()
    telegram_bot()
