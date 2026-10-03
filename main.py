# Santiago Hernández Sotomonte
# Colegio Anglo Americano
# 11E.

import tkinter as tk
from tkinter import ttk, filedialog

import random
import json

from datetime import datetime

import users, missions, resources, events

missions.loadMissions()

wn = tk.Tk()

wn.title('2040')
wn.geometry('1080x720')

# –––––––––––––––––––––––––––––––––––––- VAR UTILITIES

difficulties = ['Easy', 'Medium', 'Hard']
activeCode = None

eventsAttended = 0
SCORE = 0

historyCodes = []

# ––––––––––––––––––––––––––––––––––––––––––––––––––––

panel = tk.Frame(wn)
panel.pack()

phrase = tk.Label(panel, text = 'RoboYork 2040')
initiatePhrase = tk.Label(panel, text = 'Not account recognized...')
user = tk.Entry(panel)
password = tk.Entry(panel, show = '*')

# –––––––––––––––––––––––––––––––––––––––––- FUNCTION UTILITIES

def initiateLogin():
    u = user.get().strip()
    p = password.get()

    if users.recognizeUser(u, p):
        panel.pack_forget()
        dashboard.pack(fill = 'both', expand = True)

        ShowFrame(welcomeFrame)

        dashboardUser.config(text = f'User: {u}')
        mainTextAdvice.config(text = f'Welcome to RoboYork Control System {u.capitalize()}.\nNothing for now...')

        if activeCode is None:
            ShowPreMissionMenu()
        else:
            ShowMissionMenu()

        password.delete(0, tk.END)
        user.delete(0, tk.END)

    else:
        password.delete(0, tk.END)
        initiatePhrase.config(text = 'Invalid Credentials.')

def LogOut():
    dashboard.pack_forget()
    panel.pack()

def ShowFrame(frame):
    frame.tkraise()

def RegisterAction(action):
    if activeCode is None:
        return

    if activeCode not in missions.m:
        return

    missions.m[activeCode].setdefault('History', [])
    missions.m[activeCode]['History'].append(action)

    missions.saveMissions()

def SaveBackup():
    defaultName = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.json')

    backupPath = filedialog.asksaveasfilename(
        title = 'Save Backup',
        initialfile = defaultName,
        defaultextension = '.json',
        filetypes = [
            ('JSON files', '*.json'),
            ('All files', '*.*')
        ]
    )

    if backupPath:
        with open(backupPath, 'w', encoding = 'utf-8') as file:
            json.dump(missions.m, file, indent = 4, ensure_ascii = False)

def HideMenuButtons():
    createMission.grid_remove()
    resourcesButton.grid_remove()
    processEvent.grid_remove()
    simulation.grid_remove()
    statistics.grid_remove()
    history.grid_remove()
    generateReport.grid_remove()
    backupButton.grid_remove()
    missionReportButton.grid_remove()

def ShowPreMissionMenu():
    HideMenuButtons()

    createMission.config(text = 'Create Mission', command = CreateMission)
    createMission.grid(row = 0, sticky = 'ew')

    backupButton.grid(row = 1, sticky = 'ew')

    logOut.grid(row = 10, sticky = 'ew')

def ShowMissionMenu():
    HideMenuButtons()

    createMission.grid(row = 0, sticky = 'ew')
    resourcesButton.grid(row = 1, sticky = 'ew')
    processEvent.grid(row = 2, sticky = 'ew')
    simulation.grid(row = 3, sticky = 'ew')
    statistics.grid(row = 4, sticky = 'ew')
    history.grid(row = 5, sticky = 'ew')

    generateReport.config(text = 'Generate Report')
    generateReport.grid(row = 6, sticky = 'ew')

    backupButton.grid(row = 7, sticky = 'ew')

    logOut.grid(row = 10, sticky = 'ew')

def ShowEndMissionMenu():
    HideMenuButtons()

    missionReportButton.grid(row = 0, sticky = 'ew')
    statistics.grid(row = 1, sticky = 'ew')
    history.grid(row = 2, sticky = 'ew')

    generateReport.config(text = 'Download')
    generateReport.grid(row = 3, sticky = 'ew')

    backupButton.grid(row = 4, sticky = 'ew')

    logOut.grid(row = 10, sticky = 'ew')

