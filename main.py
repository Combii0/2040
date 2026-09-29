# Santiago Hernández Sotomonte
# Colegio Anglo Americano
# 11E.

import tkinter as tk
import users

wn = tk.Tk()

wn.title('2040')
wn.geometry('1080x720')

panel = tk.Frame(wn)
panel.pack()

phrase = tk.Label(panel, text = 'RoboYork 2040')
initiatePhrase = tk.Label(panel, text = 'Not account recognized...')
user = tk.Entry(panel)
password = tk.Entry(panel, show = '*')


def initiateLogin():
    u = user.get().strip()
    p = password.get()

    if users.recognizeUser(u, p):
        panel.pack_forget()
        dashboard.pack(fill = 'both', expand = True)
        dashboardUser.config(text = f'User: {u}')

        password.delete(0, tk.END)
        user.delete(0, tk.END)

    else:
        password.delete(0, tk.END)
        initiatePhrase.config(text = 'Invalid Credentials.')

def LogOut():
    dashboard.pack_forget()
    panel.pack()



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
tk.Label(dashboardTopFrame, text = 'Mission State: ').pack(anchor = 'w')

dashboardMenuFrame = tk.Frame(dashboard)

createMission = tk.Button(dashboardMenuFrame, text = 'Create Mission', command = None)
resources = tk.Button(dashboardMenuFrame, text = 'Resources', command = None)
processEvent = tk.Button(dashboardMenuFrame, text = 'Process Event', command = None)
simulation = tk.Button(dashboardMenuFrame, text = 'Simulation', command = None)
statistics = tk.Button(dashboardMenuFrame, text = 'Statistics', command = None)
history = tk.Button(dashboardMenuFrame, text = 'History', command = None)
generateReport = tk.Button(dashboardMenuFrame, text = 'Generate Report', command = None)
logOut = tk.Button(dashboardMenuFrame, text = 'Log Out', command = LogOut)

dashboardMainFrame = tk.Frame(dashboard)

mainTextAdvice = tk.Label(dashboardMainFrame, text = f'Welcome to RoboYork Control System...\nNothing for now...')

# –––––––––– ORGANIZATION –––––––––––

createMission.grid                  (row = 0, sticky = 'ew')
resources.grid                      (row = 1, sticky = 'ew')
processEvent.grid                   (row = 2, sticky = 'ew')
simulation.grid                     (row = 3, sticky = 'ew')
statistics.grid                     (row = 4, sticky = 'ew')
history.grid                        (row = 5, sticky = 'ew')
generateReport.grid                 (row = 6, sticky = 'ew')
logOut.grid                         (row = 8, sticky = 'ew')

mainTextAdvice.grid                 (sticky = 'ew')

# ––––––––– DASHBOARD GRID ––––––––––

dashboard.columnconfigure           (0, weight = 0)
dashboard.columnconfigure           (1, weight = 1)
dashboard.rowconfigure              (0, weight = 0)
dashboard.rowconfigure              (1, weight = 1)

dashboardMainFrame.columnconfigure  (0, weight = 1)
dashboardMainFrame.rowconfigure     (0, weight = 1)

dashboardMenuFrame.columnconfigure  (0, weight = 1)

for i in range(8):
    dashboardMenuFrame.rowconfigure (i, weight = 1)

dashboardTopFrame.grid              (row = 0, column = 0, columnspan = 2, sticky = 'ew')
dashboardMenuFrame.grid             (row = 1, column = 0, sticky = 'ns')
dashboardMainFrame.grid             (row = 1, column = 1, sticky = 'nsew')

wn.mainloop()