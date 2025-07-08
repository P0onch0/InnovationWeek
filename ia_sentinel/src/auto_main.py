import os
import time
import subprocess

LOG_PATH = '/var/log/wireshark/capture.csv'
CHECK_INTERVAL = 10  # secondes
LAST_MTIME = None

def main():
    global LAST_MTIME
    print(f"Surveillance de {LOG_PATH} ...")
    while True:
        if os.path.exists(LOG_PATH):
            mtime = os.path.getmtime(LOG_PATH)
            if LAST_MTIME is None or mtime > LAST_MTIME:
                print("Nouveau fichier détecté, traitement en cours ...")
                # Appelle main.py avec le bon chemin
                subprocess.run(['python3', 'main.py', LOG_PATH])
                LAST_MTIME = mtime
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()