def CreateMission():
    ShowFrame(createMissionFrame)
    missionstate.config(text = 'Mission State: Creating Mission')

def SaveMission():
    name = missionName.get().strip()
    code = random.randint(1000000, 9999999)

    global activeCode

    information = {
        'Mission Name': name,
        'Mission Code': code,
        'Mission Difficulty': difficulty.get(),
        'Mission State': 'Initializing',
        'History': []
    }

    while code in missions.m:
        code = random.randint(1000000, 9999999)
        information['Mission Code'] = code

    if name:
        missions.m[code] = information
        activeCode = code

        RegisterAction('Mission created')

        ShowFrame(missionOverviewFrame)

        missionstate.config(text = f'Mission State: {missions.m[code]["Mission State"]}')
        missionTitle.config(text = f'Mission: {missions.m[code]["Mission Name"].capitalize()}')
        missionCode.config(text = f'Code: {missions.m[code]["Mission Code"]}')
        missionDifficulty.config(text = f'Difficulty: {missions.m[code]["Mission Difficulty"]}')

    else:
        missionCreationStatus.config(text = 'Missing information.')
        missionName.delete(0, tk.END)

def OpenMissionControlTab():
    missionControlName.config(text = f'Mission: {missions.m[activeCode]["Mission Name"]}')
    missionState.config(text = f'State: {missions.m[activeCode]["Mission State"]}')
    eventsProcessed.config(text = f'Events: {eventsAttended}')
    scoreShowed.config(text = f'Score: {SCORE}')

    ShowFrame(missionControlFrame)

def StartMission():
    ShowFrame(missionControlFrame)

    missions.m[activeCode]['Mission State'] = 'Operating'

    missionstate.config(text = f'Mission State: {missions.m[activeCode]["Mission State"]}')

    resources.createResources(activeCode)

    RegisterAction('Mission started')

    createMission.config(text = 'Mission Control', command = OpenMissionControlTab)

    missionControlName.config(text = f'Mission: {missions.m[activeCode]["Mission Name"]}')
    missionState.config(text = f'State: {missions.m[activeCode]["Mission State"]}')

    eventsProcessed.config(text = f'Events: {eventsAttended}')
    eventsStats.config(text = eventsAttended)

    scoreShowed.config(text = f'Score: {SCORE}')
    scoreStats.config(text = SCORE)

    ShowMissionMenu()

def ShowResources():
    if activeCode is None:
        return

    if activeCode not in resources.resources:
        return

    energyValue.config(text = resources.resources[activeCode]['Energy'])
    waterValue.config(text = resources.resources[activeCode]['Water'])
    foodValue.config(text = resources.resources[activeCode]['Food'])
    communicationValue.config(text = resources.resources[activeCode]['Communication'])

    ShowFrame(resourcesFrame)

def ShowFinalReport():
    if activeCode is None:
        return

    finalEnergyValue.config(text = resources.resources[activeCode]['Energy'])
    finalWaterValue.config(text = resources.resources[activeCode]['Water'])
    finalFoodValue.config(text = resources.resources[activeCode]['Food'])
    finalCommunicationValue.config(text = resources.resources[activeCode]['Communication'])

    finalScoreLabel.config(text = f'Score: {SCORE}')

    ShowFrame(finalDataCollected)

def EndMission():
    finalEnergyValue.config(text = resources.resources[activeCode]['Energy'])
    finalWaterValue.config(text = resources.resources[activeCode]['Water'])
    finalFoodValue.config(text = resources.resources[activeCode]['Food'])
    finalCommunicationValue.config(text = resources.resources[activeCode]['Communication'])

    finalScoreLabel.config(text = f'Score: {SCORE}')

    missions.m[activeCode]['Mission State'] = 'Finished'

    RegisterAction('Mission finished')

    missionstate.config(text = 'Mission State: Finished')

    ShowEndMissionMenu()
    ShowFrame(finalDataCollected)

def RestartSession():
    global activeCode
    global SCORE
    global eventsAttended

    eventsAttended = 0
    SCORE = 0

    eventsProcessed.config(text = f'Events: {eventsAttended}')
    eventsStats.config(text = eventsAttended)

    scoreShowed.config(text = f'Score: {SCORE}')
    scoreStats.config(text = SCORE)

    createMission.config(text = 'Create Mission', command = CreateMission)
    generateReport.config(text = 'Generate Report')

    missionstate.config(text = 'Mission State: No mission')

    activeCode = None

    ShowPreMissionMenu()
    ShowFrame(welcomeFrame)

