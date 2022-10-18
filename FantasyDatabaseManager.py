import os
import tkinter as tk
from tkinter.filedialog import askdirectory
import jsonScrap as js
import LiquipediaScrap as ls
import OpenDotaScrap as ods
import OpenDotaHeroes as odh
import pandas as pd

root= tk.Tk()
FolderPath = tk.StringVar()
LiquiPage = tk.StringVar()
SpecificMatch = tk.StringVar()

defaultPath = os.getcwd()

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


canvas1 = tk.Canvas(root, bg = bgc , width = 800, height = 600)
canvas1.pack()

def SelectFolder():
  FolderPath.set( askdirectory(title='Select Folder') )  

version = tk.Label(root, text='version 1.0')
version.config(font=('helvetica', 8), bg = bgc, fg = fgcTitle)
canvas1.create_window(40, 15, window=version)

title0 = tk.Label(root, text='DOTA 2 FANTASY DATABASE')
title0.config(font=('helvetica', 34, 'bold'), bg = bgc, fg = fgcTitle)
canvas1.create_window(400, 50, window=title0)

title1 = tk.Label(root, text='Copy the folder path that contains the Database files:')
title1.config(font=('helvetica', 20), bg = bgc, fg = fgc)
canvas1.create_window(400, 100, window=title1)

entry1 = tk.Entry (root, textvariable=FolderPath) 
entry1.config(font=('helvetica', 20), bg = bgcEntry, fg = fgcEntry)
canvas1.create_window(280, 150, width = 400, window=entry1)

buttonSelect = tk.Button(text='or Select Folder', command=SelectFolder, bg= bgcSelect, fg= fgcSelect, font=('helvetica', 16, 'bold'), activebackground=bgcSelectA, activeforeground=fgcSelectA)
canvas1.create_window(600, 150, window=buttonSelect)

title2 = tk.Label(root, text='Liquipedia page:')
title2.config(font=('helvetica', 16), bg = bgc, fg = fgc)
canvas1.create_window(140, 220, window=title2)

entry2 = tk.Entry (root, textvariable=LiquiPage) 
entry2.config(font=('helvetica', 16), bg = bgcEntry, fg = fgcEntry)
canvas1.create_window(160, 250, width = 250, window=entry2)

title3 = tk.Label(root, text='MatchID:')
title3.config(font=('helvetica', 16), bg = bgc, fg = fgc)
canvas1.create_window(520, 220, window=title3)

entry3 = tk.Entry (root, textvariable=SpecificMatch) 
entry3.config(font=('helvetica', 16), bg = bgcEntry, fg = fgcEntry)
canvas1.create_window(540, 250, width = 250, window=entry3)

def UpdateStoredPath(p):
  SPFilePath = defaultPath+os.sep+"StoredPath.txt"
  SPFile = open(SPFilePath,'w')
  SPFile.write(p)
  SPFile.close()
  print("Stored Path:",p)

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
  FolderPath = entry1.get()  
  
  if FolderPath == "":
    DBPath = StoredPath+os.sep+"Database.xlsx"
  else:
    DBPath = FolderPath+os.sep+"Database.xlsx"    
    UpdateStoredPath(FolderPath)     
  
  print("Opening ",DBPath)
  
  DatabaseDF = pd.read_excel (DBPath)
  DatabaseDF.loc[DatabaseDF.MatchID == SpecificMatch, "OpenDota"] = "skip"  
  DatabaseDF.to_excel(DBPath, index = False)

#removes the done tag for a Specific Match, that way the next time Database is update the json file is extracted from OpenDota again
def UndoneMatch():
  SpecificMatch = int(entry3.get())
  FolderPath = entry1.get()  
  
  if FolderPath == "":
    DBPath = StoredPath+os.sep+"Database.xlsx"
  else:
    DBPath = FolderPath+os.sep+"Database.xlsx"    
    UpdateStoredPath(FolderPath)     
  
  print("Opening ",DBPath)
  
  DatabaseDF = pd.read_excel (DBPath)
  DatabaseDF.loc[DatabaseDF.MatchID == SpecificMatch, "OpenDota"] = ""
  DatabaseDF.to_excel(DBPath, index = False)

#Runs OpenDotaHeroes script
def RunODH():
  FolderPath = entry1.get()
  
  if FolderPath != "":
    #if there is a path specified the path is saved into Stored Path
    UpdateStoredPath(FolderPath)  
  else:
    #if no path was specified take it from Stored Path
    FolderPath = StoredPath 
  
  print("Extracting Hero Data from Open Dota")
  odh.Run(FolderPath)

