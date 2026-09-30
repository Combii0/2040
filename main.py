# Santiago Hernández Sotomonte
# Colegio Anglo Americano
# 11E.

import tkinter as tk
import random

import users
import missions 

wn = tk.Tk()

wn.title('2040')
wn.geometry('1080x720')

# –––––––––––––––––––––––––––––––––––––- VAR UTILITIES

difficulties = ['Easy', 'Medium', 'Hard']

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
        dashboardUser.config(text = f'User: {u}')

        mainTextAdvice.config(text = f'Welcome to RoboYork Control System {u.capitalize()}.\nNothing for now...')

        password.delete(0, tk.END)
        user.delete(0, tk.END)

    else:
        password.delete(0, tk.END)
        initiatePhrase.config(text = 'Invalid Credentials.')

def LogOut():
    dashboard.pack_forget()
    panel.pack()

def ShowFrame(frame):
    for widget in dashboardMainFrame.winfo_children():
        widget.grid_remove()

    frame.grid(row = 0, column = 0, sticky = 'nsew')

def CreateMission():
    ShowFrame(createMissionFrame)
    missionstate.config(text = 'Mission State: Creating Mission')

def SaveMission():
    name = missionName.get().strip()
    code = random.randint(1000000, 9999999)

    information = {'Mission Name': name, 'Mission Code': code, 'Mission Difficulty': difficulty.get(), 'Mission State': 'Initializing'}

    while code in missions.m:
        code = random.randint(1000000, 9999999)
        information = {'Mission Name': name, 'Mission Code': code, 'Mission Difficulty': difficulty.get(), 'Mission State': 'Initializing'}

    if name != '' and code != '':
        missions.m[code] = information
        ShowFrame(missionOverviewFrame)

        missionstate.config(text = f'Mission State: {missions.m[code]['Mission State']}')
        missionTitle.config(text = f'Mission: {missions.m[code]['Mission Name'].capitalize()}')
        missionCode.config(text = f'Code: {missions.m[code]['Mission Code']}')
        missionDifficulty.config(text = f'Difficulty: {missions.m[code]['Mission Difficulty']}')


    else:
        missionCreationStatus.config(text = f'Missing information.')

        missionName.delete(0, tk.END)
        missionCode.delete(0, tk.END)

def StartMission():
    pass

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
missionstate = tk.Label(dashboardTopFrame, text = 'Mission State: ')
missionstate.pack(anchor = 'w')

dashboardMenuFrame = tk.Frame(dashboard)

createMission = tk.Button(dashboardMenuFrame, text = 'Create Mission', command = CreateMission)
resources = tk.Button(dashboardMenuFrame, text = 'Resources', command = None)
processEvent = tk.Button(dashboardMenuFrame, text = 'Process Event', command = None)
simulation = tk.Button(dashboardMenuFrame, text = 'Simulation', command = None)
statistics = tk.Button(dashboardMenuFrame, text = 'Statistics', command = None)
history = tk.Button(dashboardMenuFrame, text = 'History', command = None)
generateReport = tk.Button(dashboardMenuFrame, text = 'Generate Report', command = None)
logOut = tk.Button(dashboardMenuFrame, text = 'Log Out', command = LogOut)

dashboardMainFrame = tk.Frame(dashboard)

welcomeFrame = tk.Frame(dashboardMainFrame)
mainTextAdvice = tk.Label(welcomeFrame, text = f'Welcome to RoboYork Control System...\nNothing for now...')
mainTextAdvice.pack()

# –––––––––– ORGANIZATION –––––––––––

createMission.grid                  (row = 0, sticky = 'ew')
resources.grid                      (row = 1, sticky = 'ew')
processEvent.grid                   (row = 2, sticky = 'ew')
simulation.grid                     (row = 3, sticky = 'ew')
statistics.grid                     (row = 4, sticky = 'ew')
history.grid                        (row = 5, sticky = 'ew')
generateReport.grid                 (row = 6, sticky = 'ew')
logOut.grid                         (row = 8, sticky = 'ew')

welcomeFrame.grid                   (sticky = 'ew')

# ––––––––– DASHBOARD GRID ––––––––––

dashboard.columnconfigure           (0, weight = 0)
dashboard.columnconfigure           (1, weight = 1)
dashboard.rowconfigure              (0, weight = 0)
dashboard.rowconfigure              (1, weight = 1)

dashboardMainFrame.columnconfigure  (0, weight = 1)
dashboardMainFrame.rowconfigure     (0, weight = 1)

dashboardMenuFrame.columnconfigure  (0, weight = 1)

for i in range(9):
    dashboardMenuFrame.rowconfigure (i, weight = 1)

dashboardTopFrame.grid              (row = 0, column = 0, columnspan = 2, sticky = 'ew')
dashboardMenuFrame.grid             (row = 1, column = 0, sticky = 'ns')
dashboardMainFrame.grid             (row = 1, column = 1, sticky = 'nsew')

# –––––––– NEW MISSION ––––––––––

createMissionFrame = tk.Frame(dashboardMainFrame)

newMissionTitle = tk.Label(createMissionFrame, text = 'NEW MISSION')
newMissionTitle.grid                                                                                    (row = 0, column = 0, sticky = 'ew')

tk.Label(createMissionFrame, text = 'Mission Name:').grid                                               (row = 2, column = 0, sticky = 'ew')
missionName = tk.Entry(createMissionFrame)
missionName.grid                                                                                        (row = 3, column = 0, sticky = 'ew')

difficulty = tk.StringVar(createMissionFrame)
difficulty.set(difficulties[0])

difficultySelector = tk.OptionMenu(createMissionFrame, difficulty, *difficulties)
difficultySelector.grid                                                                                 (row = 8, column = 0, sticky = 'ew')

createMissionButton = tk.Button(createMissionFrame, text = 'Create', command = SaveMission)
createMissionButton.grid                                                                                (row = 10, column = 0, sticky = 'ew')

missionCreationStatus = tk.Label(createMissionFrame, text = '')
missionCreationStatus.grid                                                                              (row = 12, column = 0, sticky = 'ew')

# ––––––– SHOW MISSION –––––––

missionOverviewFrame = tk.Frame(dashboardMainFrame)

missionTitle = tk.Label(missionOverviewFrame, text = 'Mission: N/A')
missionCode = tk.Label(missionOverviewFrame, text = 'Code: N/A')
missionDifficulty = tk.Label(missionOverviewFrame, text = 'Difficulty: N/A')
missionStartButton = tk.Button(missionOverviewFrame, text = 'Start Mission', command = StartMission)

missionTitle.grid                                                                                       (row = 0, column = 0, sticky = 'nsew')
missionCode.grid                                                                                        (row = 1, column = 0, sticky = 'nsew')
missionDifficulty.grid                                                                                  (row = 2, column = 0, sticky = 'nsew')
missionStartButton.grid                                                                                 (row = 4, column = 0, sticky = 'nsew')


wn.mainloop()