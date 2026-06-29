import asyncio
import re
import time
from bale import Bot, Message, ChatMember
import os

TOKEN = "715460300:CiPzvD38I1kbZ6yMJxu-KiuZ"
bot = Bot(TOKEN)

# لیست کلمات فحش (خودت میتونی بیشتر کنی)
BAD_WORDS = ["فحش", "کشک", "کصخل", "کونی", "گوه"]

# تنظیمات اسپم
SPAM_TIME_LIMIT = 5  # چند ثانیه
SPAM_MESSAGE_LIMIT = 5  # چند پیام مجاز

# ذخیره فعالیت کاربرا
user_activity = {}

# ============================================
# ✅ تشخیص لینک (حرفه‌ای)
# ============================================
def contains_link(text):
    if not text:
        return False
    # این الگو همه لینک‌ها رو تشخیص میده
    url_pattern = r'(https?://[^\s]+|www\.[^\s]+|[^\s]+\.(com|org|ir|net|info|io|co))'
    return bool(re.search(url_pattern, text, re.IGNORECASE))

# ============================================
# ✅ تشخیص فحش
# ============================================
def contains_bad_word(text):
    if not text:
        return False
    for word in BAD_WORDS:
        if word in text:
            return True
    return False

# ============================================
# ✅ تشخیص اسپم
# ============================================
def is_spam(user_id):
    now = time.time()
    if user_id not in user_activity:
        user_activity[user_id] = []
    # حذف زمان‌های قدیمی
    user_activity[user_id] = [t for t in user_activity[user_id] if now - t < SPAM_TIME_LIMIT]
    # اضافه کردن پیام جدید
    user_activity[user_id].append(now)
    return len(user_activity[user_id]) > SPAM_MESSAGE_LIMIT

# ============================================
# ✅ هندلر پیام‌ها
# ============================================
@bot.event
async def on_ready():
    print(f"ربات {bot.user.username} آنلاین شد!")

@bot.event
async def on_message(message: Message):
    chat_id = message.chat.id
    user_id = message.author.id
    text = message.content or ""

    # 🔹 دستورات
    if text.startswith("/"):
        await handle_commands(message)
        return

    # 🔹 حذف لینک
    if contains_link(text):
        await bot.delete_message(chat_id, message.id)
        msg = await bot.send_message(chat_id, f"@{message.author.username} ❌ ارسال لینک ممنوع!")
        await asyncio.sleep(2)
        await bot.delete_message(chat_id, msg.id)
        return

    # 🔹 حذف فحش
    if contains_bad_word(text):
        await bot.delete_message(chat_id, message.id)
        msg = await bot.send_message(chat_id, f"@{message.author.username} 🚫 ادب رو رعایت کن!")
        await asyncio.sleep(2)
        await bot.delete_message(chat_id, msg.id)
        return

    # 🔹 تشخیص اسپم
    if is_spam(user_id):
        await bot.delete_message(chat_id, message.id)
        msg = await bot.send_message(chat_id, f"@{message.author.username} ⛔ اسپم نکن!")
        await asyncio.sleep(2)
        await bot.delete_message(chat_id, msg.id)
        return

# ============================================
# ✅ خوش‌آمدگویی و خداحافظی
# ============================================
@bot.event
async def on_member_chat_join(member: ChatMember, chat_id: int):
    await bot.send_message(chat_id, f"🎉 به گروه خوش آمدی @{member.user.username}!")

@bot.event
async def on_member_chat_leave(member: ChatMember, chat_id: int):
    await bot.send_message(chat_id, f"👋 @{member.user.username} گروه رو ترک کرد!")

# ============================================
# ✅ دستورات ربات
# ============================================
async def handle_commands(message: Message):
    chat_id = message.chat.id
    text = message.content

    if text == "/start":
        await bot.send_message(chat_id, "👋 سلام! من ربات مدیریت گروه هستم.")

    elif text == "/help":
        await bot.send_message(
            chat_id,
            "🤖 **راهنما:**\n"
            "✅ حذف خودکار لینک\n"
            "✅ حذف خودکار فحش\n"
            "✅ جلوگیری از اسپم\n"
            "✅ خوش‌آمدگویی و خداحافظی\n"
            "✅ دستور /start"
        )

if __name__ == "__main__":
    print("ربات در حال اجراست...")
    bot.run()
