import os, threading, subprocess, sys
from dotenv import load_dotenv, find_dotenv


from subprocess import call

load_dotenv()

print("Env funcionanado: "+ str(load_dotenv(find_dotenv(), override=True)))

SERVER_LOCATION = str(os.getenv("SERVER_LOCATION"))
BACKUP_LOCATION = str(os.getenv("BACKUP_LOCATION"))
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

if sys.platform == 'linux':
       osBar = '/'
elif sys.platform == 'windows':
       osBar = '\\'

def runBackuper():
        call(["python","Server Manager"+osBar+"Managervenv"+osBar+"backup helper.py"])

def runBot():
        call(["python","Discord Bot"+osBar+"Botvenv"+osBar+"bot.py"])


def runTunneler():
        file = "C:"+osBar+"Users"+osBar+"diasc"+osBar+"Desktop"+osBar+"Little Server"+osBar+"MC-Server"+osBar+"Tunneler"+osBar+"bin"+osBar+"playit.exe"
        if sys.platform == 'linux':
                print("TO-DO: Running tunneler not implemented for Linux")
                #subprocess.call(['open', file])
        elif sys.platform == 'windows':
                os.startfile(file)


def runServer():
        if sys.platform == 'linux':
                print("TO-DO: Running Server not implemented for Linux")
        elif sys.platform == 'windows':
                os.chdir("C:"+osBar+"Users"+osBar+"diasc"+osBar+"Desktop"+osBar+"Little Server"+osBar+"MC-Server")
                os.startfile("C:"+osBar+"Users"+osBar+"diasc"+osBar+"Desktop"+osBar+"Little Server"+osBar+"MC-Server"+osBar+"server.jar")



def run_Systems():
    
        print('\033[94m'+"======== Booting up systems... ========"+'\033[0m')

        threadBot = threading.Thread(target=runBot).start()

        threadTunneler = threading.Thread(target=runTunneler).start()

        threadBackup = threading.Thread(target=runBackuper).start()

        threadServer = threading.Thread(target=runServer).start()

run_Systems()