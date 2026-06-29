from bale import Bot, Message
import os
import asyncio

# ======== توکن ربات ========
TOKEN = "715460300:CiPzvD38I1kbZ6yMJxu-KiuZ"
bot = Bot(TOKEN)

# =============================
# زمان روشن شدن ربات
# =============================
@bot.event
async def on_ready():
    print("ربات با موفقیت روشن شد و آماده کار است!")

# =============================
# مدیریت پیام‌ها
# =============================
@bot.event
async def on_message(message: Message):
    # اگه پیام در گروه نبود، نادیده بگیر
    if not message.chat:
        return

    # اطلاعات پایه
    text = message.content or ""
    chat_id = message.chat.id
    user_id = message.author.id
    username = message.author.username or "کاربر"

    # 1️⃣ سلام کردن به کاربر
    if text.strip().lower() == "سلام":
        await bot.send_message(chat_id, f"سلام {username} جان! 😊")
        return  # بعد از سلام، کار دیگه‌ای نکن

    # 2️⃣ اگر پیام حاوی @ بود و دستور نبود
    if "@" in text and not text.startswith("/"):
        try:
            # اخطار به کاربر
            await bot.send_message(chat_id, f"@{username} ❌ ارسال @ در گروه ممنوع است!")

            # دریافت لیست ادمین‌ها
            admins = await bot.get_chat_administrators(chat_id)
            
            # بررسی ادمین بودن کاربر
            is_admin = False
            for admin in admins:
                if admin.user.id == user_id:
                    is_admin = True
                    break

            # اگر ادمین نبود، حذفش کن
            if not is_admin:
                await bot.ban_chat_member(chat_id, user_id)
                await asyncio.sleep(1)  # مکث کوتاه برای انجام عملیات
                await bot.unban_chat_member(chat_id, user_id)
                await bot.send_message(chat_id, f"🚫 کاربر {username} به دلیل ارسال @ از گروه حذف شد.")

        except Exception as e:
            # اگه خطایی پیش اومد، فقط توی لاگ نشون بده (ربات کرش نمیکنه)
            print(f"خطا: {e}")

# =============================
# اجرای ربات
# =============================
if __name__ == "__main__":
    bot.run()
