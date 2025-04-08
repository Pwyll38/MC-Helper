import discord, os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
        print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    print (message.content)
    if message.author == client.user:
        return

    else:
        await message.channel.send('Hello!')


client.run(TOKEN)