#Runs the LiquipediaScrap script
def RunLPScrap():
  FolderPath = entry1.get()
  
  if FolderPath != "":
    #if there is a path specified the path is saved into Stored Path
    UpdateStoredPath(FolderPath)  
  else:
    #if no path was specified take it from Stored Path
    FolderPath = StoredPath 
  
  print("Extracting Matches from Liquipedia")

  ls.Run(FolderPath)

#Runs the OpenDotaScrap script
def RunODScrap():
  FolderPath = entry1.get()
  
  if FolderPath != "":
    #if there is a path specified the path is saved into Stored Path
    UpdateStoredPath(FolderPath)  
  else:
    #if no path was specified take it from Stored Path
    FolderPath = StoredPath 
  
  print("Extracting Match files from OpenDota")

  ods.Run(FolderPath)  

#Runs the OpenDotaScrap script
def RunJSScrap():
  FolderPath = entry1.get()
  
  if FolderPath != "":
    #if there is a path specified the path is saved into Stored Path
    UpdateStoredPath(FolderPath)  
  else:
    #if no path was specified take it from Stored Path
    FolderPath = StoredPath 
  
  print("Updating Database from Match files")

  js.Run(FolderPath)  


def FantasyRun():
  root2= tk.Toplevel(root)

  LeagueVar = tk.StringVar()
  LeagueVar.set("Liquipedia League")
  TeamVar = tk.StringVar()
  TeamVar.set("Team")
  PlayerVar = tk.StringVar()
  PlayerVar.set("Player")
  MatchVar = tk.StringVar()
  MatchVar.set("Match")

  FolderPath = entry1.get()
  
  if FolderPath != "":
    #if there is a path specified the path is saved into Stored Path
    UpdateStoredPath(FolderPath)  
  else:
    #if no path was specified take it from Stored Path
    FolderPath = StoredPath
     
  DBPath = FolderPath+os.sep+"Database.xlsx"
  DatabaseDF = pd.read_excel (DBPath)

  LeagueList = DatabaseDF['Liquipedia'].values.tolist()
  LeagueList = list(set(LeagueList))
  LeagueList.append("Any League")

  #Colors Theme2
  bgc = '#211316'     #background color for windows
  fgc = '#B75743'      #font color for windows
  fgcTitle = '#C74228'      #font color for Main Title
  bgcEntry = '#612624'      #background color for entry field
  fgcEntry = '#C8533C'       #font color for entry field
  hbgc = '#C8533C' #highlight background color
  bgcEntryA = '#471C1A'      #background color for entry field when highlighted
  fgcEntryA = '#C8533C'       #font color for entry field when highlighted


  canvas1 = tk.Canvas(root2, bg = bgc , width = 800, height = 600)
  canvas1.pack()

  title0 = tk.Label(root2, text='DOTA 2 FANTASY DATABASE')
  title0.config(font=('helvetica', 34, 'bold'), bg = bgc, fg = fgcTitle)
  canvas1.create_window(400, 50, window=title0)

  def ShowTeams(event):
    #print(LeagueVar.get())

    if LeagueVar.get()=="Any League":
        TeamListR = DatabaseDF['RadiantTeamName'].values.tolist()
        TeamListD = DatabaseDF['DireTeamName'].values.tolist()
        for a in TeamListD:
            TeamListR.append(a)
        TeamList = list(set(TeamListR))
    else:
        teamR = DatabaseDF.loc[DatabaseDF.Liquipedia == LeagueVar.get(), "RadiantTeamName"]
        TeamList = teamR.values.tolist()
        teamD = DatabaseDF.loc[DatabaseDF.Liquipedia == LeagueVar.get(), "DireTeamName"]
        td = teamD.values.tolist()
        for td2 in td:
            TeamList.append(td2)

    TeamList = list(set(TeamList))   

    dropdown1 = tk.OptionMenu(root2, TeamVar, *TeamList, command=ShowPlayers)
    dropdown1.config(font=('helvetica', 16), bg = bgcEntry, fg = fgcEntry, activebackground=bgcEntryA, activeforeground=fgcEntryA, highlightbackground=hbgc)
    canvas1.create_window(190, 150, window=dropdown1)
    pass


  def ShowPlayers(event):
    #print(TeamVar.get())

    p = DatabaseDF.loc[DatabaseDF.RadiantTeamName == TeamVar.get(), "p1Name"]
    PlayerList = p.values.tolist()    
    p = DatabaseDF.loc[DatabaseDF.RadiantTeamName == TeamVar.get(), "p2Name"]
    p2 = p.values.tolist()
    for p3 in p2:
        PlayerList.append(p3)
    p = DatabaseDF.loc[DatabaseDF.RadiantTeamName == TeamVar.get(), "p3Name"]
    p2 = p.values.tolist()
    for p3 in p2:
        PlayerList.append(p3)
    p = DatabaseDF.loc[DatabaseDF.RadiantTeamName == TeamVar.get(), "p4Name"]
    p2 = p.values.tolist()
    for p3 in p2:
        PlayerList.append(p3)
    p = DatabaseDF.loc[DatabaseDF.RadiantTeamName == TeamVar.get(), "p5Name"]
    p2 = p.values.tolist()
    for p3 in p2:
        PlayerList.append(p3)
    p = DatabaseDF.loc[DatabaseDF.DireTeamName == TeamVar.get(), "p6Name"]
    p2 = p.values.tolist()
    for p3 in p2:
        PlayerList.append(p3)
    p = DatabaseDF.loc[DatabaseDF.DireTeamName == TeamVar.get(), "p7Name"]
    p2 = p.values.tolist()
    for p3 in p2:
        PlayerList.append(p3)
    p = DatabaseDF.loc[DatabaseDF.DireTeamName == TeamVar.get(), "p8Name"]
    p2 = p.values.tolist()
    for p3 in p2:
        PlayerList.append(p3)
    p = DatabaseDF.loc[DatabaseDF.DireTeamName == TeamVar.get(), "p9Name"]
    p2 = p.values.tolist()
    for p3 in p2:
        PlayerList.append(p3)
    p = DatabaseDF.loc[DatabaseDF.DireTeamName == TeamVar.get(), "p10Name"]
    p2 = p.values.tolist()
    for p3 in p2:
        PlayerList.append(p3)
    
    PlayerList = list(set(PlayerList))

    dropdown2 = tk.OptionMenu(root2, PlayerVar, *PlayerList, command=ShowMatches)
    dropdown2.config(font=('helvetica', 16), bg = bgcEntry, fg = fgcEntry, activebackground=bgcEntryA, activeforeground=fgcEntryA, highlightbackground=hbgc)
    canvas1.create_window(490, 150, window=dropdown2)
    pass

  def ShowMatches(event):
    #print(PlayerVar.get())

    m = DatabaseDF.loc[DatabaseDF.p1Name == PlayerVar.get(), "MatchID"]
    MatchList = m.values.tolist()    
    m = DatabaseDF.loc[DatabaseDF.p2Name == PlayerVar.get(), "MatchID"]
    m2 = m.values.tolist()
    for m3 in m2:
        MatchList.append(m3)
    m = DatabaseDF.loc[DatabaseDF.p3Name == PlayerVar.get(), "MatchID"]
    m2 = m.values.tolist()
    for m3 in m2:
        MatchList.append(m3)
    m = DatabaseDF.loc[DatabaseDF.p4Name == PlayerVar.get(), "MatchID"]
    m2 = m.values.tolist()
    for m3 in m2:
        MatchList.append(m3)
    m = DatabaseDF.loc[DatabaseDF.p5Name == PlayerVar.get(), "MatchID"]
    m2 = m.values.tolist()
    for m3 in m2:
        MatchList.append(m3)
    m = DatabaseDF.loc[DatabaseDF.p6Name == PlayerVar.get(), "MatchID"]
    m2 = m.values.tolist()
    for m3 in m2:
        MatchList.append(m3)
    m = DatabaseDF.loc[DatabaseDF.p7Name == PlayerVar.get(), "MatchID"]
    m2 = m.values.tolist()
    for m3 in m2:
        MatchList.append(m3)
    m = DatabaseDF.loc[DatabaseDF.p8Name == PlayerVar.get(), "MatchID"]
    m2 = m.values.tolist()
    for m3 in m2:
        MatchList.append(m3)
    m = DatabaseDF.loc[DatabaseDF.p9Name == PlayerVar.get(), "MatchID"]
    m2 = m.values.tolist()
    for m3 in m2:
        MatchList.append(m3)
    m = DatabaseDF.loc[DatabaseDF.p10Name == PlayerVar.get(), "MatchID"]
    m2 = m.values.tolist()
    for m3 in m2:
        MatchList.append(m3)
    
    MatchList = list(set(MatchList))

    dropdown3 = tk.OptionMenu(root2, MatchVar, *MatchList, command=ShowFantasy)
    dropdown3.config(font=('helvetica', 16), bg = bgcEntry, fg = fgcEntry, activebackground=bgcEntryA, activeforeground=fgcEntryA, highlightbackground=hbgc)
    canvas1.create_window(100, 200, window=dropdown3)
    pass

  def ShowFantasy(event):
    #print(MatchVar.get())
    mID = int(MatchVar.get())
    
    #Find the number corresponding to that player for that match in Database
    i = 1
    while i < 11:
        ColPlayerName = "p"+str(i)+"Name"
        name = DatabaseDF.loc[DatabaseDF.MatchID == mID, ColPlayerName]
        if name.values[0] == PlayerVar.get():
            number = i
            break
        else:
            i = i+1   
    #print(number)

    TotalSeconds = DatabaseDF.loc[DatabaseDF.MatchID == mID, "Duration"]
    totalSeconds = TotalSeconds.values[0]    
    minutes = f'{int(totalSeconds//60):02d}'
    seconds = f'{int(totalSeconds%60):02d}'
    duration = "Duration: "+str(minutes)+":"+str(seconds)
    #print(duration)
    

    Col_Name = "p"+str(number)+"Won"
    IsWon = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    isWon = IsWon.values[0]
    #print(isWon)
    if isWon == 1:
        MatchResult = "Win"
    else:
        MatchResult = "Loss"    

    Col_Name = "p"+str(number)+"Side"
    Side = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    side = Side.values[0]
    #print(side)
    if side == "Radiant":
        sideVS = "Dire"
    elif side == "Dire":
        sideVS = "Radiant"    
    Col_Name = sideVS+"TeamName"
    TeamVS = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    teamVS = TeamVS.values[0]

    MatchDetails = MatchResult+" against "+teamVS

    label0 = tk.Label(root2, text=MatchDetails)
    label0.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 300, width=400, window=label0)

    label0A = tk.Label(root2, text=duration)
    label0A.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 330, width=400, window=label0A)

    Col_Name = "p"+str(number)+"HeroName"
    Hero = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    hero = "Hero: "+ Hero.values[0]
    label1 = tk.Label(root2, text=hero)
    label1.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 360, width=400, window=label1)

    Col_Name = "p"+str(number)+"FantasyKills"
    FKills = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    fKills = "Kills: "+ str(round(FKills.values[0],2))
    label2 = tk.Label(root2, text=fKills)
    label2.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(600, 200, width=350, window=label2)

    Col_Name = "p"+str(number)+"FantasyDeaths"
    FDeaths = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    fDeaths = "Deaths: "+ str(round(FDeaths.values[0],2))
    label3 = tk.Label(root2, text=fDeaths)
    label3.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(600, 230, width=350, window=label3)

    Col_Name = "p"+str(number)+"FantasyGPM"
    Fgpm = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    fgpm = "GPM: "+ str(round(Fgpm.values[0],2))
    label4 = tk.Label(root2, text=fgpm)
    label4.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(600, 260, width=350, window=label4)

    Col_Name = "p"+str(number)+"FantasyCreepScore"
    FCreepScore = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    fCreepScore = "Creep Score: "+ str(round(FCreepScore.values[0],2))
    label5 = tk.Label(root2, text=fCreepScore)
    label5.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(600, 290, width=350, window=label5)

    Col_Name = "p"+str(number)+"FantasyTowerDestroyed"
    FTowerKills = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    fTowerKills = "Towers Destroyed: "+ str(round(FTowerKills.values[0],2))
    label6 = tk.Label(root2, text=fTowerKills)
    label6.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(600, 320, width=350, window=label6)

    Col_Name = "p"+str(number)+"FantasyRoshanKills"
    FRoshanKills = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    fRoshanKills = "Roshans Killed: "+ str(round(FRoshanKills.values[0],2))
    label7 = tk.Label(root2, text=fRoshanKills)
    label7.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(600, 350, width=350, window=label7)

    Col_Name = "p"+str(number)+"FantasyTeamfight"
    FTeamfight = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    fTeamfight = "Teamfight: "+ str(round(FTeamfight.values[0],2))
    label8 = tk.Label(root2, text=fTeamfight)
    label8.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(600, 380, width=350, window=label8)

    Col_Name = "p"+str(number)+"FantasyObsPlaced"
    FObsPlaced = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    fObsPlaced = "Observers Placed: "+ str(round(FObsPlaced.values[0],2))
    label9 = tk.Label(root2, text=fObsPlaced)
    label9.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(600, 410, width=350, window=label9)

    Col_Name = "p"+str(number)+"FantasyCampsStacked"
    FCampsStacked = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    fCampsStacked = "Camps Stacked: "+ str(round(FCampsStacked.values[0],2))
    label10 = tk.Label(root2, text=fCampsStacked)
    label10.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(600, 440, width=350, window=label10)

    Col_Name = "p"+str(number)+"FantasyRunes"
    FRunes = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    fRunes = "Runes: "+ str(round(FRunes.values[0],2))
    label11 = tk.Label(root2, text=fRunes)
    label11.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(600, 470, width=350, window=label11)

    Col_Name = "p"+str(number)+"FantasyFirstBlood"
    FFirstBlood = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    fFirstBlood = "First Blood: "+ str(round(FFirstBlood.values[0],2))
    label12 = tk.Label(root2, text=fFirstBlood)
    label12.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(600, 500, width=350, window=label12)

    Col_Name = "p"+str(number)+"FantasyStuns"
    FStun = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    fStun = "Stuns: "+ str(round(FStun.values[0],2))
    label13 = tk.Label(root2, text=fStun)
    label13.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(600, 530, width=350, window=label13)

    FantasyTotal=FKills+FDeaths+Fgpm+FCreepScore+FTowerKills+FRoshanKills+FTeamfight+FObsPlaced+FCampsStacked+FRunes+FFirstBlood+FStun 
    fTotal = "Fantasy Points: "+ str(round(FantasyTotal.values[0],2))
    label14 = tk.Label(root2, text=fTotal)
    label14.config(font=('helvetica', 16), bg = bgc, fg = fgcTitle)
    canvas1.create_window(600, 570, width=350, window=label14)
    
    pass

  dropdown0 = tk.OptionMenu(root2, LeagueVar, *LeagueList, command=ShowTeams)
  dropdown0.config(font=('helvetica', 16), bg = bgcEntry, fg = fgcEntry, activebackground=bgcEntryA, activeforeground=fgcEntryA, highlightbackground=hbgc)
  canvas1.create_window(400, 100, window=dropdown0)

