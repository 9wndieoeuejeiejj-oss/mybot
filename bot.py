from fastapi import FastAPI, Request
import requests
import re
import os

app = FastAPI()

TOKEN = os.getenv("715460300:CiPzvD38I1kbZ6yMJxu-Kiu2nz8FYcFljjM")
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}/"

def send_message(chat_id, text, reply_to=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_to:
        data["reply_to_message_id"] = reply_to
    requests.post(BASE_URL + "sendMessage", json=data)

def kick_user(chat_id, user_id):
    data = {"chat_id": chat_id, "user_id": user_id}
    requests.post(BASE_URL + "kickChatMember", json=data)

@app.post("/webhook")
async def webhook(req: Request):
    update = await req.json()
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")
        msg_id = msg.get("message_id")
        user_id = msg["from"]["id"]

        # بررسی وجود لینک در پیام
        if re.search(r"http[s]?://", text):
            send_message(chat_id, "🚫 ارسال لینک ممنوع است!", msg_id)
            kick_user(chat_id, user_id)

    return {"ok": True}
