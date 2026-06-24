import requests
import time
import re

TOKEN = "715460300:CiPzvD38I1kbZ6yMJxu-Kiu2nz8FYcFljjM"

URL = f"https://tapi.bale.ai/bot{TOKEN}/"

offset = 0

link_pattern = re.compile(
    r"(https?://\S+|www\.\S+|t\.me/\S+|bale\.ai/\S+)",
    re.IGNORECASE
)

def send_message(chat_id, text):
    requests.post(
        URL + "sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        }
    )

while True:
    try:
        response = requests.get(URL + "getUpdates", params={"offset": offset})
        updates = response.json()["result"]

        for update in updates:
            offset = update["update_id"] + 1

            if "message" not in update:
                continue

            message = update["message"]

            if "text" not in message:
                continue

            text = message["text"]
            chat_id = message["chat"]["id"]

            # پاسخ به سلام
            if text.strip() == "سلام":
                send_message(chat_id, "سلام")

            # تشخیص لینک
            if link_pattern.search(text):
                send_message(chat_id, "لطفاً در گروه لینک نفرستید.")

        time.sleep(1)

    except Exception as e:
        print("خطا:", e)
        time.sleep(5)
