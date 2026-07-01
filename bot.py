from bale import Bot, Update, Message
from flask import Flask
import os
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "ربات در حال اجراست!"

# راه‌اندازی ربات در یک ترد جداگانه
client = Bot(token="715460300:CiPzvD38I1kbZ6yMJxu-Kiu2nz8FYcFljjM")

@client.event
async def on_ready():
    print(client.user.username, "is Ready!")

@client.event
async def on_update(update: Update):
    print(update.update_id)

@client.event
async def on_message(message: Message):
    if message.content == "/start":
        await message.reply("Hi, from python-bale-bot to everyone!")
        if message.chat.is_group_chat:
            await message.reply("It's is a special Hi for groups!")

def run_bot():
    client.run()

if __name__ == "__main__":
    # اجرای ربات در ترد جداگانه
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    # اجرای سرور Flask روی پورت ۱۰۰۰۰
    app.run(host="0.0.0.0", port=10000)