def Stats():
    if activeCode is None:
        return

    scoreStats.config(text = SCORE)
    eventsStats.config(text = eventsAttended)
    missionStats.config(text = missions.m[activeCode]['Mission State'])

    ShowFrame(statisticsFrame)

def ShowHistory():
    global historyCodes

    historyCodes = list(missions.m.keys())

    missionList = []

    for code in historyCodes:
        missionList.append(
            f'{code} - {missions.m[code]["Mission Name"]}'
        )

    historyMissionSelector['values'] = missionList

    historyList.delete(0, tk.END)

    if len(historyCodes) > 0:
        historyMissionSelector.current(0)
        LoadHistory(None)

    ShowFrame(historyFrame)

def LoadHistory(event):
    selectedMission = historyMissionSelector.current()

    if selectedMission < 0:
        return

    code = historyCodes[selectedMission]

    historyList.delete(0, tk.END)

    for action in missions.m[code].get('History', []):
        historyList.insert(tk.END, action)

def ShowEventPopup():
    global eventsAttended

    events.newEvent()

    global missionType

    global optionA
    global optionB

    eventsAttended += 1

    missionType = events.possibleEvents[events.event]
    missions.m[activeCode]['Mission State'] = missionType

    missionState.config(text = f'State: {missions.m[activeCode]["Mission State"]}')
    missionstate.config(text = f'Mission State: {missions.m[activeCode]["Mission State"]}')

    RegisterAction(f'Event detected: {missionType}')

    optionA = random.randint(0, 4)
    optionB = random.randint(0, 4)

    while optionB == optionA:
        optionB = random.randint(0, 4)

    eventWindow = tk.Toplevel(wn)

    eventWindow.title('EMERGENCY EVENT')
    eventWindow.geometry('400x300')

    tk.Label(eventWindow, text = events.possibleEvents[events.event]).pack(pady = 20)
    tk.Label(eventWindow, text = events.affectedResources[missionType]['Text'][events.eventText]).pack(pady = 10)

    tk.Button(eventWindow, text = events.possibleActions[missionType][optionA]['Text'], command = lambda: ClosePopUp(optionA, eventWindow)).pack(pady = 0, padx = 5)
    tk.Button(eventWindow, text = events.possibleActions[missionType][optionB]['Text'], command = lambda: ClosePopUp(optionB, eventWindow)).pack(pady = 0, padx = 20)

    eventsProcessed.config(text = f'Events: {eventsAttended}')
    eventsStats.config(text = eventsAttended)

def NoImpossibleValuesInMyHouseBro():
    x = resources.resources[activeCode]

    if x['Energy'] >= 100:
        x['Energy'] = 100
    if x['Water'] >= 80:
        x['Water'] = 80
    if x['Food'] >= 70:
        x['Food'] = 70
    if x['Communication'] >= 90:
        x['Communication'] = 90

    if x['Energy'] <= 0:
        x['Energy'] = 0
    if x['Water'] <= 0:
        x['Water'] = 0
    if x['Food'] <= 0:
        x['Food'] = 0
    if x['Communication'] <= 0:
        x['Communication'] = 0

def DamageResources(option):
    global SCORE

    x = resources.resources[activeCode]

    x['Energy'] -= events.affectedResources[missionType]['Energy']
    x['Water'] -= events.affectedResources[missionType]['Water']
    x['Food'] -= events.affectedResources[missionType]['Food']
    x['Communication'] -= events.affectedResources[missionType]['Communication']

    x['Energy'] += events.possibleActions[missionType][option]['Energy']
    x['Water'] += events.possibleActions[missionType][option]['Water']
    x['Food'] += events.possibleActions[missionType][option]['Food']
    x['Communication'] += events.possibleActions[missionType][option]['Communication']

    SCORE += events.possibleActions[missionType][option]['Score']

