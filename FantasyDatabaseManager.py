import os
import tkinter as tk
from tkinter.filedialog import askdirectory
import jsonScrap as js
import LiquipediaScrap as ls
import OpenDotaScrap as ods
import OpenDotaHeroes as odh
import pandas as pd

def DBManagerRun(root):
  root2= tk.Toplevel(root)
  FolderPath = tk.StringVar()
  LiquiPage = tk.StringVar()
  SpecificMatch = tk.StringVar()

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

  def SelectFolder():
    FolderPath.set( askdirectory(title='Select Folder') )  

  def UpdateStoredPath(p):
    SPFilePath = defaultPath+os.sep+"StoredPath.txt"
    SPFile = open(SPFilePath,'w')
    SPFile.write(p)
    SPFile.close()
    print("Stored Path:",p)  

  def GetDBPath():
    FolderPath = entry1.get()  
  
    if FolderPath == "":
      DBPath = StoredPath+os.sep+"Database.xlsx"
    else:
      DBPath = FolderPath+os.sep+"Database.xlsx"    
      UpdateStoredPath(FolderPath)

    return DBPath

  def GetFolderPath():
    FolderPath = entry1.get()
  
    if FolderPath != "":
      #if there is a path specified the path is saved into Stored Path
      UpdateStoredPath(FolderPath)  
    else:
      #if no path was specified take it from Stored Path
      FolderPath = StoredPath

      return FolderPath


  ###################################################
  ## Functions that modify the Database ##############

  #Adds the Liquipedia Page in the entry field to the queue for Liquipedia Scrap to be used when Update is ran
  def QueueLiquipediaPage():
    LiquiPage = entry2.get()
    FolderPath = entry1.get()
  
    if FolderPath == "":
      LinkTPath = StoredPath+os.sep+"liquipedia.txt"
      LinkAPath = StoredPath+os.sep+"liquipediaAdded.txt"
    else:
      LinkTPath = FolderPath+os.sep+"liquipedia.txt"
      LinkAPath = StoredPath+os.sep+"liquipediaAdded.txt"    
      UpdateStoredPath(FolderPath)     
  
    print("Opening ",LinkTPath)
    print("Opening ",LinkAPath)

    LinkTXT = pd.read_csv (LinkTPath)
    LinkDF = pd.DataFrame(LinkTXT, columns= ['Link'])
    LinkAdded = pd.read_csv (LinkAPath)
    LinkADF = pd.DataFrame(LinkAdded, columns= ['Link'])

    LinkList = LinkDF['Link'].values.tolist()
    LinkAList = LinkADF['Link'].values.tolist()

    if LiquiPage != "":
      if LiquiPage in LinkList:
        print(LiquiPage,": This Liquipedia page is already in queue and will be added when Database is updated")
      else:
        LinkList.append(LiquiPage)
  
    if (LiquiPage!="") and (LiquiPage in LinkAList):
      print(LiquiPage,": This page was already added previously, use Reload if you want to update it")
  
    DFLinkFinal = pd.DataFrame (LinkList, columns = ['Link'])
    DFLinkFinal.to_csv(LinkTPath, index = False)
    DFLinkAFinal = pd.DataFrame (LinkAList, columns = ['Link'])
    DFLinkAFinal.to_csv(LinkAPath, index = False)

  #removes the Liquipedia Link from LiquipediaAdded and adds it to Liquipedia.txt, so next time Database is updated, the Liquipedia page will be reloaded
  def ReloadLP():
    LiquiPage = entry2.get()
    FolderPath = entry1.get()
  
    if FolderPath == "":
      LinkTPath = StoredPath+os.sep+"liquipedia.txt"
      LinkAPath = StoredPath+os.sep+"liquipediaAdded.txt"
    else:
      LinkTPath = FolderPath+os.sep+"liquipedia.txt"
      LinkAPath = StoredPath+os.sep+"liquipediaAdded.txt"    
      UpdateStoredPath(FolderPath)     
  
    print("Opening ",LinkTPath)
    print("Opening ",LinkAPath)

    LinkTXT = pd.read_csv (LinkTPath)
    LinkDF = pd.DataFrame(LinkTXT, columns= ['Link'])
    LinkAdded = pd.read_csv (LinkAPath)
    LinkADF = pd.DataFrame(LinkAdded, columns= ['Link'])

    LinkList = LinkDF['Link'].values.tolist()
    LinkAList = LinkADF['Link'].values.tolist()

    if LiquiPage != "":
      if LiquiPage in LinkList:
        print("This Liquipedia page is already in queue and will be added when Database is updated")
      else:
        LinkList.append(LiquiPage)
  
    if (LiquiPage!="") and (LiquiPage in LinkAList):
      LinkAList.remove(LiquiPage)
  
    DFLinkFinal = pd.DataFrame (LinkList, columns = ['Link'])
    DFLinkFinal.to_csv(LinkTPath, index = False)
    DFLinkAFinal = pd.DataFrame (LinkAList, columns = ['Link'])
    DFLinkAFinal.to_csv(LinkAPath, index = False)


  #Skip a specific match, useful when the json file is corrupted
  def SkipMatch():
    SpecificMatch = int(entry3.get())

    DBPath = GetDBPath()     
  
    print("Opening ",DBPath)
  
    DatabaseDF = pd.read_excel (DBPath)
    DatabaseDF.loc[DatabaseDF.MatchID == SpecificMatch, "OpenDota"] = "skip"  
    DatabaseDF.to_excel(DBPath, index = False)

    print(SpecificMatch," will be skipped")

  #removes the done tag for a Specific Match, that way the next time Database is update the json file is extracted from OpenDota again
  def UndoneMatch():
    SpecificMatch = int(entry3.get())

    DBPath = GetDBPath()     
  
    print("Opening ",DBPath)
  
    DatabaseDF = pd.read_excel (DBPath)
    DatabaseDF.loc[DatabaseDF.MatchID == SpecificMatch, "OpenDota"] = ""
    DatabaseDF.to_excel(DBPath, index = False)

    print(SpecificMatch," will be downloaded again from OpenDota")

  ############################################################
  ######Scripts that run other scripts#######################

  #Runs OpenDotaHeroes script
  def RunODH():
    FolderPath = GetFolderPath() 
  
    print("Extracting Hero Data from Open Dota")
    odh.Run(FolderPath)

  #Runs the LiquipediaScrap script
  def RunLPScrap():
    FolderPath = GetFolderPath() 
  
    print("Extracting Matches from Liquipedia")

    ls.Run(FolderPath)

  #Runs the OpenDotaScrap script
  def RunODScrap():
    FolderPath = GetFolderPath()
  
    print("Extracting Match files from OpenDota")

    ods.Run(FolderPath)  

  #Runs the OpenDotaScrap script
  def RunJSScrap():
    FolderPath = GetFolderPath()
  
    print("Updating Database from Match files")

    js.Run(FolderPath)
  

  #######################################################
  #################GUI###################################

  canvas1 = tk.Canvas(root2, bg = bgc , width = 800, height = 600)
  canvas1.pack()

  title0 = tk.Label(root2, text='DOTA 2 FANTASY DATABASE')
  title0.config(font=('helvetica', 34, 'bold'), bg = bgc, fg = fgcTitle)
  canvas1.create_window(400, 50, window=title0)

  title1 = tk.Label(root2, text='Copy the folder path that contains the Database files:')
  title1.config(font=('helvetica', 20), bg = bgc, fg = fgc)
  canvas1.create_window(400, 100, window=title1)

  buttonSelect = tk.Button(root2, text='or Select Folder', command=SelectFolder, bg= bgcSelect, fg= fgcSelect, font=('helvetica', 16, 'bold'), activebackground=bgcSelectA, activeforeground=fgcSelectA)
  canvas1.create_window(600, 150, window=buttonSelect)

  entry1 = tk.Entry (root2, textvariable=FolderPath) 
  entry1.config(font=('helvetica', 20), bg = bgcEntry, fg = fgcEntry)
  canvas1.create_window(280, 150, width = 400, window=entry1)

  title2 = tk.Label(root2, text='Liquipedia page:')
  title2.config(font=('helvetica', 16), bg = bgc, fg = fgc)
  canvas1.create_window(140, 220, window=title2)

  entry2 = tk.Entry (root2, textvariable=LiquiPage) 
  entry2.config(font=('helvetica', 16), bg = bgcEntry, fg = fgcEntry)
  canvas1.create_window(160, 250, width = 250, window=entry2)

  title3 = tk.Label(root2, text='MatchID:')
  title3.config(font=('helvetica', 16), bg = bgc, fg = fgc)
  canvas1.create_window(520, 220, window=title3)

  entry3 = tk.Entry (root2, textvariable=SpecificMatch) 
  entry3.config(font=('helvetica', 16), bg = bgcEntry, fg = fgcEntry)
  canvas1.create_window(540, 250, width = 250, window=entry3)

  buttonQueueLP = tk.Button(root2, text='Queue', command=QueueLiquipediaPage, bg= bgcSelect, fg= fgcSelect, font=('helvetica', 14, 'bold'), activebackground=bgcSelectA, activeforeground=fgcSelectA)
  canvas1.create_window(80, 300, window=buttonQueueLP)

  buttonReloadLP = tk.Button(root2, text='Reload', command=ReloadLP, bg= bgcSelect, fg= fgcSelect, font=('helvetica', 14, 'bold'), activebackground=bgcSelectA, activeforeground=fgcSelectA)
  canvas1.create_window(200, 300, window=buttonReloadLP)

  buttonSkip = tk.Button(root2, text='Skip Match', command=SkipMatch, bg= bgcSelect, fg= fgcSelect, font=('helvetica', 14, 'bold'), activebackground=bgcSelectA, activeforeground=fgcSelectA)
  canvas1.create_window(450, 300, window=buttonSkip)

  buttonUndone = tk.Button(root2, text='Mark Undone', command=UndoneMatch, bg= bgcSelect, fg= fgcSelect, font=('helvetica', 14, 'bold'), activebackground=bgcSelectA, activeforeground=fgcSelectA)
  canvas1.create_window(630, 300, window=buttonUndone)

  buttonRunLP = tk.Button(root2, text='1- Extract Matches from Liquipedia', command=RunLPScrap, bg= bgcButton, fg= fgcButton, font=('helvetica', 14, 'bold'), activebackground=bgcButtonA, activeforeground=fgcButtonA)
  canvas1.create_window(200, 400, width = 350, window=buttonRunLP)

  buttonRunOD = tk.Button(root2, text='2- Extract files from OpenDota', command=RunODScrap, bg= bgcButton, fg= fgcButton, font=('helvetica', 14, 'bold'), activebackground=bgcButtonA, activeforeground=fgcButtonA)
  canvas1.create_window(200, 450, width = 350, window=buttonRunOD)

  buttonRunJS = tk.Button(root2, text='3- Update Database from files', command=RunJSScrap, bg= bgcButton, fg= fgcButton, font=('helvetica', 14, 'bold'), activebackground=bgcButtonA, activeforeground=fgcButtonA)
  canvas1.create_window(200, 500, width = 350, window=buttonRunJS)

  buttonRunODH = tk.Button(root2, text='Update Hero Stats file \n (only if there are new heroes)', command=RunODH, bg= bgcButton, fg= fgcButton, font=('helvetica', 10, 'bold'), activebackground=bgcButtonA, activeforeground=fgcButtonA)
  canvas1.create_window(200, 570, width = 250, window=buttonRunODH)  

  root.mainloop()
