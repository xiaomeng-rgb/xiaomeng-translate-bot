from flask import Flask, request
import os
import requests

app = Flask(__name__)

# 获取 Telegram Token 和 API URL
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# 简单翻译函数（中英文自动识别）
def translate(text):
    if all('\u4e00' <= char <= '\u9fff' for char in text):  # 中文
        return "Translated to English: " + text
    else:
        return "翻译成中文：" + text

# Webhook 接收处理
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return {"ok": False}, 400

    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text")

    if chat_id and text:
        translated = translate(text)
        requests.post(TELEGRAM_API_URL, json={
            "chat_id": chat_id,
            "text": translated
        })

    return {"ok": True}

# 首页用于 Render 检查服务健康状态
@app.route('/', methods=['GET'])
def index():
    return 'Telegram Translate Bot is alive.'

# 启动服务
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
