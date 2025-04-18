import discord, os, random
from dotenv import load_dotenv, find_dotenv
from discord.ext import tasks, commands
import asyncio
import re

# Load environment variables
load_dotenv()

SERVER_LOCATION = os.getenv("SERVER_LOCATION")
BACKUP_LOCATION = os.getenv("BACKUP_LOCATION")
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID')) if os.getenv('CHANNEL_ID') else None
PIPE_SOURCE = ".\\assets\\pipe.mp3"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def getChannels():
    global channelVoice
    global channelText

    channelText = discord.utils.get(bot.get_all_channels(), name='william-botner')
    channelVoice = discord.utils.get(bot.get_all_channels(), name='Gritaria Usual')

def initFile():

    logfile = open(SERVER_LOCATION+"\\logs\\latest.log", "r")
    logfile.seek(0, 2)

    return logfile

@tasks.loop(seconds=1)
async def reactToLogs(logFile):
    try:
        line = logFile.readline()
        if line:
            if re.search(r'\[Server thread/INFO\]: Done', line):
                print("Server is online!")
                await bot.change_presence(status=discord.Status.online, activity=discord.Game('Server is online!'))
            
            elif re.search(r'\[Server thread/INFO\]: Stopping the server', line):
                print("Server is stopping...")
                await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Server is stopping...'))
                
            elif re.search(r'\[Server thread/ERROR\]: Exception', line):
                print("Server is in error state!")
                await bot.change_presence(status=discord.Status.dnd, activity=discord.Game('Server is in error state!'))
            
            elif re.search(r'\[Server thread/INFO\]:', line):
                match = re.search(r'\[Server thread/INFO\]: (\w+)\[', line)
                if match:
                    player = match.group(1)
                    if channelText:
                        await channelText.send(f"O(a) jogador(a) {player} entrou no servidor.")
                        print(f"O(a) jogador(a) {player} entrou no servidor.")

                match = re.search(r'\[Server thread/INFO\]: <.*?> (.+)', line)
                if match:
                    command = match.group(1)
                    if command == "!pipe":
                        if channelVoice:
                            voice_client = await channelVoice.connect()
                            voice_client.play(discord.FFmpegPCMAudio(PIPE_SOURCE), after=lambda e: print(f'Finished playing: {e}'))
                            while voice_client.is_playing():
                                await asyncio.sleep(1)
                            await voice_client.disconnect()
                            print(f'Finished playing pipe sound in {channelVoice.name}')
                        else:
                            print('Channel "Gritaria Usual" not found.')
                    elif command == "!ping":
                        if channelText:
                            await channelText.send('Pong!')
                            print('Pong!')

    except Exception as e:
        print(f"Error reading log file: {e}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')

    logFile = initFile()
    
    await getChannels()
    await reactToLogs.start(logFile)

@bot.command()
async def pipe(ctx=None):
    """Plays a pipe sound on the channel 'Gritaria Usual'."""
    channel = discord.utils.get(ctx.guild.voice_channels, name='Gritaria Usual')
    if channel:
        try:
            voice_client = await channel.connect()
            voice_client.play(discord.FFmpegPCMAudio(PIPE_SOURCE), after=lambda e: print(f'Finished playing: {e}'))
            while voice_client.is_playing():
                await asyncio.sleep(1)
            await voice_client.disconnect()
            print(f'Finished playing pipe sound in {channel.name}')
        except discord.ClientException as e:
            await ctx.send('Bot is already connected to a voice channel.')
            print(f'Error: {e}')
    else:
        await ctx.send('Channel "Gritaria Usual" not found.')

@bot.command()
async def ping(ctx):
    """Responds with Pong!"""
    await ctx.send('Pong!')

@bot.command()
async def gae(ctx):
    """Responds with a random percentage of being gae."""
    await ctx.send(f'Você está {random.randint(0, 100)}% gae hoje!')
    
@bot.command()
async def snek(ctx):
    """Responds with a random percentage of being snek."""
    await ctx.send("Aqui uma cobra chique: ", file=discord.File(".\\assets\\Dapper snek.png"))

# Run the bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: Bot token not found. Please set it in the .env file.")
