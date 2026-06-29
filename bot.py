import asyncio
import re
from bale import Bot, Message
import os

TOKEN = "715460300:CiPzvD38I1kbZ6yMJxu-KiuZ"
bot = Bot(TOKEN)

# =============================================
# تابع بررسی وجود @ در متن پیام
# =============================================
def contains_mention(text: str) -> bool:
    # الگوی @username (حداقل ۳ کاراکتر بعد از @)
    pattern = r'@[A-Za-z0-9_]{3,}'
    return bool(re.search(pattern, text))

# =============================================
# وقتی ربات آماده شد
# =============================================
@bot.event
async def on_ready():
    print(f"ربات {bot.user.username} آماده شد!")

# =============================================
# وقتی پیامی در گروه ارسال میشود
# =============================================
@bot.event
async def on_message(message: Message):
    # فقط پیام‌های گروهی را بررسی کن
    if not message.chat:
        return

    chat_id = message.chat.id
    user_id = message.author.id
    text = message.content or ""

    # اگر پیام حاوی @ بود
    if contains_mention(text):
        # اخطار بده
        await bot.send_message(
            chat_id,
            f"@{message.author.username} ❌ ارسال آیدی دیگران در گروه ممنوع است!"
        )

        # بررسی کن که آیا کاربر ادمین است یا نه
        admins = await bot.get_chat_administrators(chat_id)
        is_admin = any(admin.user.id == user_id for admin in admins)

        # اگر ادمین نبود، ریموو کن
        if not is_admin:
            await bot.ban_chat_member(chat_id, user_id)
            await asyncio.sleep(1)
            await bot.unban_chat_member(chat_id, user_id)
            await bot.send_message(
                chat_id,
                f"🚫 کاربر {message.author.username} به دلیل ارسال آیدی، از گروه حذف شد."
            )

# =============================================
# اجرای ربات
# =============================================
if __name__ == "__main__":
    print("ربات در حال اجراست...")
    bot.run()
