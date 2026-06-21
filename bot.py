import requests
import time

TOKEN = "توکن_ربات_خودت"

URL = f"https://tapi.bale.ai/bot{TOKEN}"

offset = 0

while True:
    try:
        response = requests.get(f"{URL}/getUpdates?offset={offset}")
        updates = response.json()["result"]

        for update in updates:
            offset = update["update_id"] + 1

            if "message" not in update:
                continue

            chat_id = update["message"]["chat"]["id"]

            if "reply_to_message" in update["message"]:
                requests.post(
                    f"{URL}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "سلام 😊"
                    }
                )

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(5)
