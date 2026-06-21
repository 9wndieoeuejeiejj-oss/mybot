import requests
import time

TOKEN = "715460300:CiPzvD38I1kbZ6yMJxu-Kiu2nz8FYcFljjM"

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

            message = update["message"]

            # فقط گروه‌ها
            chat_type = message["chat"]["type"]
            if chat_type == "private":
                continue

            text = message.get("text", "")
            chat_id = message["chat"]["id"]

            # اگر پیام ریپلای بود
            if "reply_to_message" in message:
                reply_msg = message["reply_to_message"]

                # اگر روی پیام خود ربات ریپلای شده
                if "from" in reply_msg and reply_msg["from"].get("is_bot", False):

                    if text == "سلام":
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
