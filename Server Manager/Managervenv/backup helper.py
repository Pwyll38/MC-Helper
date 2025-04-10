import time, os, shutil, time
from dotenv import load_dotenv

load_dotenv()

SERVER_LOCATION = str(os.getenv("SERVER_LOCATION"))
BACKUP_LOCATION = str(os.getenv("BACKUP_LOCATION"))

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.2)
            continue
        yield line

def backup():
    shutil.make_archive(BACKUP_LOCATION+"/Backup "+ time.ctime(), 'zip', SERVER_LOCATION+"/world", )

print('\033[92m'+"====-----Backup Helper Live!----===="+'\033[0m')

logfile = open(SERVER_LOCATION+"/logs/latest.log", "r")
loglines = follow(logfile)
for line in loglines:
    if "[Server thread/INFO]: Server empty for 60 seconds, pausing" in line:
        print('\033[94m'+"Backup in progress..."+'\033[0m')
        backup()