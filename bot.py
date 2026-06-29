# bot.py
import asyncio
import re
import time
from datetime import datetime, timedelta
from bale import Bot, Message, ChatMember, ChatType
from bale.handlers import MessageHandler, ChatMemberHandler
import os

# ===================== تنظیمات =====================
TOKEN = os.getenv("715460300:CiPzvD38I1kbZ6yMJxu-Kiu2nz8FYcFljjM")
# ===================================================

bot = Bot(TOKEN)

# دیکشنری برای ذخیره اطلاعات کاربران (اسپم، تعداد پیام و...)
user_activity = {}
# لیست کلمات فحش (می‌توانید بیشتر کنید)
BAD_WORDS = ["فحش1", "فحش2", "کلمه_بد3"]
# مدت زمان محدودیت (ثانیه)
SPAM_TIME_LIMIT = 5
# تعداد مجاز پیام در بازه زمانی
SPAM_MESSAGE_LIMIT = 5

# ================ توابع کمکی ================

def is_admin(chat_id: int, user_id: int) -> bool:
    """بررسی اینکه کاربر ادمین است یا خیر"""
    try:
        admins = bot.get_chat_administrators(chat_id)
        for admin in admins:
            if admin.user.id == user_id:
                return True
        return False
    except:
        return False

def contains_link(text: str) -> bool:
    """بررسی وجود لینک در متن"""
    url_pattern = r'(https?://[^\s]+|www\.[^\s]+|[^\s]+\.(com|org|ir|net|info))'
    return bool(re.search(url_pattern, text, re.IGNORECASE))

def contains_bad_word(text: str) -> bool:
    """بررسی وجود فحش در متن"""
    if not text:
        return False
    for word in BAD_WORDS:
        if word in text:
            return True
    return False

def is_spam(user_id: int) -> bool:
    """بررسی اسپم بودن کاربر"""
    now = time.time()
    if user_id not in user_activity:
        user_activity[user_id] = []
    
    # پاک کردن پیام‌های قدیمی
    user_activity[user_id] = [t for t in user_activity[user_id] if now - t < SPAM_TIME_LIMIT]
    
    # اضافه کردن پیام جدید
    user_activity[user_id].append(now)
    
    return len(user_activity[user_id]) > SPAM_MESSAGE_LIMIT

# ================ هندلرهای رویداد ================

@bot.event
async def on_ready():
    """زمانی که ربات آماده شد"""
    print(f"ربات {bot.user.username} آماده کار شد!")

@bot.event
async def on_message(message: Message):
    """هندلر اصلی پیام‌ها"""
    if not message.chat or message.chat.type == ChatType.PRIVATE:
        return  # فقط در گروه‌ها کار می‌کند
    
    chat_id = message.chat.id
    user_id = message.author.id
    text = message.content or ""
    
    # ====== مدیریت دستورات ======
    if text.startswith('/'):
        await handle_commands(message)
        return
    
    # ====== بررسی اسپم ======
    if is_spam(user_id):
        try:
            await bot.delete_message(chat_id, message.id)
            # ارسال اخطار به کاربر
            warn_msg = await bot.send_message(chat_id, f"@{message.author.username}، لطفاً اسپم نکنید!")
            await asyncio.sleep(3)
            await bot.delete_message(chat_id, warn_msg.id)
        except:
            pass
        return
    
    # ====== حذف لینک ======
    if contains_link(text):
        try:
            await bot.delete_message(chat_id, message.id)
            warn_msg = await bot.send_message(chat_id, f"@{message.author.username}، ارسال لینک ممنوع است!")
            await asyncio.sleep(3)
            await bot.delete_message(chat_id, warn_msg.id)
        except:
            pass
        return
    
    # ====== حذف فحش ======
    if contains_bad_word(text):
        try:
            await bot.delete_message(chat_id, message.id)
            warn_msg = await bot.send_message(chat_id, f"@{message.author.username}، ادب رو رعایت کنید!")
            await asyncio.sleep(3)
            await bot.delete_message(chat_id, warn_msg.id)
        except:
            pass
        return

@bot.event
async def on_member_chat_join(member: ChatMember, chat_id: int):
    """زمانی که کاربر جدید به گروه می‌پیوندد"""
    try:
        await bot.send_message(
            chat_id,
            f"🎉 به گروه خوش آمدی @{member.user.username}!\n"
            f"لطفاً قوانین گروه را رعایت کنید. 🌸"
        )
    except:
        pass

@bot.event
async def on_member_chat_leave(member: ChatMember, chat_id: int):
    """زمانی که کاربر گروه را ترک می‌کند"""
    try:
        await bot.send_message(
            chat_id,
            f"👋 @{member.user.username} گروه را ترک کرد. خداحافظ!"
        )
    except:
        pass

# ================ هندلر دستورات ================

