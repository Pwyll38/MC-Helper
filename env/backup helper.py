import time, os, shutil, time
from dotenv import load_dotenv, find_dotenv

print("Env funcionanado: "+ str(load_dotenv(find_dotenv(), override=True)))

SERVER_LOCATION = str(os.getenv("SERVER_LOCATION"))
BACKUP_LOCATION = str(os.getenv("BACKUP_LOCATION"))

def backup():
    try:
        windowsReadableTime = time.ctime().replace(":",".")
        shutil.make_archive(BACKUP_LOCATION+"\\Backup "+ windowsReadableTime, 'zip', SERVER_LOCATION+"\\world")
    except Exception as error:
        print("Error starting backup: "+ str(error))

print('\033[92m'+"====-----Backup Helper Live!----===="+'\033[0m')

print('\033[94m'+"Backup in progress..."+'\033[0m')
backup()
print('\033[94m'+"Backup complete"+'\033[0m')