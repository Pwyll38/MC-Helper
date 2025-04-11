import os, threading

def runBackuper():
        os.system("python3 'MC Helper/Server Manager/Managervenv/backup helper.py'")

def runBot():
        os.system("python3 'MC Helper/Discord Bot/Botvenv/bot.py'")

def runServer():
        os.system("java -jar 'Server/server.jar'")

def runTunneler():
        os.system("start 'Tunneler/tunneler.exe'")

def run_Systems():

    print('\033[94m'+"======== Booting up systems... ========"+'\033[0m')

    threadServer = threading.Thread(target=runServer).start()

    threadBot = threading.Thread(target=runBot).start()

    threadBackup = threading.Thread(target=runBackuper).start()

    threadTunneler = threading.Thread(target=runTunneler).start()

run_Systems()