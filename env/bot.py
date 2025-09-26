import discord, os, time, random
from dotenv import load_dotenv, find_dotenv
from discord.ext import tasks
from mcstatus import JavaServer
import wikipedia

load_dotenv()

print("ENVs importadas: "+ str(load_dotenv(find_dotenv(), override=True)))

SERVER_LOCATION = os.getenv("SERVER_LOCATION")
BACKUP_LOCATION = os.getenv("BACKUP_LOCATION")
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
FFMPEG = os.getenv('FFMPEG')

client = discord.Client(intents=discord.Intents.all(), description="A bee bot")

"""async def playSound(file):
    source = discord.FFmpegOpusAudio(executable=FFMPEG,source=file)
    vChannel = client.get_channel(1358807353574559944)

    vClient = await vChannel.connect()

    vClient.play(source)

    vClient.stop()"""

def getRandomWikiSummary():
    pageName = wikipedia.random(1)
    try:
        return f"# {pageName} \n{wikipedia.page(pageName).summary}"
    except Exception as e:
        return "No wisdom, try again!"


async def reactToLogs(logfile):

    line = str(logfile.readline()).strip()

    if not line or line == '':
        return
    
    general = client.get_channel(CHANNEL_ID) or await client.fetch_channel(CHANNEL_ID)

    #Log file cases:

    if('[Server thread\\INFO]: Done' in line):
        await client.change_presence(status=discord.Status.online, activity=discord.Game('Server is online!'))
    
    if('[Server thread\\ERROR]' in line):
        await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Server is down ;-;'))

    if ('!ping' in line):
        await general.send("Pong!")

    if ("!gae" in line):
        await general.send(f"Você está {str(random.randint(0,101))} % gae hoje!")

    """if ('!pipe'):
        
        source = discord.FFmpegOpusAudio(executable=FFMPEG,source='MC-Helper/Discord Bot/Botvenv/assetspipe.mp3')
        vChannel = client.get_channel(1358807353574559944)

        vClient = await vChannel.connect()

        vClient.stop()

        vClient.play(source)"""

@tasks.loop(seconds = 1)
async def logLoop(logfile):

    await reactToLogs(logfile)


@client.event
async def on_ready():

    await client.change_presence(status=discord.Status.online)

    client.get_channel(CHANNEL_ID)
    
    try:
        logFile = open(SERVER_LOCATION+"/logs/latest.log", "r")
        logFile.seek(0,2)
        logLoop.start(logFile)

        print('Log file module is online!')
    except Exception as E:
        print(f"Bot log file module offline: Error loading log file: {E}")

    print('\033[92m'+"====-----Discord Bot Live!----===="+'\033[0m')

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    else:

        general = message.channel or await client.fetch_channel(CHANNEL_ID)

    #Discord chat cases:

        if(message.content == '!help'):
            await message.channel.send("My commands are: \n 1) !generate \n 2) !gae \n 3) !dapperSnake \n 4) !server \n 5) !pipe (WIP) \n 6) !wordle (WIP)\n 7) !russianroulette \n 8) !wisdom")

        if(message.content == '!generate'):
            await message.channel.send(str(random.randrange(0,40)))

        if (message.content =="!gae"):
            await general.send("Você está "+ str(random.randint(0,101))+ f"% gae hoje!")

        if (message.content =="!dapperSnake"):
            await general.send("Aqui uma cobra chique: ", file=discord.File("./assets/Dapper_snake.png"))

        if (message.content == '!server'):
            try:
                server = JavaServer.lookup(SERVER_ADDRESS).status()

                await message.channel.send(f"O servidor está rodando! Latência: {int(server.latency)}")

            except Exception as E:
                await message.channel.send(f"Não houve resposta do servidor :/ \n @Pwyll, vai arrumar! \n Erro: {E}")

        """if ( message.content =='!pipe'):
            await playSound('MC-Helper\\Discord Bot\\Botvenv\\assets\\pipe.mp3')"""
        
        if(message.content == '!wordle'):
            await message.channel.send("-----")

        if(message.content == '!russianroulette'):
            if(random.randint(0,6) == 1):
                await message.channel.send("YOU DIED")
            else:
                await message.channel.send("You lived!!")

        if(message.content == '!wisdom'):
            await message.channel.send(getRandomWikiSummary())


@client.event
async def on_disconnect():
    client.change_presence(status=discord.Status.offline)
    client.close()
    print('\033[91m'+"====--- Bot Disconnected ---====")

client.run(TOKEN)