def ClosePopUp(option, eventWindow):
    missions.m[activeCode]['Mission State'] = 'Operating'

    DamageResources(option)
    NoImpossibleValuesInMyHouseBro()

    selectedAction = events.possibleActions[missionType][option]['Text']

    RegisterAction(f'Action selected: {selectedAction}')

    RegisterAction(
        f'Energy: {resources.resources[activeCode]["Energy"]} | Water: {resources.resources[activeCode]["Water"]} | Food: {resources.resources[activeCode]["Food"]} | Communication: {resources.resources[activeCode]["Communication"]} | Score: {SCORE}'
    )

    eventWindow.destroy()

    missionState.config(text = f'State: {missions.m[activeCode]["Mission State"]}')
    missionstate.config(text = f'Mission State: {missions.m[activeCode]["Mission State"]}')

    eventsProcessed.config(text = f'Events: {eventsAttended}')
    eventsStats.config(text = eventsAttended)

    scoreShowed.config(text = f'Score: {SCORE}')
    scoreStats.config(text = SCORE)

    ShowResources()

# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––-

button = tk.Button(panel, text = 'Log In', command = initiateLogin)

# ––––––– ORGANIZATION ––––––––

phrase.pack()
user.pack()
password.pack()
button.pack()
initiatePhrase.pack()

# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

dashboard = tk.Frame(wn)

# ––––––––– TOP FRAME –––––––––

dashboardTopFrame = tk.Frame(dashboard)

tk.Label(dashboardTopFrame, text = 'RoboYork 2040').pack(anchor = 'w')

dashboardUser = tk.Label(dashboardTopFrame, text = 'User: ')
dashboardUser.pack(anchor = 'w')

missionstate = tk.Label(dashboardTopFrame, text = 'Mission State: No mission')
missionstate.pack(anchor = 'w')

dashboardMenuFrame = tk.Frame(dashboard)

createMission = tk.Button(dashboardMenuFrame, text = 'Create Mission', command = CreateMission)
resourcesButton = tk.Button(dashboardMenuFrame, text = 'Resources', command = ShowResources)
processEvent = tk.Button(dashboardMenuFrame, text = 'Process Event', command = ShowEventPopup)
simulation = tk.Button(dashboardMenuFrame, text = 'Simulation', command = None)
statistics = tk.Button(dashboardMenuFrame, text = 'Statistics', command = Stats)
history = tk.Button(dashboardMenuFrame, text = 'History', command = ShowHistory)
generateReport = tk.Button(dashboardMenuFrame, text = 'Generate Report', command = None)
backupButton = tk.Button(dashboardMenuFrame, text = 'Save Backup', command = SaveBackup)
missionReportButton = tk.Button(dashboardMenuFrame, text = 'Mission Report', command = ShowFinalReport)
logOut = tk.Button(dashboardMenuFrame, text = 'Log Out', command = LogOut)

dashboardMainFrame = tk.Frame(dashboard)

welcomeFrame = tk.Frame(dashboardMainFrame)

mainTextAdvice = tk.Label(welcomeFrame, text = f'Welcome to RoboYork Control System...\nNothing for now...')
mainTextAdvice.pack()

# –––––––––– ORGANIZATION –––––––––––

createMission.grid                  (row = 0, sticky = 'ew')
resourcesButton.grid                (row = 1, sticky = 'ew')
processEvent.grid                   (row = 2, sticky = 'ew')
simulation.grid                     (row = 3, sticky = 'ew')
statistics.grid                     (row = 4, sticky = 'ew')
history.grid                        (row = 5, sticky = 'ew')
generateReport.grid                 (row = 6, sticky = 'ew')
backupButton.grid                   (row = 7, sticky = 'ew')
missionReportButton.grid            (row = 8, sticky = 'ew')
logOut.grid                         (row = 10, sticky = 'ew')

# ––––––––– DASHBOARD GRID ––––––––––

dashboard.columnconfigure           (0, weight = 0)
dashboard.columnconfigure           (1, weight = 1)
dashboard.rowconfigure              (0, weight = 0)
dashboard.rowconfigure              (1, weight = 1)

dashboardMainFrame.columnconfigure  (0, weight = 1)
dashboardMainFrame.rowconfigure     (0, weight = 1)

dashboardMenuFrame.columnconfigure  (0, weight = 1)
dashboardMenuFrame.rowconfigure     (9, weight = 1)

dashboardTopFrame.grid              (row = 0, column = 0, columnspan = 2, sticky = 'ew')
dashboardMenuFrame.grid             (row = 1, column = 0, sticky = 'nsew')
dashboardMainFrame.grid             (row = 1, column = 1, sticky = 'nsew')

