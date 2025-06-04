import discord, os, time, random
from dotenv import load_dotenv, find_dotenv
from discord.ext import tasks

load_dotenv()

print("Env funcionanado: "+ str(load_dotenv(find_dotenv(), override=True)))

SERVER_LOCATION = str(os.getenv("SERVER_LOCATION"))
BACKUP_LOCATION = str(os.getenv("BACKUP_LOCATION"))
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
FFMPEG = os.getenv('FFMPEG')

client = discord.Client(intents=discord.Intents.all(), description="A bee bot")

async def playSound(file):
    source = discord.FFmpegOpusAudio(executable=FFMPEG,source=file)
    vChannel = client.get_channel(1358807353574559944)

    vClient = await vChannel.connect()

    vClient.play(source)

    vClient.stop()

async def reactToLogs(logfile):

    line = str(logfile.readline())

    line = line.strip()

    if not line or line == '':
        return
    
    #Cases:
    general = client.get_channel(CHANNEL_ID) or await client.fetch_channel(CHANNEL_ID)

    if('[Server thread\\INFO]: Done' in line):
        await client.change_presence(status=discord.Status.online, activity=discord.Game('Server is online!'))

    
    if('[Server thread\\ERROR]' in line):
        await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Server is down ;-;'))

    if ('!ping' in line):
        await general.send("Pong!")

    if ('!pipe'):
        
        source = discord.FFmpegOpusAudio(executable=FFMPEG,source='MC-Helper\\Discord Bot\\Botvenv\\assets\\pipe.mp3')
        vChannel = client.get_channel(1358807353574559944)

        vClient = await vChannel.connect()

        vClient.stop()

        vClient.play(source)

    if ("!gae"):
        await general.send("Você está "+ random.randint(0,101)+ f"% gae hoje!")


        
def initFile():

    logfile = open(SERVER_LOCATION+"\\logs\\latest.log", "r")
    logfile.seek(0, 2)

    return logfile

@tasks.loop(seconds = 1)
async def myLoop(logfile):

    await reactToLogs(logfile)


@client.event
async def on_ready():

    print('\033[92m'+"====-----Discord Bot Live!----===="+'\033[0m')

    await client.change_presence(status=discord.Status.online)

    client.get_channel(CHANNEL_ID)

    logfile = initFile()

    myLoop.start(logfile)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    else:
        general = message.channel or await client.fetch_channel(CHANNEL_ID)


    #Cases:

        if(message.content == '!generate'):
            await message.channel.send(str(random.randrange(0,40)))

        if (message.content =="!gae"):
            await general.send("Você está "+ str(random.randint(0,101))+ f"% gae hoje!")

        if (message.content =="!dapperSnake"):
            await general.send("Aqui uma cobra chique: ", file=discord.File("..//..//assets//Dapper snek.png"))

        if ( message.content =='!pipe'):

            await playSound('MC-Helper\\Discord Bot\\Botvenv\\assets\\pipe.mp3')
        


@client.event
async def on_disconnect():
    client.change_presence(status=discord.Status.offline)
    client.close()
    print('\033[91m'+"====--- Bot Disconnected ---====")


client.run(TOKEN)
