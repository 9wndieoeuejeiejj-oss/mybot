from bale import Bot, Update, Message

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

client.run()
