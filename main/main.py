import os, threading
from dotenv import load_dotenv, find_dotenv

from subprocess import call

load_dotenv()

print("Env funcionanado: "+ str(load_dotenv(find_dotenv(), override=True)))

SERVER_LOCATION = str(os.getenv("SERVER_LOCATION"))
BACKUP_LOCATION = str(os.getenv("BACKUP_LOCATION"))
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

def runBackuper():
        call(["python","MC-Helper\\Server Manager\\Managervenv\\backup helper.py"])

def runBot():
        call(["python","MC-Helper\\Discord Bot\\Botvenv\\bot.py"])

def runTunneler():
        os.startfile("C:\\Users\\diasc\\Desktop\\Little Server\\MC-Server\\Tunneler\\bin\\playit.exe")

def runServer():
        os.chdir("C:\\Users\\diasc\\Desktop\\Little Server\\MC-Server")
        os.startfile("C:\\Users\\diasc\\Desktop\\Little Server\\MC-Server\\server.jar")

def run_Systems():
    
    print('\033[94m'+"======== Booting up systems... ========"+'\033[0m')


    threadBot = threading.Thread(target=runBot).start()

    threadTunneler = threading.Thread(target=runTunneler).start()

    threadBackup = threading.Thread(target=runBackuper).start()

    threadServer = threading.Thread(target=runServer).start()

run_Systems()