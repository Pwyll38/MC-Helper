import discord, os, time
from dotenv import load_dotenv
from discord.ext import tasks

load_dotenv()

SERVER_LOCATION = str(os.getenv("SERVER_LOCATION"))
BACKUP_LOCATION = str(os.getenv("BACKUP_LOCATION"))
TOKEN = os.getenv('TOKEN')

client = discord.Client(intents=discord.Intents.all())

def initFile():

    logfile = open(SERVER_LOCATION+"/logs/latest.log", "r")
    logfile.seek(0, 2)

    return logfile

@tasks.loop(seconds = 1)
async def myLoop(logfile):

    line = str(logfile.readline())

    line = line.strip()

    if not line or line == '':
        return
    
    general = client.get_channel(1358807353117642826)
    
    await general.send(line + ", goodbye!")


@client.event
async def on_ready():    
    print("Im online")

    logfile = initFile()

    myLoop.start(logfile)



@client.event
async def on_message(message):
    print (message.content)
    if message.author == client.user:
        return

    else:
        await message.channel.send('Hello!')
        await message.channel.send(str(message.channel))


client.run(TOKEN)


