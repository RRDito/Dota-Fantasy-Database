import os
import tkinter as tk
import CheckPerformances as cp
import FantasyDatabaseManager as fdb
import pandas as pd

root= tk.Tk()

defaultPath = os.getcwd()

#StoredPath file will be used to remember the path to the folder with the Database and the rest of the files used by the program
#Creates the StoredPath file if it doesnt exist or reads it if it exists
SPFilePath = defaultPath+os.sep+"StoredPath.txt"
if os.path.exists(SPFilePath):
  SPFile = open(SPFilePath,'r+')
else:
  SPFile = open(SPFilePath,'w+')  
StoredPath = SPFile.read()
SPFile.close()
    
print("Stored Path:",StoredPath)

DBPath = StoredPath+os.sep+"Database.xlsx"
DatabaseDF = pd.read_excel (DBPath)

#Colors Theme1
bgc = 'SlateBlue4'     #background color for windows
fgc = 'light cyan'      #font color for windows
fgcTitle = 'dark violet'      #font color for Main Title
bgcEntry = 'cornflower blue'      #background color for entry field
fgcEntry = 'DarkOrchid4'       #font color for entry field
bgcButton = 'IndianRed4'      #background color for button
fgcButton = 'goldenrod'       #font color for button
bgcButtonA = 'firebrick4'        #background color for button when pressed
fgcButtonA = 'dark goldenrod'        #font color for button when pressed
bgcSelect = 'sienna4'
fgcSelect = 'white'
bgcSelectA = 'OrangeRed4'
fgcSelectA = 'white smoke'

######################################################################
############DEFINED FUNCTIONS########################################

def FantasyRun():  
  cp.CheckPerformancesRun(root, StoredPath)
  
def DBManagerRun():  
  fdb.DBManagerRun(root)

#######################################################
#################GUI###################################

canvas1 = tk.Canvas(root, bg = bgc , width = 800, height = 600)
canvas1.pack()

version = tk.Label(root, text='version 1.1')
version.config(font=('helvetica', 8), bg = bgc, fg = fgcTitle)
canvas1.create_window(40, 15, window=version)

title0 = tk.Label(root, text='DOTA 2 FANTASY DATABASE')
title0.config(font=('helvetica', 34, 'bold'), bg = bgc, fg = fgcTitle)
canvas1.create_window(400, 50, window=title0)

buttonDBManager = tk.Button(text='Manage Database', command=DBManagerRun, bg= fgcButton, fg= bgcButton, font=('helvetica', 18, 'bold'), activebackground=fgcButtonA, activeforeground=bgcButtonA)
canvas1.create_window(400, 200, window=buttonDBManager)

buttonFantasy = tk.Button(text='Compare 2 Performances', command=FantasyRun, bg= bgcButton, fg= fgcButton, font=('helvetica', 18, 'bold'), activebackground=bgcButtonA, activeforeground=fgcButtonA)
canvas1.create_window(400, 400, window=buttonFantasy)

root.mainloop()
