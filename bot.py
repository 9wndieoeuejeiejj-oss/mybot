import requests
import time

# توکن ربات
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

            chat_id = message["chat"]["id"]
            chat_type = message["chat"]["type"]
            text = message.get("text", "")
            name = message["from"]["first_name"]

            # فقط در گروه‌ها
            if chat_type == "private":
                continue

            # تشخیص لینک
            if (
                "http://" in text
                or "https://" in text
                or "www." in text
                or ".com" in text
                or ".ir" in text
            ):

                requests.post(
                    f"{URL}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": f"⚠️ {name}\nارسال لینک در این گروه ممنوع است!"
                    }
                )

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(5)
