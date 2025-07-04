import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

# 获取你的 Telegram Bot Token（从环境变量中）
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# 自动语言识别并翻译
def translate(text):
    from googletrans import Translator
    translator = Translator()
    src_lang = 'zh-cn' if any('\u4e00' <= ch <= '\u9fff' for ch in text) else 'en'
    dest_lang = 'en' if src_lang == 'zh-cn' else 'zh-cn'
    translated = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated.text

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        translated_text = translate(text)
        requests.post(TELEGRAM_API, json={
            "chat_id": chat_id,
            "text": translated_text
        })
    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "Bot is running."

if __name__ == "__main__":
    app.run(debug=True)
