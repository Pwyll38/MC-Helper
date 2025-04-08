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

logfile = open(SERVER_LOCATION+"/logs/latest.log", "r")
loglines = follow(logfile)
for line in loglines:
    print(time.perf_counter())
    if "[Server thread/INFO]: Server empty for 60 seconds, pausing" in line:
        backup()