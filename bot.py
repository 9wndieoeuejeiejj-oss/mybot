import requests
import time

TOKEN = "715460300:CiPzvD38I1kbZ6yMJxu-Kiu2nz8FYcFljjM"

URL = "https://tapi.bale.ai/bot" + TOKEN

offset = 0

while True:
    try:
        response = requests.get(URL + "/getUpdates?offset=" + str(offset))
        updates = response.json()["result"]

        for update in updates:
            offset = update["update_id"] + 1

            if "message" not in update:
                continue

            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")

            if text == "سلام":
                requests.post(
                    URL + "/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "سلام چطوری؟ 😊"
                    }
                )

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(5)
