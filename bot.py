import asyncio
import re
import time
from bale import Bot, Message, ChatMember
import os

TOKEN = os.getenv("715460300:CiPzvD38I1kbZ6yMJxu-Kiu2nz8FYcFljjM")
bot = Bot(TOKEN)

user_activity = {}
BAD_WORDS = ["فحش1", "فحش2"]
SPAM_TIME_LIMIT = 5
SPAM_MESSAGE_LIMIT = 5

def contains_link(text):
    url_pattern = r'(https?://[^\s]+|www\.[^\s]+|[^\s]+\.(com|org|ir|net|info))'
    return bool(re.search(url_pattern, text, re.IGNORECASE))

def contains_bad_word(text):
    if not text:
        return False
    for word in BAD_WORDS:
        if word in text:
            return True
    return False

def is_spam(user_id):
    now = time.time()
    if user_id not in user_activity:
        user_activity[user_id] = []
    user_activity[user_id] = [t for t in user_activity[user_id] if now - t < SPAM_TIME_LIMIT]
    user_activity[user_id].append(now)
    return len(user_activity[user_id]) > SPAM_MESSAGE_LIMIT

@bot.event
async def on_ready():
    print(f"ربات {bot.user.username} آماده شد!")

@bot.event
async def on_message(message: Message):
    if not message.chat:
        return
    chat_id = message.chat.id
    user_id = message.author.id
    text = message.content or ""
    
    if text.startswith('/'):
        await handle_commands(message)
        return
    
    if is_spam(user_id) or contains_link(text) or contains_bad_word(text):
        try:
            await bot.delete_message(chat_id, message.id)
        except:
            pass
        return

@bot.event
async def on_member_chat_join(member: ChatMember, chat_id: int):
    try:
        await bot.send_message(chat_id, f"🎉 به گروه خوش آمدی @{member.user.username}!")
    except:
        pass

@bot.event
async def on_member_chat_leave(member: ChatMember, chat_id: int):
    try:
        await bot.send_message(chat_id, f"👋 @{member.user.username} گروه را ترک کرد.")
    except:
        pass

async def handle_commands(message: Message):
    chat_id = message.chat.id
    text = message.content
    
    if text == '/start':
        await bot.send_message(chat_id, "سلام! من ربات مدیریت گروه هستم.")
    
    elif text == '/help':
        await bot.send_message(chat_id, "دستورات: /start , /help")

if __name__ == "__main__":
    print("ربات در حال اجراست...")
    bot.run()
