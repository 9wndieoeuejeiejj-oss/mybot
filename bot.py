import requests
import time

TOKEN = "715460300:CiPzvD38I1kbZ6yMJxu-Kiu2nz8FYcFljjM"

BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}/"

offset = 0

def send_message(chat_id, text):
    requests.post(
        BASE_URL + "sendMessage",
        json={"chat_id": chat_id, "text": text}
    )

while True:
    try:
        response = requests.get(
            BASE_URL + "getUpdates",
            params={"offset": offset},
            timeout=30
        )

        data = response.json()

        for update in data.get("result", []):
            offset = update["update_id"] + 1

            message = update.get("message", {})
            text = message.get("text", "")
            chat_id = message.get("chat", {}).get("id")

            if not chat_id:
                continue

            # پاسخ به سلام
            if text.strip() == "سلام":
                send_message(chat_id, "سلام")

            # اخطار برای لینک
            if (
                "http://" in text or
                "https://" in text or
                "www." in text or
                "t.me/" in text or
                "bale.ai/" in text
            ):
                send_message(chat_id, "⚠️ لطفاً لینک ارسال نکنید.")

        time.sleep(1)

    except Exception as e:
        print("ERROR:", e)
        time.sleep(5)
