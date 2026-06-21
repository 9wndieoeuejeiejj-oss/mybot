import requests
import time

TOKEN = "715460300:CiPzvD38I1kbZ6yMJxu-Kiu2nz8FYcFljjM"
URL = f"https://tapi.bale.ai/bot{TOKEN}"

offset = 0
warnings = {}

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

            if chat_type == "private":
                continue

            user_id = message["from"]["id"]
            name = message["from"]["first_name"]
            text = message.get("text", "")
            message_id = message["message_id"]

            # تشخیص لینک
            if (
                "http://" in text
                or "https://" in text
                or "www." in text
                or ".com" in text
                or ".ir" in text
            ):

                # حذف پیام لینک
                requests.post(
                    f"{URL}/deleteMessage",
                    json={
                        "chat_id": chat_id,
                        "message_id": message_id
                    }
                )

                # ثبت اخطار
                if user_id not in warnings:
                    warnings[user_id] = 0

                warnings[user_id] += 1

                # اگر اخطار کمتر از 3 بود
                if warnings[user_id] < 3:
                    requests.post(
                        f"{URL}/sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": f"⚠️ {name}\nاخطار {warnings[user_id]}\nارسال لینک ممنوع است."
                        }
                    )

                # اخطار سوم = حذف از گروه
                else:
                    requests.post(
                        f"{URL}/sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": f"⛔ {name}\n3 اخطار دریافت کرد و از گروه حذف شد."
                        }
                    )

                    requests.post(
                        f"{URL}/banChatMember",
                        json={
                            "chat_id": chat_id,
                            "user_id": user_id
                        }
                    )

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(5)