buttonQueueLP = tk.Button(text='Queue', command=QueueLiquipediaPage, bg= bgcSelect, fg= fgcSelect, font=('helvetica', 14, 'bold'), activebackground=bgcSelectA, activeforeground=fgcSelectA)
canvas1.create_window(80, 300, window=buttonQueueLP)

buttonReloadLP = tk.Button(text='Reload', command=ReloadLP, bg= bgcSelect, fg= fgcSelect, font=('helvetica', 14, 'bold'), activebackground=bgcSelectA, activeforeground=fgcSelectA)
canvas1.create_window(200, 300, window=buttonReloadLP)

buttonSkip = tk.Button(text='Skip Match', command=SkipMatch, bg= bgcSelect, fg= fgcSelect, font=('helvetica', 14, 'bold'), activebackground=bgcSelectA, activeforeground=fgcSelectA)
canvas1.create_window(450, 300, window=buttonSkip)

buttonUndone = tk.Button(text='Mark Undone', command=UndoneMatch, bg= bgcSelect, fg= fgcSelect, font=('helvetica', 14, 'bold'), activebackground=bgcSelectA, activeforeground=fgcSelectA)
canvas1.create_window(630, 300, window=buttonUndone)


buttonRunLP = tk.Button(text='1- Extract Matches from Liquipedia', command=RunLPScrap, bg= bgcButton, fg= fgcButton, font=('helvetica', 14, 'bold'), activebackground=bgcButtonA, activeforeground=fgcButtonA)
canvas1.create_window(200, 400, width = 350, window=buttonRunLP)