async def handle_commands(message: Message):
    """مدیریت دستورات ربات"""
    chat_id = message.chat.id
    user_id = message.author.id
    text = message.content
    
    # فقط ادمین‌ها می‌توانند از دستورات مدیریتی استفاده کنند
    if not is_admin(chat_id, user_id):
        await bot.send_message(chat_id, "⛔ شما دسترسی به این دستور را ندارید!")
        return
    
    if text == '/ban' and message.reply_to_message:
        # بن کردن کاربر
        target_user = message.reply_to_message.author
        try:
            await bot.ban_chat_member(chat_id, target_user.id)
            await bot.send_message(
                chat_id,
                f"🚫 @{target_user.username} از گروه بن شد!"
            )
        except:
            await bot.send_message(chat_id, "❌ خطا در بن کردن کاربر!")
    
    elif text == '/unban' and message.reply_to_message:
        # آنبن کردن کاربر
        target_user = message.reply_to_message.author
        try:
            await bot.unban_chat_member(chat_id, target_user.id)
            await bot.send_message(
                chat_id,
                f"✅ @{target_user.username} آنبن شد!"
            )
        except:
            await bot.send_message(chat_id, "❌ خطا در آنبن کردن!")
    
    elif text == '/kick' and message.reply_to_message:
        # اخراج کاربر
        target_user = message.reply_to_message.author
        try:
            await bot.ban_chat_member(chat_id, target_user.id)
            await asyncio.sleep(1)
            await bot.unban_chat_member(chat_id, target_user.id)
            await bot.send_message(
                chat_id,
                f"👢 @{target_user.username} از گروه اخراج شد!"
            )
        except:
            await bot.send_message(chat_id, "❌ خطا در اخراج کاربر!")
    
    elif text == '/promote' and message.reply_to_message:
        # ادمین کردن کاربر
        target_user = message.reply_to_message.author
        try:
            await bot.promote_chat_member(
                chat_id,
                target_user.id,
                can_change_info=True,
                can_delete_messages=True,
                can_invite_users=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=False
            )
            await bot.send_message(
                chat_id,
                f"⭐ @{target_user.username} به ادمینی منصوب شد!"
            )
        except:
            await bot.send_message(chat_id, "❌ خطا در ادمین کردن!")
    
    elif text == '/demote' and message.reply_to_message:
        # گرفتن ادمینی از کاربر
        target_user = message.reply_to_message.author
        try:
            await bot.promote_chat_member(
                chat_id,
                target_user.id,
                can_change_info=False,
                can_delete_messages=False,
                can_invite_users=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False
            )
            await bot.send_message(
                chat_id,
                f"⬇️ ادمینی @{target_user.username} گرفته شد!"
            )
        except:
            await bot.send_message(chat_id, "❌ خطا در گرفتن ادمینی!")
    
    elif text == '/clear' and message.reply_to_message:
        # پاک کردن پیام‌ها
        try:
            msg_id = message.reply_to_message.id
            count = 0
            # حذف تا 100 پیام اخیر
            async for msg in bot.get_chat_history(chat_id, limit=100):
                if msg.id >= msg_id:
                    await bot.delete_message(chat_id, msg.id)
                    count += 1
                    await asyncio.sleep(0.1)  # جلوگیری از محدودیت
            await bot.send_message(
                chat_id,
                f"🧹 {count} پیام پاک شد!"
            )
        except:
            await bot.send_message(chat_id, "❌ خطا در پاک کردن پیام‌ها!")
    
    elif text == '/mute' and message.reply_to_message:
        # محدود کردن کاربر (ارسال پیام ممنوع)
        target_user = message.reply_to_message.author
        try:
            await bot.restrict_chat_member(
                chat_id,
                target_user.id,
                can_send_messages=False
            )
            await bot.send_message(
                chat_id,
                f"🔇 @{target_user.username} محدود شد!"
            )
        except:
            await bot.send_message(chat_id, "❌ خطا در محدود کردن کاربر!")
    
    elif text == '/unmute' and message.reply_to_message:
        # برداشتن محدودیت
        target_user = message.reply_to_message.author
        try:
            await bot.restrict_chat_member(
                chat_id,
                target_user.id,
                can_send_messages=True
            )
            await bot.send_message(
                chat_id,
                f"🔊 @{target_user.username} آزاد شد!"
            )
        except:
            await bot.send_message(chat_id, "❌ خطا در آزاد کردن کاربر!")
    
    elif text == '/stats':
        # آمار گروه
        try:
            count = bot.get_chat_members_count(chat_id)
            await bot.send_message(
                chat_id,
                f"📊 آمار گروه:\n"
                f"👥 تعداد اعضا: {count}\n"
                f"🤖 ربات توسط @BaleBot ساخته شده است"
            )
        except:
            await bot.send_message(chat_id, "❌ خطا در دریافت آمار!")
    
    elif text == '/help':
        # راهنما
        help_text = """
🤖 **راهنمای ربات مدیریت گروه**

**دستورات مدیریتی (فقط ادمین‌ها):**
- `/ban` (ریپلای) : بن کردن کاربر
- `/unban` (ریپلای) : آنبن کردن کاربر
- `/kick` (ریپلای) : اخراج کاربر از گروه
- `/promote` (ریپلای) : ادمین کردن کاربر
- `/demote` (ریپلای) : گرفتن ادمینی
- `/mute` (ریپلای) : محدود کردن کاربر
- `/unmute` (ریپلای) : آزاد کردن کاربر
- `/clear` (ریپلای) : پاک کردن پیام‌ها
- `/stats` : نمایش آمار گروه
- `/help` : نمایش این راهنما

**قابلیت‌های خودکار:**
- ✅ حذف خودکار لینک‌ها
- ✅ حذف خودکار فحش‌ها
- ✅ جلوگیری از اسپم
- ✅ خوش‌آمدگویی به اعضای جدید
- ✅ خداحافظی با اعضای خارج شده
"""
        await bot.send_message(chat_id, help_text, parse_mode="Markdown")

# ================ اجرای ربات ================

if __name__ == "__main__":
    print("ربات در حال اجراست...")
    bot.run()
