import json
import os

from datetime import datetime

m = {}

def backupMissions():
    backupFolder = os.path.join(os.path.dirname(__file__), 'backups')

    os.makedirs(backupFolder, exist_ok = True)

    date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    backupPath = os.path.join(
        backupFolder,
        f'missions_{date}.json'
    )

    with open(backupPath, 'w', encoding = 'utf-8') as file:
        json.dump(m, file, indent = 4, ensure_ascii = False)

filePath = os.path.join(os.path.dirname(__file__), 'missions.json')

def saveMissions():
    with open(filePath, 'w', encoding = 'utf-8') as file:
        json.dump(m, file, indent = 4, ensure_ascii = False)

def loadMissions():
    global m

    try:
        with open(filePath, 'r', encoding = 'utf-8') as file:
            savedMissions = json.load(file)

        m = {}

        for code in savedMissions:
            m[int(code)] = savedMissions[code]

    except FileNotFoundError:
        m = {}