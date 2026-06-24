import requests
import time

TOKEN = "715460300:CiPzvD38I1kbZ6yMJxu-Kiu2nz8FYcFljjM"

BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}/"

offset = None

def send_message(chat_id, text):
    requests.post(
        BASE_URL + "sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=10
    )

while True:
    try:
        params = {}

        if offset is not None:
            params["offset"] = offset

        response = requests.get(
            BASE_URL + "getUpdates",
            params=params,
            timeout=30
        )

        data = response.json()

        for update in data.get("result", []):

            offset = update["update_id"] + 1

            if "message" not in update:
                continue

            message = update["message"]
            text = str(message.get("text", "")).strip()
            chat_id = message.get("chat", {}).get("id")

            if not chat_id:
                continue

            # پاسخ به سلام
            if text == "سلام":
                send_message(chat_id, "سلام")

            # تشخیص لینک
            text_lower = text.lower()

            if (
                "http://" in text_lower or
                "https://" in text_lower or
                "www." in text_lower or
                "t.me/" in text_lower or
                "bale.ai/" in text_lower
            ):
                send_message(
                    chat_id,
                    "⚠️ لطفاً لینک ارسال نکنید."
                )

        time.sleep(1)

    except Exception as e:
        print("ERROR:", e)
        time.sleep(5)
