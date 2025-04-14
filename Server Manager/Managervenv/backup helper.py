import time, os, shutil, time
from dotenv import load_dotenv, find_dotenv

print("Env funcionanado: "+ str(load_dotenv(find_dotenv(), override=True))) #Env nao ta funcionando no windows

SERVER_LOCATION = str(os.getenv("SERVER_LOCATION"))
BACKUP_LOCATION = str(os.getenv("BACKUP_LOCATION"))

def follow(thefile):

    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.2)
            continue
        yield line

def backup():
    windowsReadableTime = time.ctime().replace(":",".")
    shutil.make_archive(BACKUP_LOCATION+"\\Backup "+ windowsReadableTime, 'zip', SERVER_LOCATION+"\\world")

print('\033[92m'+"====-----Backup Helper Live!----===="+'\033[0m')

logfile = open(SERVER_LOCATION+"\\logs\\latest.log", "r+")
logfile.seek(0, 2)
loglines = follow(logfile)
for line in loglines:
    if "[Server thread/INFO]: Server empty for 60 seconds, pausing" in line:
        print('\033[94m'+"Backup in progress..."+'\033[0m')
        backup()
        print('\033[94m'+"Backup complete"+'\033[0m')