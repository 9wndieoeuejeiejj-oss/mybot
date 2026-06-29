from bale import Bot, Message
import os

TOKEN = "715460300:CiPzvD38I1kbZ6yMJxu-KiuZ"
bot = Bot(TOKEN)

@bot.event
async def on_ready():
    print("ربات آنلاین شد!")

@bot.event
async def on_message(message: Message):
    if not message.chat:
        return
    
    text = message.content or ""
    chat_id = message.chat.id
    user_id = message.author.id
    username = message.author.username or "کاربر"

    # سلام
    if text == "سلام":
        await bot.send_message(chat_id, f"سلام {username} جان! 😊")
        return

    # اگه @ داشت
    if "@" in text and not text.startswith("/"):
        admins = await bot.get_chat_administrators(chat_id)
        is_admin = False
        for admin in admins:
            if admin.user.id == user_id:
                is_admin = True
                break
        
        if not is_admin:
            await bot.send_message(chat_id, f"@{username} ❌ ارسال @ ممنوع!")
            await bot.ban_chat_member(chat_id, user_id)
            await bot.unban_chat_member(chat_id, user_id)
            await bot.send_message(chat_id, f"🚫 {username} حذف شد!")

if __name__ == "__main__":
    bot.run()
