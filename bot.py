import requests
import random
import time

TOKEN = "715460300:CiPzvD38I1kbZ6yMJxu-Kiu2nz8FYcFljjM"

URL = f"https://tapi.bale.ai/bot{TOKEN}"

offset = 0

start_messages = [
    "سلام 😊"
]

while True:
    try:
        response = requests.get(f"{URL}/getUpdates?offset={offset}")
        updates = response.json()["result"]

        for update in updates:
            offset = update["update_id"] + 1

            if "message" not in update:
                continue

            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")

            if text == "/start":
                answer = random.choice(start_messages)
            else:
                answer = "سلام 😊"

            requests.post(
                f"{URL}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": answer
                }
            )

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(5)
