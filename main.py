from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# 获取 Token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# 翻译函数（中英互译示例）
def translate(text):
    if all('\u4e00' <= char <= '\u9fff' for char in text):  # 是中文
        return "Translated to English: " + text
    else:
        return "翻译成中文：" + text

# Webhook 接口
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify(success=False)

    message = data.get("message")
    if not message:
        return jsonify(success=False)

    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text")

    if chat_id and text:
        translated = translate(text)
        requests.post(TELEGRAM_API_URL, json={
            "chat_id": chat_id,
            "text": translated
        })

    return jsonify(success=True)

# Render首页测试
@app.route("/", methods=["GET"])
def home():
    return "Xiaomeng Translate Bot is running."

# 启动服务器（Render 平台用）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
