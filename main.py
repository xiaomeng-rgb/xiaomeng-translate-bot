from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# 获取环境变量中的 Telegram Token
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# 简单中英文互译逻辑
def translate(text):
    if any('\u4e00' <= c <= '\u9fff' for c in text):  # 如果包含中文
        return "Translated to English: " + text  # 这里可接入翻译 API
    else:
        return "翻译成中文：" + text  # 同样可接入翻译 API

# 设置 webhook 路由
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("⚠️ 收到 Telegram 消息：", data)  # 调试用日志

    message = data.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text")

    if chat_id and text:
        translated_text = translate(text)
        requests.post(TELEGRAM_API_URL, json={
            "chat_id": chat_id,
            "text": translated_text
        })

    return jsonify(success=True)

# 设置测试用 GET 路由
@app.route("/", methods=["GET"])
def home():
    return "Telegram Translate Bot is running."

# 启动服务，Render 会自动分配 PORT 环境变量
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
