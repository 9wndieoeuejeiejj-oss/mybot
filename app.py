from bot import bot
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "ربات مدیریت گروه بله فعال است!"

def run_bot():
    bot.run()

if __name__ == "__main__":
    thread = threading.Thread(target=run_bot)
    thread.start()
    app.run(host='0.0.0.0', port=8080)