buttonRunOD = tk.Button(text='2- Extract files from OpenDota', command=RunODScrap, bg= bgcButton, fg= fgcButton, font=('helvetica', 14, 'bold'), activebackground=bgcButtonA, activeforeground=fgcButtonA)
canvas1.create_window(200, 450, width = 350, window=buttonRunOD)

buttonRunJS = tk.Button(text='3- Update Database from files', command=RunJSScrap, bg= bgcButton, fg= fgcButton, font=('helvetica', 14, 'bold'), activebackground=bgcButtonA, activeforeground=fgcButtonA)
canvas1.create_window(200, 500, width = 350, window=buttonRunJS)

buttonRunODH = tk.Button(text='Update Hero Stats file \n (only if there are new heroes)', command=RunODH, bg= bgcButton, fg= fgcButton, font=('helvetica', 10, 'bold'), activebackground=bgcButtonA, activeforeground=fgcButtonA)
canvas1.create_window(200, 570, width = 250, window=buttonRunODH)

buttonFantasy = tk.Button(text='Check Fantasy', command=FantasyRun, bg= fgcButton, fg= bgcButton, font=('helvetica', 18, 'bold'), activebackground=fgcButtonA, activeforeground=bgcButtonA)
canvas1.create_window(600, 450, window=buttonFantasy)

root.mainloop()
