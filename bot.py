from bale import Bot, Message

bot = Bot("715460300:CiPzvD38I1kbZ6yMJxu-Kiu2nz8FYcFljjM")

@bot.event
async def on_message(message: Message):
    await message.reply("پیام شما دریافت شد")

bot.run()
