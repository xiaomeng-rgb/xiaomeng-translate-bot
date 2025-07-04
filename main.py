from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# 从环境变量获取 Telegram Bot Token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# 简单中英文互译函数（演示用）
def translate(text):
    if all('\u4e00' <= char <= '\u9fff' for char in text):
        return "Translated to English: " + text
    else:
        return "翻译成中文：" + text

# Telegram webhook 消息处理接口
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text")

    if chat_id and text:
        translated = translate(text)
        requests.post(TELEGRAM_API_URL, json={
            "chat_id": chat_id,
            "text": translated
        })
    return jsonify(success=True)

# 健康检查（GET）
@app.route("/", methods=["GET"])
def home():
    return "Telegram Translate Bot is running."

# 主函数用于本地测试或 Render 启动
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