# –––––––– NEW MISSION ––––––––––

createMissionFrame = tk.Frame(dashboardMainFrame)
createMissionFrame.grid_anchor('center')

newMissionTitle = tk.Label(createMissionFrame, text = 'NEW MISSION')
newMissionTitle.grid                                                                                    (row = 0, column = 0)

tk.Label(createMissionFrame, text = 'Mission Name:').grid                                               (row = 2, column = 0)

missionName = tk.Entry(createMissionFrame)
missionName.grid                                                                                        (row = 3, column = 0)

difficulty = tk.StringVar(createMissionFrame)
difficulty.set(difficulties[0])

difficultySelector = tk.OptionMenu(createMissionFrame, difficulty, *difficulties)
difficultySelector.grid                                                                                 (row = 8, column = 0)

createMissionButton = tk.Button(createMissionFrame, text = 'Create', command = SaveMission)
createMissionButton.grid                                                                                (row = 10, column = 0)

missionCreationStatus = tk.Label(createMissionFrame, text = '')
missionCreationStatus.grid                                                                              (row = 12, column = 0)

# ––––––– SHOW MISSION –––––––

missionOverviewFrame = tk.Frame(dashboardMainFrame)
missionOverviewFrame.grid_anchor('center')

missionTitle = tk.Label(missionOverviewFrame, text = 'Mission: N/A')
missionCode = tk.Label(missionOverviewFrame, text = 'Code: N/A')
missionDifficulty = tk.Label(missionOverviewFrame, text = 'Difficulty: N/A')
missionStartButton = tk.Button(missionOverviewFrame, text = 'Start Mission', command = StartMission)

missionTitle.grid                                                                                       (row = 0, column = 0)
missionCode.grid                                                                                        (row = 1, column = 0)
missionDifficulty.grid                                                                                  (row = 2, column = 0)
missionStartButton.grid                                                                                 (row = 4, column = 0)

# –––––– START MISSION –––––––

missionControlFrame = tk.Frame(dashboardMainFrame)
missionControlFrame.grid_anchor('center')

tk.Label(missionControlFrame, text = 'MISSION CONTROL', anchor = 'center').grid(row = 0, column = 0)

missionControlName = tk.Label(missionControlFrame, text = 'Mission: N/A', anchor = 'center')
missionState = tk.Label(missionControlFrame, text = 'State: N/A', anchor = 'center')
eventsProcessed = tk.Label(missionControlFrame, text = 'Events: N/A', anchor = 'center')
scoreShowed = tk.Label(missionControlFrame, text = 'Score: N/A', anchor = 'center')
endMissionButton = tk.Button(missionControlFrame, text = 'End Mission', command = EndMission, anchor = 'center')

missionControlName.grid(row = 1, column = 0)
missionState.grid(row = 4, column = 0)
eventsProcessed.grid(row = 6, column = 0)
scoreShowed.grid(row = 7, column = 0)

endMissionButton.grid(row = 10, column = 0)

# –––––– RESOURCES ––––––

resourcesFrame = tk.Frame(dashboardMainFrame)
resourcesFrame.grid_anchor('center')

energyLabel = tk.Label(resourcesFrame, text = 'Energy')
waterLabel = tk.Label(resourcesFrame, text = 'Water')
foodLabel = tk.Label(resourcesFrame, text = 'Food')
communicationLabel = tk.Label(resourcesFrame, text = 'Communication')

energyValue = tk.Label(resourcesFrame, text = 'No database detected')
waterValue = tk.Label(resourcesFrame, text = 'No database detected')
foodValue = tk.Label(resourcesFrame, text = 'No database detected')
communicationValue = tk.Label(resourcesFrame, text = 'No database detected')

energyLabel.grid(row = 0, column = 0)
energyValue.grid(row = 0, column = 1)

waterLabel.grid(row = 1, column = 0)
waterValue.grid(row = 1, column = 1)

foodLabel.grid(row = 2, column = 0)
foodValue.grid(row = 2, column = 1)

communicationLabel.grid(row = 3, column = 0)
communicationValue.grid(row = 3, column = 1)

# ––––– END MISSION ––––––

finalDataCollected = tk.Frame(dashboardMainFrame)

