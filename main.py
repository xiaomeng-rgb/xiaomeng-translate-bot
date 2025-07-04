from flask import Flask, request
import requests
import os

app = Flask(__name__)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def translate(text):
    import googletrans
    from googletrans import Translator
    translator = Translator()
    detected = translator.detect(text).lang
    dest = 'zh-cn' if detected == 'en' else 'en'
    return translator.translate(text, dest=dest).text

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        translated = translate(text)
        requests.post(URL, json={"chat_id": chat_id, "text": translated})
    return {"ok": True}

@app.route("/", methods=["GET"])
def home():
    return "Xiaomeng Translate Bot is running."

if __name__ == "__main__":
    app.run()
