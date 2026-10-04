# Santiago Hernández Sotomonte
# Colegio Anglo Americano
# 11E.

import tkinter as tk
from tkinter import ttk, filedialog

import random
import json
import os
import sys
import ctypes
import tkinter.font as tkfont

from datetime import datetime

import users, missions, resources, events

missions.loadMissions()

BASE_WIDTH = 1080
BASE_HEIGHT = 720

def SetupAdaptiveWindow(root):
    root.update_idletasks()

    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()

    availableWidth = max(1, screenWidth - 60)
    availableHeight = max(1, screenHeight - 90)

    scale = min(
        1.0,
        availableWidth / BASE_WIDTH,
        availableHeight / BASE_HEIGHT
    )

    windowWidth = max(1, int(BASE_WIDTH * scale))
    windowHeight = max(1, int(BASE_HEIGHT * scale))

    positionX = max(0, (screenWidth - windowWidth) // 2)
    positionY = max(0, (screenHeight - windowHeight) // 2)

    root.geometry(
        f'{windowWidth}x{windowHeight}+{positionX}+{positionY}'
    )

    root.resizable(False, False)

    return scale, windowWidth, windowHeight

wn = tk.Tk()

wn.title('2040')

UI_SCALE, WINDOW_WIDTH, WINDOW_HEIGHT = SetupAdaptiveWindow(wn)

def S(value):
    if value == 0:
        return 0

    return max(1, int(round(value * UI_SCALE)))

def CenterPopup(window, width, height):
    popupWidth = S(width)
    popupHeight = S(height)

    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()

    positionX = max(0, (screenWidth - popupWidth) // 2)
    positionY = max(0, (screenHeight - popupHeight) // 2)

    window.geometry(
        f'{popupWidth}x{popupHeight}+{positionX}+{positionY}'
    )

    window.resizable(False, False)

# –––––––––––––––––––––––––––––––––––––- VISUAL STYLE

CREAM = '#DDE4DA'
ROSE = '#8F4B4E'
TEAL = '#466252'
GREEN = '#6D8873'
DARK = '#182019'
PANEL = '#202A22'
BUTTON = '#2A382F'
MUTED = '#94A197'
CYAN = '#5EB7C1'

resourceFolder = os.path.join(os.path.dirname(__file__), 'Resources')
regularFontPath = os.path.join(resourceFolder, 'pixeloid.ttf')
boldFontPath = os.path.join(resourceFolder, 'pixeloid_bold.ttf')

def RegisterMacFont(fontPath):
    if sys.platform != 'darwin' or not os.path.exists(fontPath):
        return False

    try:
        coreFoundation = ctypes.CDLL('/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation')
        coreText = ctypes.CDLL('/System/Library/Frameworks/CoreText.framework/CoreText')

        coreFoundation.CFURLCreateFromFileSystemRepresentation.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_long,
            ctypes.c_bool
        ]
        coreFoundation.CFURLCreateFromFileSystemRepresentation.restype = ctypes.c_void_p

        coreFoundation.CFRelease.argtypes = [ctypes.c_void_p]
        coreFoundation.CFRelease.restype = None

        coreText.CTFontManagerRegisterFontsForURL.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_void_p)
        ]
        coreText.CTFontManagerRegisterFontsForURL.restype = ctypes.c_bool

        encodedPath = fontPath.encode('utf-8')

        fontURL = coreFoundation.CFURLCreateFromFileSystemRepresentation(
            None,
            encodedPath,
            len(encodedPath),
            False
        )

        if not fontURL:
            return False

        error = ctypes.c_void_p()
        coreText.CTFontManagerRegisterFontsForURL(fontURL, 1, ctypes.byref(error))
        coreFoundation.CFRelease(fontURL)

        return True

    except Exception:
        return False

RegisterMacFont(regularFontPath)
RegisterMacFont(boldFontPath)

availableFamilies = tkfont.families(wn)
pixeloidFamilies = [family for family in availableFamilies if 'pixeloid' in family.lower()]

if pixeloidFamilies:
    PIXEL_FONT = pixeloidFamilies[0]
else:
    PIXEL_FONT = 'Courier New'

FONT_SMALL = (PIXEL_FONT, S(9))
FONT_BODY = (PIXEL_FONT, S(11))
FONT_BODY_BOLD = (PIXEL_FONT, S(11), 'bold')
FONT_BUTTON = (PIXEL_FONT, S(10), 'bold')
FONT_SECTION = (PIXEL_FONT, S(16), 'bold')
FONT_TITLE = (PIXEL_FONT, S(24), 'bold')
FONT_HERO = (PIXEL_FONT, S(30), 'bold')

wn.configure(bg = DARK)

def LightenColor(color, amount = 0.14):
    color = color.lstrip('#')

    red = int(color[0:2], 16)
    green = int(color[2:4], 16)
    blue = int(color[4:6], 16)

    red = int(red + (255 - red) * amount)
    green = int(green + (255 - green) * amount)
    blue = int(blue + (255 - blue) * amount)

    return f'#{red:02X}{green:02X}{blue:02X}'

class PixelButton(tk.Label):
    def __init__(self, master = None, command = None, **kwargs):
        self.command = command
        self.buttonState = kwargs.pop('state', 'normal')

        super().__init__(master, **kwargs)

        self.config(takefocus = True)

        self.bind('<Button-1>', self.InvokeCommand)
        self.bind('<Return>', self.InvokeCommand)
        self.bind('<space>', self.InvokeCommand)

    def InvokeCommand(self, event = None):
        if self.buttonState == 'disabled':
            return

        if callable(self.command):
            self.command()

    def config(self, cnf = None, **kwargs):
        if cnf:
            kwargs.update(cnf)

        if 'command' in kwargs:
            self.command = kwargs.pop('command')

        if 'state' in kwargs:
            self.buttonState = kwargs.pop('state')

            if self.buttonState == 'disabled':
                kwargs.setdefault('cursor', 'arrow')

            else:
                kwargs.setdefault('cursor', 'hand2')

        return tk.Label.config(self, **kwargs)

    configure = config

def StyleButton(widget, background = BUTTON, foreground = CREAM, border = TEAL):
    if background == DARK:
        background = BUTTON

    hoverBackground = LightenColor(background)
    hoverForeground = foreground

    widget.config(
        font = FONT_BUTTON,
        bg = background,
        fg = foreground,
        relief = 'flat',
        bd = 0,
        highlightthickness = S(2),
        highlightbackground = border,
        highlightcolor = hoverBackground,
        cursor = 'hand2',
        padx = S(14),
        pady = S(9)
    )

    def HoverIn(event):
        if getattr(widget, 'buttonState', 'normal') != 'disabled':
            widget.config(bg = hoverBackground, fg = hoverForeground)

    def HoverOut(event):
        if getattr(widget, 'buttonState', 'normal') != 'disabled':
            widget.config(bg = background, fg = foreground)

    widget.bind('<Enter>', HoverIn)
    widget.bind('<Leave>', HoverOut)

def StyleEntry(widget):
    widget.config(
        font = FONT_BODY,
        bg = DARK,
        fg = CREAM,
        insertbackground = CREAM,
        relief = 'flat',
        bd = 0,
        highlightthickness = S(2),
        highlightbackground = TEAL,
        highlightcolor = GREEN
    )

def StyleCard(widget):
    widget.config(
        bg = DARK,
        highlightbackground = TEAL,
        highlightcolor = GREEN,
        highlightthickness = S(2),
        bd = 0
    )

def ApplyPopupTheme(window):
    window.configure(bg = DARK)

    def ApplyToChildren(parent):
        for child in parent.winfo_children():
            if isinstance(child, tk.Frame):
                child.config(bg = DARK)

            elif isinstance(child, PixelButton):
                buttonText = str(child.cget('text')).lower()

                if 'failed' in buttonText or 'exit' in buttonText:
                    StyleButton(child, ROSE, CREAM, ROSE)
                else:
                    StyleButton(child, BUTTON, CREAM, TEAL)

            elif isinstance(child, tk.Label):
                labelText = str(child.cget('text'))

                if 'failed' in labelText.lower() or 'mission failed' in labelText.lower():
                    child.config(bg = DARK, fg = ROSE, font = FONT_SECTION if len(labelText) < 45 else FONT_BODY)
                elif labelText in events.possibleEvents or 'emergency' in labelText.lower():
                    child.config(bg = DARK, fg = GREEN, font = FONT_SECTION if len(labelText) < 45 else FONT_BODY)
                elif 'victorious' in labelText.lower() or 'completed' in labelText.lower():
                    child.config(bg = DARK, fg = GREEN, font = FONT_SECTION if len(labelText) < 45 else FONT_BODY)
                elif labelText.isupper() and len(labelText) < 45:
                    child.config(bg = DARK, fg = CREAM, font = FONT_SECTION)
                else:
                    child.config(bg = DARK, fg = CREAM, font = FONT_BODY)

            elif isinstance(child, tk.Listbox):
                child.config(
                    bg = DARK,
                    fg = CREAM,
                    selectbackground = TEAL,
                    selectforeground = CREAM,
                    font = FONT_BODY,
                    relief = 'flat',
                    highlightbackground = TEAL,
                    highlightcolor = GREEN,
                    highlightthickness = S(2),
                    bd = 0
                )

            ApplyToChildren(child)

    ApplyToChildren(window)

def MissionStateColor(state):
    state = str(state).lower()

    if state == 'failed':
        return ROSE

    if state in ['completed', 'resolved']:
        return GREEN

    if state in ['critical', 'alert']:
        return LightenColor(TEAL, 0.24)

    if state in ['operating', 'initializing', 'creating mission']:
        return TEAL

    return CREAM

def ResourceColor(resourceName, value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return CREAM

    alertLimits = {
        'Energy': 40,
        'Water': 30,
        'Food': 25,
        'Communication': 35
    }

    if value <= alertLimits[resourceName]:
        return LightenColor(TEAL, 0.24)

    return GREEN

def UpdateStateColors():
    if activeCode is None or activeCode not in missions.m:
        missionstate.config(fg = CREAM)
        return

    state = missions.m[activeCode]['Mission State']
    stateColor = MissionStateColor(state)

    missionstate.config(fg = stateColor)
    missionState.config(fg = stateColor)
    missionStats.config(fg = stateColor)

def UpdateResourceColors(resourceData = None):
    if resourceData is None:
        if activeCode is None or activeCode not in resources.resources:
            return
        resourceData = resources.resources[activeCode]

    resourceWidgets = {
        'Energy': (energyValue, energyStats, finalEnergyValue),
        'Water': (waterValue, waterStats, finalWaterValue),
        'Food': (foodValue, foodStats, finalFoodValue),
        'Communication': (communicationValue, communicationStats, finalCommunicationValue)
    }

    for resourceName, widgets in resourceWidgets.items():
        if resourceName not in resourceData:
            continue

        color = ResourceColor(resourceName, resourceData[resourceName])

        for widget in widgets:
            widget.config(fg = color)

# –––––––––––––––––––––––––––––––––––––- VAR UTILITIES

difficulties = ['Easy', 'Medium', 'Hard']
activeCode = None

eventsAttended = 0
SCORE = 0

finalRank = 'B'

historyCodes = []

correctDecisions = 0
incorrectDecisions = 0

loginAttempts = 0
maxLoginAttempts = 3

currentUser = None
sessionActions = []

dataFolder = os.path.join(os.path.dirname(__file__), '.data')
os.makedirs(dataFolder, exist_ok = True)

operatorFile = os.path.join(dataFolder, 'operators.json')

try:
    with open(operatorFile, 'r', encoding = 'utf-8') as file:
        createdOperators = json.load(file)

except FileNotFoundError:
    createdOperators = {}

damages = []

damagePadRunning = False
damagePadJob = None
damageID = 0
eventPopUpOpened = False

terminalBlinkState = False
terminalBlinkJob = None

# ––––––––––––––––––––––––––––––––––––––––––––––––––––

panel = tk.Frame(wn)
panel.pack(expand = True)

phrase = tk.Label(panel, text = 'RoboYork 2040')
initiatePhrase = tk.Label(panel, text = 'Not account recognized...')
user = tk.Entry(panel)
password = tk.Entry(panel, show = '*')

operatorPanel = tk.Frame(wn)

operatorPhrase = tk.Label(operatorPanel, text = 'CREATE OPERATOR')
newOperatorUser = tk.Entry(operatorPanel)
newOperatorPassword = tk.Entry(operatorPanel, show = '*')
confirmOperatorPassword = tk.Entry(operatorPanel, show = '*')
operatorStatus = tk.Label(operatorPanel, text = '')

# –––––––––––––––––––––––––––––––––––––––––- FUNCTION UTILITIES

def initiateLogin():
    global loginAttempts
    global currentUser
    global sessionActions

    u = user.get().strip()
    p = password.get()

    if not u or not p:
        initiatePhrase.config(text = 'Missing credentials.', fg = ROSE)
        return

    recognized = users.recognizeUser(u, p) or createdOperators.get(u) == p

    if recognized:
        loginAttempts = 0
        currentUser = u
        sessionActions = [f'Operator logged in: {u}']

        panel.pack_forget()
        operatorPanel.pack_forget()
        dashboard.pack(fill = 'both', expand = True)
        dashboard.lift()
        wn.update_idletasks()
        wn.update()

        ShowFrame(welcomeFrame)

        dashboardUser.config(text = f'User: {u}')
        mainTextAdvice.config(text = f'Welcome to RoboYork Control System {u.capitalize()}.\nNothing for now...')

        if activeCode is None:
            ShowPreMissionMenu()

        elif missions.m[activeCode].get('Mission Ended', missions.m[activeCode]['Mission State'] in ['Resolved', 'Completed', 'Failed']):
            RegisterAction(f'Operator logged in: {u}')
            ShowEndMissionMenu()

        else:
            RegisterAction(f'Operator logged in: {u}')
            ShowMissionMenu()
            ResumeDamagePad()

        password.delete(0, tk.END)
        user.delete(0, tk.END)
        initiatePhrase.config(text = 'Access granted.', fg = GREEN)

    else:
        loginAttempts += 1
        password.delete(0, tk.END)

        if loginAttempts >= maxLoginAttempts:
            initiatePhrase.config(text = 'Too many failed attempts. Try again in 5 seconds.', fg = ROSE)
            button.config(state = 'disabled')
            wn.after(5000, ResetLoginAttempts)

        else:
            initiatePhrase.config(text = f'Invalid Credentials. Attempt {loginAttempts}/{maxLoginAttempts}.', fg = ROSE)

def ResetLoginAttempts():
    global loginAttempts

    loginAttempts = 0
    button.config(state = 'normal')
    initiatePhrase.config(text = 'You can try again.', fg = TEAL)

def OpenCreateOperator():
    panel.pack_forget()
    operatorPanel.pack(expand = True)
    operatorPanel.lift()
    wn.update_idletasks()
    wn.update()

def SaveOperator():
    newUser = newOperatorUser.get().strip()
    newPassword = newOperatorPassword.get()
    confirmPassword = confirmOperatorPassword.get()

    if not newUser or not newPassword or not confirmPassword:
        operatorStatus.config(text = 'Missing information.', fg = ROSE)
        return

    if len(newPassword) < 4:
        operatorStatus.config(text = 'Password must contain at least 4 characters.', fg = ROSE)
        return

    if newPassword != confirmPassword:
        operatorStatus.config(text = 'Passwords do not match.', fg = ROSE)
        return

    if newUser in createdOperators:
        operatorStatus.config(text = 'Operator already exists.', fg = ROSE)
        return

    createdOperators[newUser] = newPassword

    with open(operatorFile, 'w', encoding = 'utf-8') as file:
        json.dump(createdOperators, file, indent = 4, ensure_ascii = False)

    newOperatorUser.delete(0, tk.END)
    newOperatorPassword.delete(0, tk.END)
    confirmOperatorPassword.delete(0, tk.END)

    operatorStatus.config(text = '')
    initiatePhrase.config(text = 'Operator created successfully. Please log in.', fg = GREEN)
    BackToLogin()

def BackToLogin():
    operatorPanel.pack_forget()
    dashboard.pack_forget()
    panel.pack(expand = True)
    panel.lift()
    wn.update_idletasks()
    wn.update()
    user.focus_set()

def LogOut():
    global currentUser

    if activeCode is not None and currentUser is not None:
        RegisterAction(f'Operator logged out: {currentUser}')

    PauseDamagePad()

    currentUser = None

    BackToLogin()

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
    damagePadButton.grid_remove()
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

    logOut.grid(row = 11, sticky = 'ew')

def ShowMissionMenu():
    HideMenuButtons()

    row = 0

    createMission.grid(row = row, sticky = 'ew')
    row += 1

    resourcesButton.grid(row = row, sticky = 'ew')
    row += 1

    damagePadButton.grid(row = row, sticky = 'ew')
    row += 1

    processEvent.grid(row = row, sticky = 'ew')
    row += 1

    if activeCode is not None:
        mission = missions.m[activeCode]

        if not mission.get('Manual Event Processed', False) and not mission.get('Damage Event Processed', False) and not mission.get('Simulation Used', False) and not mission.get('Victory Achieved', False):
            simulation.grid(row = row, sticky = 'ew')
            row += 1

    statistics.grid(row = row, sticky = 'ew')
    row += 1

    history.grid(row = row, sticky = 'ew')
    row += 1

    generateReport.config(text = 'Generate Report')
    generateReport.grid(row = row, sticky = 'ew')
    row += 1

    backupButton.grid(row = row, sticky = 'ew')

    logOut.grid(row = 11, sticky = 'ew')

def ShowEndMissionMenu():
    HideMenuButtons()

    missionReportButton.grid(row = 0, sticky = 'ew')
    statistics.grid(row = 1, sticky = 'ew')
    history.grid(row = 2, sticky = 'ew')

    generateReport.config(text = 'Download')
    generateReport.grid(row = 3, sticky = 'ew')

    backupButton.grid(row = 4, sticky = 'ew')

    logOut.grid(row = 11, sticky = 'ew')

def CreateMission():
    ShowFrame(createMissionFrame)
    missionstate.config(text = 'Mission State: Creating Mission', fg = TEAL)

def SaveMission():
    name = missionName.get().strip()
    code = random.randint(1000000, 9999999)

    global activeCode

    information = {
        'Mission Name': name,
        'Mission Code': code,
        'Mission Difficulty': difficulty.get(),
        'Mission State': 'Initializing',
        'History': sessionActions.copy(),
        'Correct Decisions': 0,
        'Incorrect Decisions': 0,
        'Victory Achieved': False,
        'Mission Ended': False,
        'Manual Event Processed': False,
        'Damage Event Processed': False,
        'Simulation Used': False
    }

    while code in missions.m:
        code = random.randint(1000000, 9999999)
        information['Mission Code'] = code

    if name:
        missions.m[code] = information
        activeCode = code

        RegisterAction('Mission created')

        missionCreationStatus.config(text = '')
        missionName.delete(0, tk.END)

        ShowFrame(missionOverviewFrame)

        missionstate.config(text = f'Mission State: {missions.m[code]["Mission State"]}')
        missionTitle.config(text = f'Mission: {missions.m[code]["Mission Name"].capitalize()}')
        missionCode.config(text = f'Code: {missions.m[code]["Mission Code"]}')
        missionDifficulty.config(text = f'Difficulty: {missions.m[code]["Mission Difficulty"]}')

    else:
        missionCreationStatus.config(text = 'Missing information.')
        missionName.delete(0, tk.END)

def OpenMissionControlTab():
    missionControlName.config(text = missions.m[activeCode]['Mission Name'])
    missionState.config(text = missions.m[activeCode]['Mission State'])
    eventsProcessed.config(text = eventsAttended)
    scoreShowed.config(text = SCORE)
    missionGoal.config(text = f'Victory Goal: more than {VictoryLimit()} events')

    UpdateEndMissionButton()
    ShowFrame(missionControlFrame)

def OpenDamagePad():
    DrawDamagePad()
    ShowFrame(damagePadFrame)

def StartMission():
    global correctDecisions
    global incorrectDecisions

    ShowFrame(missionControlFrame)

    correctDecisions = 0
    incorrectDecisions = 0

    missions.m[activeCode]['Correct Decisions'] = 0
    missions.m[activeCode]['Incorrect Decisions'] = 0
    missions.m[activeCode]['Victory Achieved'] = False
    missions.m[activeCode]['Mission Ended'] = False
    missions.m[activeCode]['Manual Event Processed'] = False
    missions.m[activeCode]['Damage Event Processed'] = False
    missions.m[activeCode]['Simulation Used'] = False
    missions.m[activeCode]['Mission State'] = 'Operating'

    missionstate.config(text = f'Mission State: {missions.m[activeCode]["Mission State"]}')

    events.setDifficulty(missions.m[activeCode]['Mission Difficulty'])
    resources.createResources(activeCode)

    StartDamagePad()

    RegisterAction('Mission started')

    createMission.config(text = 'Mission Control', command = OpenMissionControlTab)

    missionControlName.config(text = missions.m[activeCode]['Mission Name'])
    missionState.config(text = missions.m[activeCode]['Mission State'])
    UpdateStateColors()

    eventsProcessed.config(text = eventsAttended)
    eventsStats.config(text = eventsAttended)

    scoreShowed.config(text = SCORE)
    scoreStats.config(text = SCORE)
    missionGoal.config(text = f'Victory Goal: more than {VictoryLimit()} events')

    UpdateEndMissionButton()
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

    UpdateResourceColors()
    ShowFrame(resourcesFrame)

def ShowFinalReport():
    if activeCode is None:
        return

    mission = missions.m[activeCode]
    finalResources = mission.get('Final Resources', resources.resources.get(activeCode, {}))
    finalScore = mission.get('Final Score', SCORE)

    finalEnergyValue.config(text = finalResources.get('Energy', 'N/A'))
    finalWaterValue.config(text = finalResources.get('Water', 'N/A'))
    finalFoodValue.config(text = finalResources.get('Food', 'N/A'))
    finalCommunicationValue.config(text = finalResources.get('Communication', 'N/A'))

    finalScoreLabel.config(text = f'Score: {finalScore}')
    finalResultLabel.config(text = f'MISSION {mission["Mission State"].upper()}', fg = MissionStateColor(mission['Mission State']))
    UpdateResourceColors(finalResources)

    if mission['Mission State'] == 'Failed':
        finalRankDetected.pack_forget()

        failureReasonLabel.config(text = f'Reason: {mission.get("Failure Reason", "Unknown")}')
        failureEventLabel.config(text = f'Final Event: {mission.get("Failure Event", "Unknown")}')

        if not failureReasonLabel.winfo_ismapped():
            failureReasonLabel.pack(after = finalScoreLabel)

        if not failureEventLabel.winfo_ismapped():
            failureEventLabel.pack(after = failureReasonLabel)

    else:
        failureReasonLabel.pack_forget()
        failureEventLabel.pack_forget()

        finalRankDetected.config(text = f'Rank: {mission.get("Final Rank", determineRank())}', fg = GREEN)

        if not finalRankDetected.winfo_ismapped():
            finalRankDetected.pack(after = finalScoreLabel)

        if mission.get('Completion Reason'):
            failureReasonLabel.config(text = f'End Reason: {mission["Completion Reason"]}')
            failureEventLabel.config(text = f'Final Event: {mission.get("Completion Event", "Unknown")}')

            failureReasonLabel.pack(after = finalRankDetected)
            failureEventLabel.pack(after = failureReasonLabel)

    ShowFrame(finalDataCollected)

def SaveFinalMissionData():
    missions.m[activeCode]['Final Score'] = SCORE
    missions.m[activeCode]['Events Processed'] = eventsAttended
    missions.m[activeCode]['Correct Decisions'] = correctDecisions
    missions.m[activeCode]['Incorrect Decisions'] = incorrectDecisions
    missions.m[activeCode]['Final Resources'] = resources.resources[activeCode].copy()

    if missions.m[activeCode]['Mission State'] != 'Failed':
        missions.m[activeCode]['Final Rank'] = determineRank()

    missions.saveMissions()

def FailMission(resourceName, lastEvent):
    StopDamagePad()

    if missions.m[activeCode].get('Victory Achieved', False):
        missions.m[activeCode]['Mission State'] = 'Completed'
        missions.m[activeCode]['Mission Ended'] = True
        missions.m[activeCode]['Completion Reason'] = f'Infinite mode ended because {resourceName} reached 0.'
        missions.m[activeCode]['Completion Event'] = lastEvent if lastEvent else 'Unknown'

        RegisterAction(f'Infinite mode ended: {resourceName} reached 0.')
        RegisterAction(f'Final event: {missions.m[activeCode]["Completion Event"]}')

        SaveFinalMissionData()

        missionstate.config(text = 'Mission State: Completed')
        missionState.config(text = 'Completed')
        UpdateStateColors()

        UpdateEndMissionButton()
        ShowEndMissionMenu()
        ShowFinalReport()
        return

    missions.m[activeCode]['Mission State'] = 'Failed'
    missions.m[activeCode]['Mission Ended'] = True
    missions.m[activeCode]['Failure Reason'] = f'{resourceName} reached 0.'
    missions.m[activeCode]['Failure Event'] = lastEvent if lastEvent else 'Unknown'

    RegisterAction(f'Mission failed: {resourceName} reached 0.')
    RegisterAction(f'Failure event: {missions.m[activeCode]["Failure Event"]}')

    SaveFinalMissionData()

    missionstate.config(text = 'Mission State: Failed')
    missionState.config(text = 'Failed')
    UpdateStateColors()

    ShowEndMissionMenu()
    ShowFinalReport()

def UpdateMissionState(lastEvent = None):
    if activeCode is None:
        return None

    if activeCode not in resources.resources:
        return None

    x = resources.resources[activeCode]

    failedResource = None

    for resourceName in ['Energy', 'Water', 'Food', 'Communication']:
        if x[resourceName] <= 0:
            failedResource = resourceName
            break

    if failedResource is not None:
        victoryAlreadyAchieved = missions.m[activeCode].get('Victory Achieved', False)
        FailMission(failedResource, lastEvent)

        if victoryAlreadyAchieved:
            return 'Completed'

        return 'Failed'

    if missions.m[activeCode].get('Victory Achieved', False):
        newState = 'Completed'

    elif x['Energy'] <= 20 or x['Water'] <= 15 or x['Food'] <= 15 or x['Communication'] <= 20:
        newState = 'Critical'

    elif x['Energy'] <= 40 or x['Water'] <= 30 or x['Food'] <= 25 or x['Communication'] <= 35:
        newState = 'Alert'

    else:
        newState = 'Operating'

    oldState = missions.m[activeCode]['Mission State']
    missions.m[activeCode]['Mission State'] = newState

    if oldState != newState:
        RegisterAction(f'Mission state changed: {oldState} → {newState}')

    missionState.config(text = newState)
    missionstate.config(text = f'Mission State: {newState}')
    UpdateStateColors()

    missions.saveMissions()

    return newState

def RegisterDecision(option):
    global correctDecisions
    global incorrectDecisions

    decisionScore = events.possibleActions[missionType][option]['Score']

    if decisionScore >= 70:
        correctDecisions += 1
        decisionResult = 'Correct'

    else:
        incorrectDecisions += 1
        decisionResult = 'Incorrect'

    missions.m[activeCode]['Correct Decisions'] = correctDecisions
    missions.m[activeCode]['Incorrect Decisions'] = incorrectDecisions

    RegisterAction(f'Decision result: {decisionResult}')

def VictoryLimit():
    if activeCode is None:
        return 0

    difficultyLevel = missions.m[activeCode]['Mission Difficulty']

    if difficultyLevel == 'Easy':
        return 10

    if difficultyLevel == 'Medium':
        return 15

    return 20

def UpdateEndMissionButton():
    if activeCode is None:
        endMissionButton.grid_remove()
        return

    mission = missions.m[activeCode]

    if mission.get('Victory Achieved', False) and not mission.get('Mission Ended', False):
        endMissionButton.grid(row = 2, column = 0, columnspan = 2, pady = (S(14), S(0)))

    else:
        endMissionButton.grid_remove()

def ShowVictoryPopup():
    victoryWindow = tk.Toplevel(wn)

    victoryWindow.title('MISSION VICTORIOUS')
    CenterPopup(victoryWindow, 420, 230)
    victoryWindow.transient(wn)
    victoryWindow.grab_set()
    victoryWindow.protocol('WM_DELETE_WINDOW', lambda: None)

    tk.Label(victoryWindow, text = 'MISSION VICTORIOUS').pack(pady = (S(25), S(8)))
    tk.Label(victoryWindow, text = f'You survived {eventsAttended} events.').pack(pady = S(4))
    tk.Label(victoryWindow, text = 'End the mission now or continue indefinitely.').pack(pady = S(4))

    victoryButtons = tk.Frame(victoryWindow)
    victoryButtons.pack(pady = S(18))

    PixelButton(victoryButtons, text = 'End Mission', command = lambda: CompleteVictory(victoryWindow)).grid(row = 0, column = 0, padx = S(8))
    PixelButton(victoryButtons, text = 'Continue Indefinitely', command = lambda: ContinueIndefinitely(victoryWindow)).grid(row = 0, column = 1, padx = S(8))

    ApplyPopupTheme(victoryWindow)

def CompleteVictory(victoryWindow = None):
    if victoryWindow is not None:
        victoryWindow.grab_release()
        victoryWindow.destroy()

    EndMission()

def ContinueIndefinitely(victoryWindow):
    victoryWindow.grab_release()
    victoryWindow.destroy()

    RegisterAction('Mission continued indefinitely after victory')

    ShowMissionMenu()
    OpenMissionControlTab()
    ResumeDamagePad()

def CheckMissionVictory():
    if activeCode is None:
        return False

    mission = missions.m[activeCode]

    if mission.get('Mission Ended', False) or mission.get('Victory Achieved', False):
        return False

    if eventsAttended > VictoryLimit():
        mission['Victory Achieved'] = True
        mission['Mission State'] = 'Completed'

        RegisterAction(f'Victory condition reached after {eventsAttended} events')

        missionState.config(text = 'Completed')
        missionstate.config(text = 'Mission State: Completed')
        missionGoal.config(text = 'Victory Achieved - Continue or End Mission', fg = GREEN)
        UpdateStateColors()

        UpdateEndMissionButton()
        ShowMissionMenu()
        missions.saveMissions()

        PauseDamagePad()
        ShowVictoryPopup()
        return True

    return False

def EndMission():
    if activeCode is None:
        return

    if activeCode not in resources.resources:
        return

    mission = missions.m[activeCode]

    if not mission.get('Victory Achieved', False):
        return

    failedState = UpdateMissionState()

    if failedState == 'Failed':
        return

    StopDamagePad()

    mission['Mission State'] = 'Completed'
    mission['Mission Ended'] = True

    RegisterAction('Mission completed')

    SaveFinalMissionData()

    finalRankDetected.config(text = f'Rank: {determineRank()}')
    missionstate.config(text = 'Mission State: Completed')
    missionState.config(text = 'Completed')
    UpdateStateColors()

    UpdateEndMissionButton()
    ShowEndMissionMenu()
    ShowFinalReport()

def RestartSession():
    global activeCode
    global SCORE
    global eventsAttended
    global correctDecisions
    global incorrectDecisions
    global eventPopUpOpened

    StopDamagePad()

    damages.clear()
    eventPopUpOpened = False

    damagePadStatus.config(text = 'SYSTEM: STANDBY')

    eventsAttended = 0
    SCORE = 0
    correctDecisions = 0
    incorrectDecisions = 0

    eventsProcessed.config(text = eventsAttended)
    eventsStats.config(text = eventsAttended)

    scoreShowed.config(text = SCORE)
    scoreStats.config(text = SCORE)

    correctStats.config(text = correctDecisions)
    incorrectStats.config(text = incorrectDecisions)

    createMission.config(text = 'Create Mission', command = CreateMission)
    generateReport.config(text = 'Generate Report')

    missionstate.config(text = 'Mission State: No mission', fg = CREAM)
    missionState.config(fg = CREAM)
    missionGoal.config(fg = CREAM)

    activeCode = None

    UpdateEndMissionButton()
    ShowPreMissionMenu()
    ShowFrame(welcomeFrame)

def Stats():
    if activeCode is None:
        return

    mission = missions.m[activeCode]

    scoreStats.config(text = mission.get('Final Score', SCORE))
    eventsStats.config(text = mission.get('Events Processed', eventsAttended))
    correctStats.config(text = mission.get('Correct Decisions', correctDecisions))
    incorrectStats.config(text = mission.get('Incorrect Decisions', incorrectDecisions))
    missionStats.config(text = mission['Mission State'])

    statsResources = mission.get('Final Resources', resources.resources.get(activeCode, {}))

    energyStats.config(text = statsResources.get('Energy', 'N/A'))
    waterStats.config(text = statsResources.get('Water', 'N/A'))
    foodStats.config(text = statsResources.get('Food', 'N/A'))
    communicationStats.config(text = statsResources.get('Communication', 'N/A'))

    missionStats.config(fg = MissionStateColor(mission['Mission State']))
    UpdateResourceColors(statsResources)
    incorrectStats.config(fg = CREAM)
    correctStats.config(fg = GREEN if mission.get('Correct Decisions', correctDecisions) > 0 else CREAM)

    ShowFrame(statisticsFrame)

def ShowHistory():
    global historyCodes

    historyCodes = list(missions.m.keys())

    missionList = []

    for code in historyCodes:
        missionList.append(f'{code} - {missions.m[code]["Mission Name"]}')

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

def ShowEventPopup(source = 'Manual'):
    global eventsAttended
    global eventPopUpOpened
    global missionType
    global optionA
    global optionB

    if eventPopUpOpened:
        return

    if activeCode is None:
        return

    if activeCode not in resources.resources:
        return

    if missions.m[activeCode].get('Mission Ended', False) or missions.m[activeCode]['Mission State'] == 'Failed':
        return

    if source == 'Manual':
        missions.m[activeCode]['Manual Event Processed'] = True

    elif source == 'Damage Pad':
        missions.m[activeCode]['Damage Event Processed'] = True

    missions.saveMissions()
    simulation.grid_remove()

    eventPopUpOpened = True
    PauseDamagePad()

    events.newEvent()

    eventsAttended += 1

    missionType = events.possibleEvents[events.event]

    RegisterAction(f'Event detected: {missionType} | Source: {source}')

    optionA = random.randint(0, 4)
    optionB = random.randint(0, 4)

    while optionB == optionA:
        optionB = random.randint(0, 4)

    eventWindow = tk.Toplevel(wn)

    eventWindow.title('EMERGENCY EVENT')
    CenterPopup(eventWindow, 400, 300)
    eventWindow.transient(wn)
    eventWindow.grab_set()
    eventWindow.protocol('WM_DELETE_WINDOW', lambda: None)

    tk.Label(eventWindow, text = events.possibleEvents[events.event]).pack(pady = S(20))
    tk.Label(eventWindow, text = events.affectedResources[missionType]['Text'][events.eventText]).pack(pady = S(10))

    PixelButton(eventWindow, text = events.possibleActions[missionType][optionA]['Text'], command = lambda: ClosePopUp(optionA, eventWindow)).pack(pady = S(0), padx = S(5))
    PixelButton(eventWindow, text = events.possibleActions[missionType][optionB]['Text'], command = lambda: ClosePopUp(optionB, eventWindow)).pack(pady = S(6), padx = S(20))

    ApplyPopupTheme(eventWindow)

    eventsProcessed.config(text = eventsAttended)
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

    x['Energy'] += events.possibleActions[missionType][option]['Energy'] * events.n
    x['Water'] += events.possibleActions[missionType][option]['Water'] * events.n
    x['Food'] += events.possibleActions[missionType][option]['Food'] * events.n
    x['Communication'] += events.possibleActions[missionType][option]['Communication'] * events.n

    SCORE += events.possibleActions[missionType][option]['Score']

def ClosePopUp(option, eventWindow):
    global eventPopUpOpened

    DamageResources(option)
    NoImpossibleValuesInMyHouseBro()

    selectedAction = events.possibleActions[missionType][option]['Text']

    RegisterAction(f'Action selected: {selectedAction}')
    RegisterDecision(option)

    RegisterAction(f'Energy: {resources.resources[activeCode]["Energy"]} | Water: {resources.resources[activeCode]["Water"]} | Food: {resources.resources[activeCode]["Food"]} | Communication: {resources.resources[activeCode]["Communication"]} | Score: {SCORE}')

    eventWindow.grab_release()
    eventWindow.destroy()

    eventPopUpOpened = False

    eventsProcessed.config(text = eventsAttended)
    eventsStats.config(text = eventsAttended)

    scoreShowed.config(text = SCORE)
    scoreStats.config(text = SCORE)

    currentState = UpdateMissionState(missionType)
    UpdateResourceColors()

    if missions.m[activeCode].get('Mission Ended', False):
        StopDamagePad()
        return

    victoryReached = CheckMissionVictory()

    if not victoryReached:
        ResumeDamagePad()

def GenerateReport():
    if activeCode is None:
        return

    mission = missions.m[activeCode]

    report = ''

    report += 'ROBOYORK 2040 - MISSION REPORT\n'
    report += '================================\n\n'

    report += f'Mission Name: {mission["Mission Name"]}\n'
    report += f'Mission Code: {mission["Mission Code"]}\n'
    report += f'Difficulty: {mission["Mission Difficulty"]}\n'
    report += f'Final State: {mission["Mission State"]}\n\n'

    report += 'STATISTICS\n'
    report += '–––––––––––––––––––––––––––––––\n'

    reportScore = mission.get('Final Score', SCORE)
    reportEvents = mission.get('Events Processed', eventsAttended)
    reportResources = mission.get('Final Resources', resources.resources.get(activeCode, {}))
    reportCorrect = mission.get('Correct Decisions', correctDecisions)
    reportIncorrect = mission.get('Incorrect Decisions', incorrectDecisions)

    report += f'Score: {reportScore}\n'
    report += f'Events Processed: {reportEvents}\n'
    report += f'Correct Decisions: {reportCorrect}\n'
    report += f'Incorrect Decisions: {reportIncorrect}\n\n'

    if mission['Mission State'] == 'Failed':
        report += 'MISSION FAILED\n'
        report += f'Reason: {mission.get("Failure Reason", "Unknown")}\n'
        report += f'Final Event: {mission.get("Failure Event", "Unknown")}\n\n'

    else:
        report += f'Rank: {mission.get("Final Rank", determineRank())}\n'

        if mission.get('Completion Reason'):
            report += f'End Reason: {mission["Completion Reason"]}\n'
            report += f'Final Event: {mission.get("Completion Event", "Unknown")}\n'

        report += '\n'

    report += 'FINAL RESOURCES\n'
    report += '–––––––––––––––––––––––––––––––\n'

    report += f'Energy: {reportResources.get("Energy", "N/A")}\n'
    report += f'Water: {reportResources.get("Water", "N/A")}\n'
    report += f'Food: {reportResources.get("Food", "N/A")}\n'
    report += f'Communication: {reportResources.get("Communication", "N/A")}\n\n'

    report += 'MISSION HISTORY\n'
    report += '–––––––––––––––––––––––––––––––\n'

    for action in mission['History']:
        report += f'- {action}\n'

    defaultName = f'{mission["Mission Name"]}_{mission["Mission Code"]}.txt'

    reportPath = filedialog.asksaveasfilename(
        title = 'Download Mission Report',
        initialfile = defaultName,
        defaultextension = '.txt',
        filetypes = [
            ('Text files', '*.txt'),
            ('All files', '*.*')
        ]
    )

    if reportPath:
        with open(reportPath, 'w', encoding = 'utf-8') as file:
            file.write(report)

def determineRank():

    # F:

    if SCORE <= 100:
        finalRank = 'F-'
    elif SCORE <= 150 and SCORE > 100:
        finalRank = 'F'
    elif SCORE < 200 and SCORE > 150:
        finalRank = 'F+'

    # E:

    if SCORE >= 200 and SCORE < 250:
        finalRank = 'E-'
    elif SCORE >= 250 and SCORE < 300:
        finalRank = 'E'
    elif SCORE >= 300 and SCORE < 350:
        finalRank = 'E+'

    # D:

    if SCORE >= 350 and SCORE < 400:
        finalRank = 'D-'
    elif SCORE >= 400 and SCORE < 450:
        finalRank = 'D'
    elif SCORE >= 450 and SCORE < 500:
        finalRank = 'D+'

    # C:

    if SCORE >= 500 and SCORE < 550:
        finalRank = 'C-'
    elif SCORE >= 550 and SCORE < 600:
        finalRank = 'C'
    elif SCORE >= 600 and SCORE < 650:
        finalRank = 'C+'

    # B:

    if SCORE >= 650 and SCORE < 700:
        finalRank = 'B-'
    elif SCORE >= 700 and SCORE < 750:
        finalRank = 'B'
    elif SCORE >= 750 and SCORE < 800:
        finalRank = 'B+'

    # A:

    if SCORE >= 800 and SCORE < 850:
        finalRank = 'A-'
    elif SCORE >= 850 and SCORE < 950:
        finalRank = 'A'
    elif SCORE >= 950 and SCORE < 1000:
        finalRank = 'A+'

    # 'S:

    if SCORE >= 1000 and SCORE < 1250:
        finalRank = 'S-'
    elif SCORE >= 1250 and SCORE < 1500:
        finalRank = 'S'
    elif SCORE >= 1500:
        finalRank = 'S+, Perfect!'

    return finalRank

def ShowSimulationResults(simulationResults):
    simulationWindow = tk.Toplevel(wn)

    simulationWindow.title('SIMULATION RESULTS')
    CenterPopup(simulationWindow, 500, 400)
    simulationWindow.transient(wn)
    simulationWindow.protocol('WM_DELETE_WINDOW', lambda: EndSimulation(simulationWindow))

    tk.Label(simulationWindow, text = 'SIMULATION COMPLETED').pack(pady = S(10))

    simulationList = tk.Listbox(simulationWindow, width = 70, height = 12)
    simulationList.pack(pady = S(10))

    for result in simulationResults:
        simulationList.insert(tk.END, result)

    tk.Label(simulationWindow, text = f'Score: {SCORE}').pack()

    tk.Label(simulationWindow, text = f'Events Processed: {eventsAttended}').pack()
    PixelButton(simulationWindow, text = 'Continue', command = lambda: EndSimulation(simulationWindow)).pack(pady = S(10))

    ApplyPopupTheme(simulationWindow)

def EndSimulation(simulationWindow):
    simulationWindow.destroy()

    victoryReached = CheckMissionVictory()

    if not victoryReached and activeCode is not None and not missions.m[activeCode].get('Mission Ended', False):
        ResumeDamagePad()

def RunSimulation():
    global eventsAttended
    global missionType

    if activeCode is None:
        return

    if activeCode not in resources.resources:
        return

    if missions.m[activeCode].get('Mission Ended', False) or missions.m[activeCode]['Mission State'] == 'Failed':
        return

    if missions.m[activeCode].get('Manual Event Processed', False) or missions.m[activeCode].get('Damage Event Processed', False) or missions.m[activeCode].get('Simulation Used', False):
        return

    PauseDamagePad()

    missions.m[activeCode]['Simulation Used'] = True
    missions.saveMissions()
    simulation.grid_remove()

    difficultyLevel = missions.m[activeCode]['Mission Difficulty']

    if difficultyLevel == 'Easy':
        simulationEvents = 11

    elif difficultyLevel == 'Medium':
        simulationEvents = 16

    else:
        simulationEvents = 21

    simulationResults = []

    RegisterAction(f'Simulation started: {simulationEvents} events')

    for i in range(simulationEvents):
        events.newEvent()

        missionType = events.possibleEvents[events.event]

        option = random.randint(0, 4)

        eventsAttended += 1

        RegisterAction(f'Simulation Event: {missionType}')
        DamageResources(option)
        NoImpossibleValuesInMyHouseBro()

        selectedAction = events.possibleActions[missionType][option]['Text']

        RegisterAction(f'Simulation Action: {selectedAction}')
        RegisterDecision(option)
        RegisterAction(f'Energy: {resources.resources[activeCode]["Energy"]} | Water: {resources.resources[activeCode]["Water"]} | Food: {resources.resources[activeCode]["Food"]} | Communication: {resources.resources[activeCode]["Communication"]} | Score: {SCORE}')

        simulationResults.append(f'{i + 1}. {missionType} → {selectedAction}')

        currentState = UpdateMissionState(missionType)

        if currentState == 'Failed':
            return

    eventsProcessed.config(text = eventsAttended)
    eventsStats.config(text = eventsAttended)

    scoreShowed.config(text = SCORE)
    scoreStats.config(text = SCORE)

    RegisterAction(f'Simulation finished | Score: {SCORE}')

    ShowSimulationResults(simulationResults)

def BlinkTerminal():
    global terminalBlinkState
    global terminalBlinkJob

    terminalBlinkState = not terminalBlinkState

    if terminalBlinkState:
        damageCanvas.itemconfig(
            'terminalCore',
            state = 'hidden'
        )

    else:
        damageCanvas.itemconfig(
            'terminalCore',
            state = 'normal'
        )

    terminalBlinkJob = wn.after(
        450,
        BlinkTerminal
    )

def GridToCanvas(x, y):
    centerX = damagePadWidth / 2
    centerY = damagePadHeight / 2

    canvasX = centerX + (x * damageCellSize)
    canvasY = centerY - (y * damageCellSize)

    return canvasX, canvasY

def DrawDamagePad():
    damageCanvas.delete('all')

    centerX = damagePadWidth / 2
    centerY = damagePadHeight / 2

    for x in range(-damageLimitX, damageLimitX + 1):
        canvasX, canvasY = GridToCanvas(x, 0)

        damageCanvas.create_line(
            canvasX,
            0,
            canvasX,
            damagePadHeight,
            fill = BUTTON
        )

    for y in range(-damageLimitY, damageLimitY + 1):
        canvasX, canvasY = GridToCanvas(0, y)

        damageCanvas.create_line(0, canvasY, damagePadWidth, canvasY, fill = BUTTON)

    damageCanvas.create_line(centerX, 0, centerX, damagePadHeight, fill = TEAL, width = S(2))
    damageCanvas.create_line(0, centerY, damagePadWidth, centerY, fill = TEAL, width = S(2))
    
    terminalCanvasX, terminalCanvasY = GridToCanvas(terminalX, terminalY)

    damageCanvas.create_oval(
        terminalCanvasX - S(6),
        terminalCanvasY - S(6),
        terminalCanvasX + S(6),
        terminalCanvasY + S(6),
        fill = CYAN,
        outline = CYAN,
        tags = 'terminalCore'
    )

    damageCanvas.create_text(
        terminalCanvasX + S(16),                                                       #                            ⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀
        terminalCanvasY,                                                               #                            ⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀
        text = 'TERMINAL',                                                             #                            ⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀
        fill = CYAN,                                                                   #                            ⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀
        font = FONT_SMALL,                                                             #                            ⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆ 
        anchor = 'w',                                                                  #                            ⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿ 
        tags = 'terminalText'                                                          #                            ⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀ 
    )                                                                                  #                            ⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
                                                                                       #                            ⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀
    global terminalBlinkJob                                                            #                            ⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀
    global terminalBlinkState                                                          #                            ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀
                                                                                       #                            ⠀⠀⠀⠀ ⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀
    terminalBlinkState = False                                                         #                            ⠀⠀⠀⠀⠀ ⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀
                                                                                       #                                ⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁
    if terminalBlinkJob is not None:                                                   #                                     ⠉⠛⠻⠿⠿⠿⠿⠛⠉
        try:
            wn.after_cancel(terminalBlinkJob)
        except tk.TclError:
            pass

    for damage in damages:
        DrawDamage(damage)
    
    BlinkTerminal()
#                                                                                                        DIOMIO YA ES MUCHO CÓDIGOOOOO, se ve hasta lindo eh
def DamageCoordinateOccupied(x, y):
    for damage in damages:
        if damage['X'] == x and damage['Y'] == y:
            return True

    return False

def SpawnDamage(quadrant):
    global damageID

    if quadrant == 1:
        x = random.randint(1, damageLimitX)
        y = random.randint(1, damageLimitY)

    elif quadrant == 2:
        x = random.randint(-damageLimitX, -1)
        y = random.randint(1, damageLimitY)

    elif quadrant == 3:
        x = random.randint(-damageLimitX, -1)
        y = random.randint(-damageLimitY, -1)

    else:
        x = random.randint(1, damageLimitX)
        y = random.randint(-damageLimitY, -1)

    attempts = 0

    while DamageCoordinateOccupied(x, y) and attempts < 100:
        attempts += 1

        if quadrant == 1:
            x = random.randint(1, damageLimitX)
            y = random.randint(1, damageLimitY)

        elif quadrant == 2:
            x = random.randint(-damageLimitX, -1)
            y = random.randint(1, damageLimitY)

        elif quadrant == 3:
            x = random.randint(-damageLimitX, -1)
            y = random.randint(-damageLimitY, -1)

        else:
            x = random.randint(1, damageLimitX)
            y = random.randint(-damageLimitY, -1)

    if DamageCoordinateOccupied(x, y):
        return None

    damageID += 1

    damage = {'ID': damageID, 'X': x, 'Y': y}

    damages.append(damage)
    DrawDamage(damage)

    return damage

def DrawDamage(damage):
    canvasX, canvasY = GridToCanvas(damage['X'], damage['Y'])

    damageCanvas.create_rectangle(
        canvasX - S(6),
        canvasY - S(6),
        canvasX + S(6),
        canvasY + S(6),
        fill = ROSE,
        outline = ROSE,
        tags = ('damage', f'damage_{damage["ID"]}')
    )

    damageCanvas.tag_bind(
        f'damage_{damage["ID"]}',
        '<Button-1>',
        lambda event, damageID = damage['ID']: RepairDamage(damageID)
    )

    damageCanvas.tag_bind(
        f'damage_{damage["ID"]}',
        '<Enter>',
        lambda event: damageCanvas.config(cursor = 'hand2')
    )

    damageCanvas.tag_bind(
        f'damage_{damage["ID"]}',
        '<Leave>',
        lambda event: damageCanvas.config(cursor = '')
    )

def SpawnInitialDamages():
    global damages
    global damageID

    damages = []
    damageID = 0

    damageCanvas.delete('damage')

    SpawnDamage(1)
    SpawnDamage(2)
    SpawnDamage(3)
    SpawnDamage(4)

    damagePadStatus.config(text = f'ACTIVE DAMAGES: {len(damages)}')

def RepairDamage(damageID):

    global SCORE

    if activeCode is None:
        return

    if activeCode not in resources.resources:
        return

    if missions.m[activeCode].get('Mission Ended', False):
        return

    if not damagePadRunning or eventPopUpOpened:
        return

    damageDetected = None

    for damage in damages:
        if damage['ID'] == damageID:
            damageDetected = damage
            break

    if damageDetected is None:
        return

    if resources.resources[activeCode]['Energy'] < 3:
        damagePadStatus.config(text = 'INSUFFICIENT ENERGY - REPAIR REQUIRES 3 ENERGY')
        return

    resources.resources[activeCode]['Energy'] -= 3

    SCORE += 10

    damages.remove(damageDetected)

    damageCanvas.delete(f'damage_{damageID}')
    RegisterAction(f'Damage repaired at ({damageDetected["X"]}, {damageDetected["Y"]}) | Energy -3 | Score +10')

    SpawnDamage(random.randint(1, 4))
    SpawnDamage(random.randint(1, 4))

    damagePadStatus.config(text = f'ACTIVE DAMAGES: {len(damages)} | REPAIR COST: 3 ENERGY')

    energyValue.config(text = resources.resources[activeCode]['Energy'])
    energyStats.config(text = resources.resources[activeCode]['Energy'])

    scoreShowed.config(text = SCORE)
    scoreStats.config(text = SCORE)

    UpdateResourceColors()

    currentState = UpdateMissionState('Damage Pad Repair')

    if missions.m[activeCode].get('Mission Ended', False):
        StopDamagePad()
        return

    if currentState == 'Failed':
        return

def MoveDamageTowardsTerminal(damage):
    possibleMoves = []

    x = damage['X']
    y = damage['Y']

    if x < terminalX:
        possibleMoves.append((x + 1, y))

    elif x > terminalX:
        possibleMoves.append((x - 1, y))

    if y < terminalY:
        possibleMoves.append((x, y + 1))

    elif y > terminalY:
        possibleMoves.append((x, y - 1))

    if len(possibleMoves) == 0:
        return

    newX, newY = random.choice(possibleMoves)

    damage['X'] = newX
    damage['Y'] = newY

def MoveDamages():
    global damagePadJob

    damagePadJob = None

    if not damagePadRunning:
        return

    if activeCode is None:
        return

    if missions.m[activeCode].get('Mission Ended', False):
        return

    for damage in damages.copy():
        MoveDamageTowardsTerminal(damage)

        if damage['X'] == terminalX and damage['Y'] == terminalY:
            DrawDamagePad()
            DamageReachedTerminal(damage)
            return

    DrawDamagePad()

    if damagePadRunning:
        damagePadJob = wn.after(
            DamageMoveSpeed(),
            MoveDamages
        )

def PauseDamagePad():
    global damagePadRunning
    global damagePadJob

    damagePadRunning = False

    if damagePadJob is not None:
        try:
            wn.after_cancel(damagePadJob)
        except tk.TclError:
            pass

    damagePadJob = None

def ResumeDamagePad():
    global damagePadRunning
    global damagePadJob

    if activeCode is None:
        return

    if activeCode not in missions.m:
        return

    if activeCode not in resources.resources:
        return

    if missions.m[activeCode].get('Mission Ended', False):
        return

    if eventPopUpOpened:
        return

    if damagePadRunning and damagePadJob is not None:
        return

    damagePadRunning = True

    damagePadJob = wn.after(
        DamageMoveSpeed(),
        MoveDamages
    )

def StartDamagePad():
    global damagePadRunning
    global damagePadJob

    StopDamagePad()

    damagePadRunning = True

    SpawnInitialDamages()

    damagePadStatus.config(text = f'ACTIVE DAMAGES: {len(damages)}')

    damagePadJob = wn.after(
        DamageMoveSpeed(),
        MoveDamages
    )

def StopDamagePad():
    PauseDamagePad()

def DamageReachedTerminal(damage):
    if damage not in damages:
        return

    damages.remove(damage)

    RegisterAction(f'Damage reached terminal at ({damage["X"]}, {damage["Y"]})')

    SpawnDamage(random.randint(1, 4))

    damagePadStatus.config(text = f'TERMINAL BREACH | ACTIVE DAMAGES: {len(damages)}')

    DrawDamagePad()

    ShowEventPopup('Damage Pad')

def DamageMoveSpeed():
    difficultyLevel = missions.m[activeCode]['Mission Difficulty']

    if difficultyLevel == 'Easy':
        return 2400

    if difficultyLevel == 'Medium':
        return 1800

    if difficultyLevel == 'Hard':
        return 1200



# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––-

button = PixelButton(panel, text = 'Log In', command = initiateLogin)
createOperatorButton = PixelButton(panel, text = 'Create Operator', command = OpenCreateOperator)
exitButton = PixelButton(panel, text = 'Exit', command = wn.destroy)

saveOperatorButton = PixelButton(operatorPanel, text = 'Create', command = SaveOperator)
backToLoginButton = PixelButton(operatorPanel, text = 'Back', command = BackToLogin)

# ––––––– LOGIN ––––––––

panel.config(bg = DARK, padx = S(54), pady = S(44), highlightbackground = TEAL, highlightthickness = S(2))
phrase.config(text = '2040\nCONTROL SYSTEM', bg = DARK, fg = CREAM, font = FONT_HERO, justify = 'center')
initiatePhrase.config(bg = DARK, fg = TEAL, font = FONT_SMALL)

StyleEntry(user)
StyleEntry(password)

user.config(width = 28)
password.config(width = 28)

StyleButton(button, TEAL, CREAM, TEAL)
StyleButton(createOperatorButton, DARK, CREAM, TEAL)
StyleButton(exitButton, ROSE, CREAM, ROSE)

phrase.pack(pady = (S(0), S(30)))
tk.Label(panel, text = 'OPERATOR', bg = DARK, fg = CREAM, font = FONT_SMALL).pack(anchor = 'w')
user.pack(fill = 'x', ipady = S(8), pady = (S(4), S(12)))

tk.Label(panel, text = 'PASSWORD', bg = DARK, fg = CREAM, font = FONT_SMALL).pack(anchor = 'w')
password.pack(fill = 'x', ipady = S(8), pady = (S(4), S(20)))

button.pack(fill = 'x', pady = S(4))
createOperatorButton.pack(fill = 'x', pady = S(4))
exitButton.pack(fill = 'x', pady = S(4))

initiatePhrase.pack(pady = (S(18), S(0)))

# ––––––– CREATE OPERATOR ––––––––

operatorPanel.config(bg = DARK, padx = S(54), pady = S(44), highlightbackground = TEAL, highlightthickness = S(2))
operatorPhrase.config(bg = DARK, fg = CREAM, font = FONT_SECTION)

operatorStatus.config(bg = DARK, fg = ROSE, font = FONT_SMALL)

StyleEntry(newOperatorUser)
StyleEntry(newOperatorPassword)
StyleEntry(confirmOperatorPassword)

newOperatorUser.config(width = 28)
newOperatorPassword.config(width = 28)
confirmOperatorPassword.config(width = 28)

StyleButton(saveOperatorButton, TEAL, CREAM, TEAL)
StyleButton(backToLoginButton, DARK, CREAM, TEAL)

operatorPhrase.pack(pady = (S(0), S(26)))

tk.Label(operatorPanel, text = 'USERNAME', bg = DARK, fg = CREAM, font = FONT_SMALL).pack(anchor = 'w')
newOperatorUser.pack(fill = 'x', ipady = S(8), pady = (S(4), S(12)))

tk.Label(operatorPanel, text = 'PASSWORD', bg = DARK, fg = CREAM, font = FONT_SMALL).pack(anchor = 'w')
newOperatorPassword.pack(fill = 'x', ipady = S(8), pady = (S(4), S(12)))

tk.Label(operatorPanel, text = 'CONFIRM PASSWORD', bg = DARK, fg = CREAM, font = FONT_SMALL).pack(anchor = 'w')
confirmOperatorPassword.pack(fill = 'x', ipady = S(8), pady = (S(4), S(20)))

saveOperatorButton.pack(fill = 'x', pady = S(4))
backToLoginButton.pack(fill = 'x', pady = S(4))
operatorStatus.pack(pady = (S(16), S(0)))

# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

dashboard = tk.Frame(wn, bg = DARK)

# ––––––––– TOP FRAME –––––––––

dashboardTopFrame = tk.Frame(dashboard, bg = DARK, padx = S(24), pady = S(14))

brandFrame = tk.Frame(dashboardTopFrame, bg = DARK)
brandFrame.pack(side = 'left')

brandLabel = tk.Label(brandFrame, text = 'ROBOYORK 2040', bg = DARK, fg = CREAM, font = FONT_SECTION)
brandLabel.pack(anchor = 'w')

brandSubtitle = tk.Label(brandFrame, text = 'EMERGENCY CONTROL SYSTEM', bg = DARK, fg = TEAL, font = FONT_SMALL)
brandSubtitle.pack(anchor = 'w', pady = (S(2), S(0)))

topStatusFrame = tk.Frame(dashboardTopFrame, bg = DARK)
topStatusFrame.pack(side = 'right')

dashboardUser = tk.Label(topStatusFrame, text = 'User: ', bg = DARK, fg = CREAM, font = FONT_BODY)
dashboardUser.pack(anchor = 'e')

missionstate = tk.Label(topStatusFrame, text = 'Mission State: No mission', bg = DARK, fg = CREAM, font = FONT_BODY_BOLD)
missionstate.pack(anchor = 'e', pady = (S(4), S(0)))

# ––––––––– SIDE MENU –––––––––

dashboardMenuFrame = tk.Frame(dashboard, bg = DARK, padx = S(12), pady = S(18), width = S(220), highlightbackground = TEAL, highlightthickness = S(2))

createMission = PixelButton(dashboardMenuFrame, text = 'Create Mission', command = CreateMission)
resourcesButton = PixelButton(dashboardMenuFrame, text = 'Resources', command = ShowResources)
damagePadButton = PixelButton(dashboardMenuFrame, text = 'Damage Pad', command = OpenDamagePad)
processEvent = PixelButton(dashboardMenuFrame, text = 'Process Event', command = ShowEventPopup)
simulation = PixelButton(dashboardMenuFrame, text = 'Simulation', command = RunSimulation)
statistics = PixelButton(dashboardMenuFrame, text = 'Statistics', command = Stats)
history = PixelButton(dashboardMenuFrame, text = 'History', command = ShowHistory)
generateReport = PixelButton(dashboardMenuFrame, text = 'Generate Report', command = GenerateReport)
backupButton = PixelButton(dashboardMenuFrame, text = 'Save Backup', command = SaveBackup)
missionReportButton = PixelButton(dashboardMenuFrame, text = 'Mission Report', command = ShowFinalReport)
logOut = PixelButton(dashboardMenuFrame, text = 'Log Out', command = LogOut)

sideButtons = (
    createMission,
    resourcesButton,
    damagePadButton,
    processEvent,
    simulation,
    statistics,
    history,
    generateReport,
    backupButton,
    missionReportButton
)

for sideButton in sideButtons:
    StyleButton(sideButton, DARK, CREAM, TEAL)
    sideButton.config(
        anchor = 'w',
        activebackground = GREEN,
        activeforeground = DARK
    )

StyleButton(logOut, ROSE, CREAM, ROSE)
logOut.config(anchor = 'w')

dashboardMainFrame = tk.Frame(dashboard, bg = DARK, padx = S(34), pady = S(30))

# –––––––––– ORGANIZATION –––––––––––

createMission.grid                  (row = 0, sticky = 'ew', pady = S(3))
resourcesButton.grid                (row = 1, sticky = 'ew', pady = S(3))
damagePadButton.grid                (row = 2, sticky = 'ew', pady = S(3))
processEvent.grid                   (row = 3, sticky = 'ew', pady = S(3))
simulation.grid                     (row = 4, sticky = 'ew', pady = S(3))
statistics.grid                     (row = 5, sticky = 'ew', pady = S(3))
history.grid                        (row = 6, sticky = 'ew', pady = S(3))
generateReport.grid                 (row = 7, sticky = 'ew', pady = S(3))
backupButton.grid                   (row = 8, sticky = 'ew', pady = S(3))
missionReportButton.grid            (row = 9, sticky = 'ew', pady = S(3))
logOut.grid                         (row = 11, sticky = 'ew', pady = S(3))

# ––––––––– DASHBOARD GRID ––––––––––

dashboard.columnconfigure           (0, weight = 0)
dashboard.columnconfigure           (1, weight = 1)
dashboard.rowconfigure              (0, weight = 0)
dashboard.rowconfigure              (1, weight = 1)

dashboardMainFrame.columnconfigure  (0, weight = 1)
dashboardMainFrame.rowconfigure     (0, weight = 1)

dashboardMenuFrame.columnconfigure  (0, weight = 1)
dashboardMenuFrame.rowconfigure     (10, weight = 1)
dashboardMenuFrame.grid_propagate(False)

dashboardTopFrame.grid              (row = 0, column = 0, columnspan = 2, sticky = 'ew')
dashboardMenuFrame.grid             (row = 1, column = 0, sticky = 'nsew')
dashboardMainFrame.grid             (row = 1, column = 1, sticky = 'nsew')

# –––––––– WELCOME ––––––––––

welcomeFrame = tk.Frame(dashboardMainFrame, bg = DARK)
welcomeFrame.grid_anchor('center')

welcomeCard = tk.Frame(
    welcomeFrame,
    bg = DARK,
    padx = S(46),
    pady = S(42),
    highlightbackground = TEAL,
    highlightthickness = S(2)
)
welcomeCard.grid(row = 0, column = 0)

welcomeEyebrow = tk.Label(
    welcomeCard,
    text = 'RCS // ONLINE',
    bg = DARK,
    fg = GREEN,
    font = FONT_BODY_BOLD
)
welcomeEyebrow.pack(pady = (S(0), S(12)))

mainTextAdvice = tk.Label(
    welcomeCard,
    text = 'Welcome to RoboYork Control System...\nNothing for now...',
    bg = DARK,
    fg = CREAM,
    font = FONT_SECTION,
    justify = 'center'
)
mainTextAdvice.pack()

welcomeHint = tk.Label(
    welcomeCard,
    text = 'CREATE A MISSION TO BEGIN OPERATIONS',
    bg = DARK,
    fg = TEAL,
    font = FONT_SMALL
)
welcomeHint.pack(pady = (S(18), S(0)))

# –––––––– NEW MISSION ––––––––––

createMissionFrame = tk.Frame(dashboardMainFrame, bg = DARK)
createMissionFrame.grid_anchor('center')

createMissionCard = tk.Frame(
    createMissionFrame,
    bg = DARK,
    padx = S(44),
    pady = S(38),
    highlightbackground = TEAL,
    highlightthickness = S(2)
)
createMissionCard.grid(row = 0, column = 0)

newMissionTitle = tk.Label(
    createMissionCard,
    text = 'NEW MISSION',
    bg = DARK,
    fg = CREAM,
    font = FONT_SECTION
)
newMissionTitle.grid(row = 0, column = 0, sticky = 'w', pady = (S(0), S(24)))

missionNameLabel = tk.Label(
    createMissionCard,
    text = 'MISSION NAME',
    bg = DARK,
    fg = TEAL,
    font = FONT_SMALL
)
missionNameLabel.grid(row = 1, column = 0, sticky = 'w')

missionName = tk.Entry(createMissionCard, width = 30)
StyleEntry(missionName)
missionName.grid(row = 2, column = 0, sticky = 'ew', ipady = S(8), pady = (S(5), S(18)))

difficultyLabel = tk.Label(
    createMissionCard,
    text = 'DIFFICULTY',
    bg = DARK,
    fg = TEAL,
    font = FONT_SMALL
)
difficultyLabel.grid(row = 3, column = 0, sticky = 'w')

difficulty = tk.StringVar(createMissionCard)
difficulty.set(difficulties[0])

difficultySelector = tk.OptionMenu(createMissionCard, difficulty, *difficulties)
difficultySelector.config(
    font = FONT_BODY,
    bg = GREEN,
    fg = CREAM,
    activebackground = TEAL,
    activeforeground = DARK,
    relief = 'flat',
    highlightthickness = 0,
    width = 25
)
difficultySelector['menu'].config(
    font = FONT_BODY,
    bg = DARK,
    fg = CREAM,
    activebackground = TEAL,
    activeforeground = DARK
)
difficultySelector.grid(row = 4, column = 0, sticky = 'ew', pady = (S(5), S(22)))

createMissionButton = PixelButton(createMissionCard, text = 'Create', command = SaveMission)
StyleButton(createMissionButton, TEAL, CREAM, TEAL)
createMissionButton.grid(row = 5, column = 0, sticky = 'ew')

missionCreationStatus = tk.Label(
    createMissionCard,
    text = '',
    bg = DARK,
    fg = ROSE,
    font = FONT_SMALL
)
missionCreationStatus.grid(row = 6, column = 0, pady = (S(14), S(0)))

# ––––––– SHOW MISSION –––––––

missionOverviewFrame = tk.Frame(dashboardMainFrame, bg = DARK)
missionOverviewFrame.grid_anchor('center')

missionOverviewCard = tk.Frame(
    missionOverviewFrame,
    bg = DARK,
    padx = S(50),
    pady = S(40),
    highlightbackground = TEAL,
    highlightthickness = S(2)
)
missionOverviewCard.grid(row = 0, column = 0)

overviewTitle = tk.Label(
    missionOverviewCard,
    text = 'MISSION READY',
    bg = DARK,
    fg = GREEN,
    font = FONT_SECTION
)
overviewTitle.pack(pady = (S(0), S(24)))

missionTitle = tk.Label(missionOverviewCard, text = 'Mission: N/A', bg = DARK, fg = CREAM, font = FONT_BODY_BOLD)
missionCode = tk.Label(missionOverviewCard, text = 'Code: N/A', bg = DARK, fg = CREAM, font = FONT_BODY)
missionDifficulty = tk.Label(missionOverviewCard, text = 'Difficulty: N/A', bg = DARK, fg = CREAM, font = FONT_BODY)
missionStartButton = PixelButton(missionOverviewCard, text = 'Start Mission', command = StartMission)

missionTitle.pack(pady = S(5))
missionCode.pack(pady = S(5))
missionDifficulty.pack(pady = S(5))

StyleButton(missionStartButton, TEAL, CREAM, TEAL)
missionStartButton.pack(fill = 'x', pady = (S(24), S(0)))

# –––––– START MISSION –––––––

missionControlFrame = tk.Frame(dashboardMainFrame, bg = DARK)
missionControlFrame.grid_anchor('center')

missionControlCard = tk.Frame(
    missionControlFrame,
    bg = DARK,
    padx = S(34),
    pady = S(30),
    highlightbackground = TEAL,
    highlightthickness = S(2)
)
missionControlCard.grid(row = 0, column = 0)

missionControlHeader = tk.Label(
    missionControlCard,
    text = 'MISSION CONTROL',
    bg = DARK,
    fg = CREAM,
    font = FONT_SECTION
)
missionControlHeader.grid(row = 0, column = 0, columnspan = 2, pady = (S(0), S(18)))

missionControlTable = tk.Frame(missionControlCard, bg = DARK)
missionControlTable.grid(row = 1, column = 0, columnspan = 2, sticky = 'ew')

missionControlNameText = tk.Label(missionControlTable, text = 'Mission', bg = DARK, fg = TEAL, font = FONT_BODY_BOLD)
missionStateText = tk.Label(missionControlTable, text = 'State', bg = DARK, fg = TEAL, font = FONT_BODY_BOLD)
eventsProcessedText = tk.Label(missionControlTable, text = 'Events', bg = DARK, fg = TEAL, font = FONT_BODY_BOLD)
scoreShowedText = tk.Label(missionControlTable, text = 'Score', bg = DARK, fg = TEAL, font = FONT_BODY_BOLD)
missionGoalText = tk.Label(missionControlTable, text = 'Goal', bg = DARK, fg = TEAL, font = FONT_BODY_BOLD)

missionControlName = tk.Label(missionControlTable, text = 'N/A', bg = DARK, fg = CREAM, font = FONT_BODY)
missionState = tk.Label(missionControlTable, text = 'N/A', bg = DARK, fg = CREAM, font = FONT_BODY)
eventsProcessed = tk.Label(missionControlTable, text = 'N/A', bg = DARK, fg = CREAM, font = FONT_BODY)
scoreShowed = tk.Label(missionControlTable, text = 'N/A', bg = DARK, fg = CREAM, font = FONT_BODY)
missionGoal = tk.Label(missionControlTable, text = 'N/A', bg = DARK, fg = CREAM, font = FONT_BODY)

missionControlNameText.grid(row = 0, column = 0, sticky = 'w', padx = (S(0), S(30)), pady = S(7))
missionControlName.grid(row = 0, column = 1, sticky = 'w', pady = S(7))

missionStateText.grid(row = 1, column = 0, sticky = 'w', padx = (S(0), S(30)), pady = S(7))
missionState.grid(row = 1, column = 1, sticky = 'w', pady = S(7))

eventsProcessedText.grid(row = 2, column = 0, sticky = 'w', padx = (S(0), S(30)), pady = S(7))
eventsProcessed.grid(row = 2, column = 1, sticky = 'w', pady = S(7))

scoreShowedText.grid(row = 3, column = 0, sticky = 'w', padx = (S(0), S(30)), pady = S(7))
scoreShowed.grid(row = 3, column = 1, sticky = 'w', pady = S(7))

missionGoalText.grid(row = 4, column = 0, sticky = 'w', padx = (S(0), S(30)), pady = S(7))
missionGoal.grid(row = 4, column = 1, sticky = 'w', pady = S(7))

# –––––– DAMAGE PAD ––––––

damagePadFrame = tk.Frame(dashboardMainFrame, bg = DARK)
damagePadFrame.grid_anchor('center')

damagePadWidth = S(570)
damagePadHeight = S(330)
damageCellSize = S(30)

terminalX = 0
terminalY = -3

damageLimitX = 8
damageLimitY = 5

damagePadCard = tk.Frame(
    damagePadFrame,
    bg = DARK,
    padx = S(24),
    pady = S(18),
    highlightbackground = TEAL,
    highlightthickness = S(2)
)

damagePadCard.grid(row = 0, column = 0)

damagePadTitle = tk.Label(
    damagePadCard,
    text = 'DAMAGE PAD',
    bg = DARK,
    fg = CREAM,
    font = FONT_SECTION
)

damagePadTitle.pack(pady = (S(0), S(10)))

damageCanvas = tk.Canvas(
    damagePadCard,
    width = damagePadWidth,
    height = damagePadHeight,
    bg = DARK,
    highlightthickness = 0
)

damageCanvas.pack()

damagePadStatus = tk.Label(
    damagePadCard,
    text = 'SYSTEM: STANDBY',
    bg = DARK,
    fg = TEAL,
    font = FONT_BODY
)

damagePadStatus.pack(pady = (S(10), S(0)))

DrawDamagePad()

endMissionButton = PixelButton(missionControlCard, text = 'End Mission', command = EndMission, anchor = 'center')
StyleButton(endMissionButton, TEAL, CREAM, TEAL)

# –––––– RESOURCES ––––––

resourcesFrame = tk.Frame(dashboardMainFrame, bg = DARK)
resourcesFrame.grid_anchor('center')

resourcesCard = tk.Frame(
    resourcesFrame,
    bg = DARK,
    padx = S(38),
    pady = S(32),
    highlightbackground = TEAL,
    highlightthickness = S(2)
)
resourcesCard.grid(row = 0, column = 0)

resourcesTitle = tk.Label(resourcesCard, text = 'RESOURCES', bg = DARK, fg = CREAM, font = FONT_SECTION)
resourcesTitle.grid(row = 0, column = 0, pady = (S(0), S(18)))

resourcesTableFrame = tk.Frame(resourcesCard, bg = DARK, padx = S(16), pady = S(14))
resourcesTableFrame.grid(row = 1, column = 0)

resourceHeader = tk.Label(resourcesTableFrame, text = 'RESOURCE', bg = DARK, fg = TEAL, font = FONT_BODY_BOLD)
currentHeader = tk.Label(resourcesTableFrame, text = 'CURRENT', bg = DARK, fg = TEAL, font = FONT_BODY_BOLD)
maximumHeader = tk.Label(resourcesTableFrame, text = 'MAX', bg = DARK, fg = TEAL, font = FONT_BODY_BOLD)

resourceHeader.grid(row = 0, column = 0, sticky = 'w', padx = S(14), pady = (S(4), S(10)))
currentHeader.grid(row = 0, column = 1, padx = S(14), pady = (S(4), S(10)))
maximumHeader.grid(row = 0, column = 2, padx = S(14), pady = (S(4), S(10)))

energyLabel = tk.Label(resourcesTableFrame, text = 'Energy', bg = DARK, fg = CREAM, font = FONT_BODY)
waterLabel = tk.Label(resourcesTableFrame, text = 'Water', bg = DARK, fg = CREAM, font = FONT_BODY)
foodLabel = tk.Label(resourcesTableFrame, text = 'Food', bg = DARK, fg = CREAM, font = FONT_BODY)
communicationLabel = tk.Label(resourcesTableFrame, text = 'Communication', bg = DARK, fg = CREAM, font = FONT_BODY)

energyValue = tk.Label(resourcesTableFrame, text = 'No database detected', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
waterValue = tk.Label(resourcesTableFrame, text = 'No database detected', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
foodValue = tk.Label(resourcesTableFrame, text = 'No database detected', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
communicationValue = tk.Label(resourcesTableFrame, text = 'No database detected', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)

resourceRows = (
    (1, energyLabel, energyValue, '100'),
    (2, waterLabel, waterValue, '80'),
    (3, foodLabel, foodValue, '70'),
    (4, communicationLabel, communicationValue, '90')
)

for rowNumber, resourceLabel, valueLabel, maximumValue in resourceRows:
    resourceLabel.grid(row = rowNumber, column = 0, sticky = 'w', padx = S(14), pady = S(8))
    valueLabel.grid(row = rowNumber, column = 1, padx = S(14), pady = S(8))

    tk.Label(
        resourcesTableFrame,
        text = maximumValue,
        bg = DARK,
        fg = CREAM,
        font = FONT_BODY
    ).grid(row = rowNumber, column = 2, padx = S(14), pady = S(8))

# ––––– END MISSION ––––––

finalDataCollected = tk.Frame(dashboardMainFrame, bg = DARK)
finalDataCollected.grid_anchor('center')

finalCard = tk.Frame(
    finalDataCollected,
    bg = DARK,
    padx = S(38),
    pady = S(28),
    highlightbackground = TEAL,
    highlightthickness = S(2)
)
finalCard.grid(row = 0, column = 0)

finalReportTitle = tk.Label(finalCard, text = 'MISSION REPORT', bg = DARK, fg = CREAM, font = FONT_SECTION)
finalReportTitle.pack(pady = (S(0), S(10)))

finalResultLabel = tk.Label(finalCard, text = 'MISSION RESULT', bg = DARK, fg = TEAL, font = FONT_BODY_BOLD)
finalResultLabel.pack(pady = S(4))

finalScoreLabel = tk.Label(finalCard, text = 'Score: N/A', bg = DARK, fg = CREAM, font = FONT_BODY)
finalScoreLabel.pack(pady = S(3))

finalRankDetected = tk.Label(finalCard, text = f'Rank: {determineRank()}', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
finalRankDetected.pack(pady = S(3))

failureReasonLabel = tk.Label(finalCard, text = '', bg = DARK, fg = ROSE, font = FONT_BODY, wraplength = S(620))
failureEventLabel = tk.Label(finalCard, text = '', bg = DARK, fg = ROSE, font = FONT_BODY)

finalResourcesTitle = tk.Label(finalCard, text = 'FINAL RESOURCES', bg = DARK, fg = TEAL, font = FONT_BODY_BOLD)
finalResourcesTitle.pack(pady = (S(18), S(8)))

finalResourcesFrame = tk.Frame(finalCard, bg = DARK, padx = S(18), pady = S(12))
finalResourcesFrame.pack()

finalEnergyLabel = tk.Label(finalResourcesFrame, text = 'Energy', bg = DARK, fg = CREAM, font = FONT_BODY)
finalWaterLabel = tk.Label(finalResourcesFrame, text = 'Water', bg = DARK, fg = CREAM, font = FONT_BODY)
finalFoodLabel = tk.Label(finalResourcesFrame, text = 'Food', bg = DARK, fg = CREAM, font = FONT_BODY)
finalCommunicationLabel = tk.Label(finalResourcesFrame, text = 'Communication', bg = DARK, fg = CREAM, font = FONT_BODY)

finalEnergyValue = tk.Label(finalResourcesFrame, text = 'No database detected', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
finalWaterValue = tk.Label(finalResourcesFrame, text = 'No database detected', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
finalFoodValue = tk.Label(finalResourcesFrame, text = 'No database detected', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
finalCommunicationValue = tk.Label(finalResourcesFrame, text = 'No database detected', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)

finalEnergyLabel.grid(row = 0, column = 0, sticky = 'w', padx = S(12), pady = S(6))
finalEnergyValue.grid(row = 0, column = 1, padx = S(12), pady = S(6))

finalWaterLabel.grid(row = 1, column = 0, sticky = 'w', padx = S(12), pady = S(6))
finalWaterValue.grid(row = 1, column = 1, padx = S(12), pady = S(6))

finalFoodLabel.grid(row = 2, column = 0, sticky = 'w', padx = S(12), pady = S(6))
finalFoodValue.grid(row = 2, column = 1, padx = S(12), pady = S(6))

finalCommunicationLabel.grid(row = 3, column = 0, sticky = 'w', padx = S(12), pady = S(6))
finalCommunicationValue.grid(row = 3, column = 1, padx = S(12), pady = S(6))

endContinueButton = PixelButton(finalCard, text = 'Continue', command = RestartSession)
StyleButton(endContinueButton, TEAL, CREAM, TEAL)
endContinueButton.pack(fill = 'x', pady = (S(18), S(0)))

# ––––– STATISTICS ––––––

statisticsFrame = tk.Frame(dashboardMainFrame, bg = DARK)
statisticsFrame.grid_anchor('center')

statisticsCard = tk.Frame(
    statisticsFrame,
    bg = DARK,
    padx = S(38),
    pady = S(30),
    highlightbackground = TEAL,
    highlightthickness = S(2)
)
statisticsCard.grid(row = 0, column = 0)

statisticsTitle = tk.Label(statisticsCard, text = 'STATISTICS', bg = DARK, fg = CREAM, font = FONT_SECTION)
statisticsTitle.pack(pady = (S(0), S(18)))

statisticsTableFrame = tk.Frame(statisticsCard, bg = DARK, padx = S(18), pady = S(14))

scoreTableStatsText = tk.Label(statisticsTableFrame, text = 'Score', bg = DARK, fg = CREAM, font = FONT_BODY)
eventsOccuredStatsText = tk.Label(statisticsTableFrame, text = 'Events Occurred', bg = DARK, fg = CREAM, font = FONT_BODY)
correctDecisionsStatsText = tk.Label(statisticsTableFrame, text = 'Correct Decisions', bg = DARK, fg = CREAM, font = FONT_BODY)
incorrectDecisionsStatsText = tk.Label(statisticsTableFrame, text = 'Incorrect Decisions', bg = DARK, fg = CREAM, font = FONT_BODY)
energyStatsText = tk.Label(statisticsTableFrame, text = 'Energy', bg = DARK, fg = CREAM, font = FONT_BODY)
waterStatsText = tk.Label(statisticsTableFrame, text = 'Water', bg = DARK, fg = CREAM, font = FONT_BODY)
foodStatsText = tk.Label(statisticsTableFrame, text = 'Food', bg = DARK, fg = CREAM, font = FONT_BODY)
communicationStatsText = tk.Label(statisticsTableFrame, text = 'Communication', bg = DARK, fg = CREAM, font = FONT_BODY)
missionStateStatsText = tk.Label(statisticsTableFrame, text = 'Mission State', bg = DARK, fg = CREAM, font = FONT_BODY)

scoreStats = tk.Label(statisticsTableFrame, text = 'N/A', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
eventsStats = tk.Label(statisticsTableFrame, text = 'N/A', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
correctStats = tk.Label(statisticsTableFrame, text = 'N/A', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
incorrectStats = tk.Label(statisticsTableFrame, text = 'N/A', bg = DARK, fg = CREAM, font = FONT_BODY_BOLD)
energyStats = tk.Label(statisticsTableFrame, text = 'N/A', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
waterStats = tk.Label(statisticsTableFrame, text = 'N/A', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
foodStats = tk.Label(statisticsTableFrame, text = 'N/A', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
communicationStats = tk.Label(statisticsTableFrame, text = 'N/A', bg = DARK, fg = GREEN, font = FONT_BODY_BOLD)
missionStats = tk.Label(statisticsTableFrame, text = 'N/A', bg = DARK, fg = CREAM, font = FONT_BODY_BOLD)

statisticsRows = (
    (0, scoreTableStatsText, scoreStats),
    (1, eventsOccuredStatsText, eventsStats),
    (2, correctDecisionsStatsText, correctStats),
    (3, incorrectDecisionsStatsText, incorrectStats),
    (4, energyStatsText, energyStats),
    (5, waterStatsText, waterStats),
    (6, foodStatsText, foodStats),
    (7, communicationStatsText, communicationStats),
    (8, missionStateStatsText, missionStats)
)

for rowNumber, statLabel, statValue in statisticsRows:
    statLabel.grid(row = rowNumber, column = 0, sticky = 'w', padx = (S(10), S(34)), pady = S(6))
    statValue.grid(row = rowNumber, column = 1, sticky = 'e', padx = S(10), pady = S(6))

statisticsTableFrame.pack()

# ––––– HISTORY –––––

historyFrame = tk.Frame(dashboardMainFrame, bg = DARK)
historyFrame.grid_anchor('center')

historyCard = tk.Frame(
    historyFrame,
    bg = DARK,
    padx = S(34),
    pady = S(28),
    highlightbackground = TEAL,
    highlightthickness = S(2)
)
historyCard.grid(row = 0, column = 0)

historyTitle = tk.Label(historyCard, text = 'HISTORY', bg = DARK, fg = CREAM, font = FONT_SECTION)
historyTitle.pack(pady = (S(0), S(14)))

historySelectorLabel = tk.Label(
    historyCard,
    text = 'SELECT MISSION',
    bg = DARK,
    fg = TEAL,
    font = FONT_SMALL
)
historySelectorLabel.pack(anchor = 'w')

ttkStyle = ttk.Style()
try:
    ttkStyle.theme_use('clam')
except tk.TclError:
    pass

ttkStyle.configure(
    'RCS.TCombobox',
    fieldbackground = DARK,
    background = DARK,
    foreground = CREAM,
    arrowcolor = CREAM,
    bordercolor = TEAL,
    lightcolor = TEAL,
    darkcolor = TEAL,
    padding = 7,
    font = FONT_BODY
)

ttkStyle.map(
    'RCS.TCombobox',
    fieldbackground = [('readonly', DARK)],
    foreground = [('readonly', CREAM)],
    selectbackground = [('readonly', DARK)],
    selectforeground = [('readonly', CREAM)],
    bordercolor = [('focus', GREEN), ('readonly', TEAL)]
)

historyMissionSelector = ttk.Combobox(
    historyCard,
    state = 'readonly',
    style = 'RCS.TCombobox',
    width = 46
)

historyMissionSelector.pack(fill = 'x', pady = (S(5), S(14)))

historyMissionSelector.bind(
    '<<ComboboxSelected>>',
    LoadHistory
)

historyListFrame = tk.Frame(historyCard, bg = DARK)
historyListFrame.pack()

historyList = tk.Listbox(
    historyListFrame,
    width = 78,
    height = 18,
    bg = DARK,
    fg = CREAM,
    selectbackground = TEAL,
    selectforeground = CREAM,
    font = FONT_BODY,
    relief = 'flat',
    highlightbackground = TEAL,
    highlightcolor = GREEN,
    highlightthickness = S(2),
    bd = 0
)

historyScroll = tk.Scrollbar(
    historyListFrame,
    orient = 'vertical',
    command = historyList.yview,
    bg = TEAL,
    activebackground = GREEN,
    troughcolor = DARK,
    relief = 'flat',
    bd = 0
)

historyList.config(
    yscrollcommand = historyScroll.set
)

historyList.grid(row = 0, column = 0)
historyScroll.grid(row = 0, column = 1, sticky = 'ns')

# ––––––––––– DAMAGE PAD ––––––––––


pages = (
    welcomeFrame,
    createMissionFrame,
    missionOverviewFrame,
    missionControlFrame,
    damagePadFrame,
    resourcesFrame,
    finalDataCollected,
    statisticsFrame,
    historyFrame
)

for frame in pages:
    frame.grid(row = 0, column = 0, sticky = 'nsew')

welcomeFrame.tkraise()

UpdateEndMissionButton()
ShowPreMissionMenu()

wn.mainloop()