tk.Label(finalDataCollected, text = 'MISSION REPORT', anchor = 'center').pack()

finalScoreLabel = tk.Label(finalDataCollected, text = 'Score: N/A', anchor = 'center')
finalScoreLabel.pack()

tk.Label(finalDataCollected, text = 'Resources:', anchor = 'center').pack()

finalResourcesFrame = tk.Frame(finalDataCollected)

finalEnergyLabel = tk.Label(finalResourcesFrame, text = 'Energy', anchor = 'center')
finalWaterLabel = tk.Label(finalResourcesFrame, text = 'Water', anchor = 'center')
finalFoodLabel = tk.Label(finalResourcesFrame, text = 'Food', anchor = 'center')
finalCommunicationLabel = tk.Label(finalResourcesFrame, text = 'Communication', anchor = 'center')

finalEnergyValue = tk.Label(finalResourcesFrame, text = 'No database detected', anchor = 'center')
finalWaterValue = tk.Label(finalResourcesFrame, text = 'No database detected', anchor = 'center')
finalFoodValue = tk.Label(finalResourcesFrame, text = 'No database detected', anchor = 'center')
finalCommunicationValue = tk.Label(finalResourcesFrame, text = 'No database detected', anchor = 'center')

finalResourcesFrame.pack()

finalEnergyLabel.grid(row = 0, column = 0)
finalEnergyValue.grid(row = 0, column = 1)

finalWaterLabel.grid(row = 1, column = 0)
finalWaterValue.grid(row = 1, column = 1)

finalFoodLabel.grid(row = 2, column = 0)
finalFoodValue.grid(row = 2, column = 1)

finalCommunicationLabel.grid(row = 3, column = 0)
finalCommunicationValue.grid(row = 3, column = 1)

endContinueButton = tk.Button(finalResourcesFrame, text = 'Continue', command = RestartSession)
endContinueButton.grid(columnspan = 2)

# ––––– STATISTICS ––––––

statisticsFrame = tk.Frame(dashboardMainFrame)

tk.Label(statisticsFrame, text = 'STATISTICS').pack()

statisticsTableFrame = tk.Frame(statisticsFrame)

scoreTableStatsText = tk.Label(statisticsTableFrame, text = 'Score')
eventsOccuredStatsText = tk.Label(statisticsTableFrame, text = 'Events Occured')
missionStateStatsText = tk.Label(statisticsTableFrame, text = 'Mission State')

scoreStats = tk.Label(statisticsTableFrame, text = 'N/A')
eventsStats = tk.Label(statisticsTableFrame, text = 'N/A')
missionStats = tk.Label(statisticsTableFrame, text = 'N/A')

scoreTableStatsText.grid(row = 0, column = 0)
scoreStats.grid(row = 0, column = 1)

eventsOccuredStatsText.grid(row = 1, column = 0)
eventsStats.grid(row = 1, column = 1)

missionStateStatsText.grid(row = 2, column = 0)
missionStats.grid(row = 2, column = 1)

statisticsTableFrame.pack()

# ––––– HISTORY –––––

historyFrame = tk.Frame(dashboardMainFrame)

tk.Label(historyFrame, text = 'HISTORY').pack()

historyMissionSelector = ttk.Combobox(
    historyFrame,
    state = 'readonly'
)

historyMissionSelector.pack()

historyMissionSelector.bind(
    '<<ComboboxSelected>>',
    LoadHistory
)

historyListFrame = tk.Frame(historyFrame)
historyListFrame.pack()

historyList = tk.Listbox(
    historyListFrame,
    width = 80,
    height = 20
)

historyScroll = tk.Scrollbar(
    historyListFrame,
    orient = 'vertical',
    command = historyList.yview
)

historyList.config(
    yscrollcommand = historyScroll.set
)

historyList.grid(row = 0, column = 0)
historyScroll.grid(row = 0, column = 1, sticky = 'ns')

# –––––––––––––––––––––––––-

pages = (
    welcomeFrame,
    createMissionFrame,
    missionOverviewFrame,
    missionControlFrame,
    resourcesFrame,
    finalDataCollected,
    statisticsFrame,
    historyFrame
)

for frame in pages:
    frame.grid(row = 0, column = 0, sticky = 'nsew')

welcomeFrame.tkraise()

ShowPreMissionMenu()

wn.mainloop()