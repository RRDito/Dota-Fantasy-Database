import tkinter as tk
import os
import pandas as pd
import matplotlib.pyplot as plt

def CheckPerformancesRun(root,fpath):
  root2= tk.Toplevel(root)

  LeagueVar = tk.StringVar()
  LeagueVar.set("Liquipedia League")
  TeamVar = tk.StringVar()
  TeamVar.set("Team")
  PlayerVar = tk.StringVar()
  PlayerVar.set("Player")
  MatchVar = tk.StringVar()
  MatchVar.set("Match")

  v0 = tk.StringVar()
  v1 = tk.StringVar()
  v2 = tk.StringVar()
  v3 = tk.StringVar()
  v4 = tk.StringVar()
  v5 = tk.StringVar()
  v6 = tk.StringVar()
  v7 = tk.StringVar()
  v8 = tk.StringVar()
  v9 = tk.StringVar()
  v10 = tk.StringVar()
  v11 = tk.StringVar()
  v12 = tk.StringVar()
  v13 = tk.StringVar()
  v14 = tk.StringVar()
  v15 = tk.StringVar()
  v16 = tk.StringVar()


  FolderPath = fpath
     
  DBPath = FolderPath+os.sep+"Database.xlsx"
  DatabaseDF = pd.read_excel (DBPath)

  LeagueList = DatabaseDF['Liquipedia'].values.tolist()
  LeagueList = list(set(LeagueList))
  LeagueList.append("Any League")

  PlayerA = tk.StringVar()
  PlayerA.set("")
  PlayerB = tk.StringVar()
  PlayerB.set("")

  #Colors Theme2
  bgc = '#211316'     #background color for windows
  fgc = '#B75743'      #font color for windows
  fgcTitle = '#C74228'      #font color for Main Title
  bgcEntry = '#612624'      #background color for entry field
  fgcEntry = '#C8533C'       #font color for entry field
  hbgc = '#C8533C' #highlight background color
  bgcEntryA = '#471C1A'      #background color for entry field when highlighted
  fgcEntryA = '#C8533C'       #font color for entry field when highlighted


  canvas1 = tk.Canvas(root2, bg = bgc , width = 1000, height = 800)
  canvas1.pack()

  title0 = tk.Label(root2, text='DOTA 2 FANTASY DATABASE')
  title0.config(font=('helvetica', 34, 'bold'), bg = bgc, fg = fgcTitle)
  canvas1.create_window(500, 50, window=title0)

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
    canvas1.create_window(150, 150, window=dropdown1)
    pass

  
  def ShowPlayers(event):
    columns = ["p1Name", "p2Name", "p3Name", "p4Name", "p5Name"] 
    PlayerList = []
    for column in columns:
        p = DatabaseDF.loc[DatabaseDF.RadiantTeamName == TeamVar.get(), column]
        PlayerList += p.values.tolist()
    columns = ["p6Name", "p7Name", "p8Name", "p9Name", "p10Name"]
    for column in columns:    
        p = DatabaseDF.loc[DatabaseDF.DireTeamName == TeamVar.get(), column]
        PlayerList += p.values.tolist()

    PlayerList = list(set(PlayerList))

    dropdown2 = tk.OptionMenu(root2, PlayerVar, *PlayerList, command=ShowMatches)
    dropdown2.config(font=('helvetica', 16), bg = bgcEntry, fg = fgcEntry, activebackground=bgcEntryA, activeforeground=fgcEntryA, highlightbackground=hbgc)
    canvas1.create_window(500, 150, window=dropdown2)
    pass
  

  def ShowMatches(event):
    columns = ["p1Name", "p2Name", "p3Name", "p4Name", "p5Name", "p6Name", "p7Name", "p8Name", "p9Name", "p10Name"]
    MatchList = []
    for column in columns:
        m = DatabaseDF.loc[((DatabaseDF[column] == PlayerVar.get())&(DatabaseDF.Liquipedia == LeagueVar.get())),"MatchID"]
        MatchList += m.values.tolist()

    MatchList = list(set(MatchList))

    dropdown3 = tk.OptionMenu(root2, MatchVar, *MatchList, command=ShowFantasy)
    dropdown3.config(font=('helvetica', 16), bg = bgcEntry, fg = fgcEntry, activebackground=bgcEntryA, activeforeground=fgcEntryA, highlightbackground=hbgc)
    canvas1.create_window(850, 150, window=dropdown3)
    pass
  
  
  def FindNumberAndName(mID):
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

    return name, number        
  
  
  def CalculateFantasy():
    
    mID = int(MatchVar.get())

    name, number = FindNumberAndName(mID)      
    
    VarName = name.values[0]
    v0.set(VarName)

    Col_Name = "p"+str(number)+"Won"
    IsWon = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    isWon = IsWon.values[0]
    
    if isWon == 1:
        MatchResult = "Win"
    else:
        MatchResult = "Loss"    

    Col_Name = "p"+str(number)+"Side"
    Side = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    side = Side.values[0]
    
    if side == "Radiant":
        sideVS = "Dire"
    elif side == "Dire":
        sideVS = "Radiant"    
    Col_Name = sideVS+"TeamName"
    TeamVS = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    teamVS = TeamVS.values[0]

    VarDetails = MatchResult+" against "+teamVS
    v1.set(VarDetails)

    TotalSeconds = DatabaseDF.loc[DatabaseDF.MatchID == mID, "Duration"]
    totalSeconds = TotalSeconds.values[0]    
    minutes = f'{int(totalSeconds//60):02d}'
    seconds = f'{int(totalSeconds%60):02d}'

    VarDuration = "Duration: "+str(minutes)+":"+str(seconds)
    v2.set(VarDuration)
    
    Col_Name = "p"+str(number)+"HeroName"
    Hero = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    
    VarHero = "Hero: "+ Hero.values[0]
    v3.set(VarHero)
    
    Col_Name = "p"+str(number)+"FantasyKills"
    FKills = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    
    VarKills = "Kills: "+ str(round(FKills.values[0],2))
    v4.set(VarKills)
    
    Col_Name = "p"+str(number)+"FantasyDeaths"
    FDeaths = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    
    VarDeaths = "Deaths: "+ str(round(FDeaths.values[0],2))
    v5.set(VarDeaths)
    
    Col_Name = "p"+str(number)+"FantasyGPM"
    Fgpm = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    
    VarGPM = "GPM: "+ str(round(Fgpm.values[0],2))
    v6.set(VarGPM)
    
    Col_Name = "p"+str(number)+"FantasyCreepScore"
    FCreepScore = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    
    VarCreepScore = "Creep Score: "+ str(round(FCreepScore.values[0],2))
    v7.set(VarCreepScore)    
    
    Col_Name = "p"+str(number)+"FantasyTowerDestroyed"
    FTowerKills = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    
    VarTowerKills = "Towers Destroyed: "+ str(round(FTowerKills.values[0],2))
    v8.set(VarTowerKills)
    
    Col_Name = "p"+str(number)+"FantasyRoshanKills"
    FRoshanKills = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    
    VarRoshanKills = "Roshans Killed: "+ str(round(FRoshanKills.values[0],2))
    v9.set(VarRoshanKills)
    
    Col_Name = "p"+str(number)+"FantasyTeamfight"
    FTeamfight = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    
    VarTeamfight = "Teamfight: "+ str(round(FTeamfight.values[0],2))
    v10.set(VarTeamfight)
    
    Col_Name = "p"+str(number)+"FantasyObsPlaced"
    FObsPlaced = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    
    VarObsPlaced = "Observers Placed: "+ str(round(FObsPlaced.values[0],2))
    v11.set(VarObsPlaced)
    
    Col_Name = "p"+str(number)+"FantasyCampsStacked"
    FCampsStacked = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    
    VarCampsStacked = "Camps Stacked: "+ str(round(FCampsStacked.values[0],2))
    v12.set(VarCampsStacked)
    
    Col_Name = "p"+str(number)+"FantasyRunes"
    FRunes = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    
    VarRunes = "Runes: "+ str(round(FRunes.values[0],2))
    v13.set(VarRunes)
    
    Col_Name = "p"+str(number)+"FantasyFirstBlood"
    FFirstBlood = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    
    VarFirstBlood = "First Blood: "+ str(round(FFirstBlood.values[0],2))
    v14.set(VarFirstBlood)
    
    Col_Name = "p"+str(number)+"FantasyStuns"
    FStun = DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_Name]
    
    VarStun = "Stuns: "+ str(round(FStun.values[0],2))
    v15.set(VarStun)
    
    FantasyTotal=FKills+FDeaths+Fgpm+FCreepScore+FTowerKills+FRoshanKills+FTeamfight+FObsPlaced+FCampsStacked+FRunes+FFirstBlood+FStun 
    
    VarFantasyTotal = "Fantasy Points: "+ str(round(FantasyTotal.values[0],2))
    v16.set(VarFantasyTotal)    
  
  def FantasyA():
    PlayerA.set(PlayerVar.get())

    CalculateFantasy()
    
    labelA0 = tk.Label(root2, text=v0.get())
    labelA0.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 230, width=400, window=labelA0)

    labelA1 = tk.Label(root2, text=v1.get())
    labelA1.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 260, width=400, window=labelA1)

    labelA2 = tk.Label(root2, text=v2.get())
    labelA2.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 290, width=400, window=labelA2)

    labelA3 = tk.Label(root2, text=v3.get())
    labelA3.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 320, width=400, window=labelA3)

    labelA4 = tk.Label(root2, text=v4.get())
    labelA4.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 350, width=400, window=labelA4)

    labelA5 = tk.Label(root2, text=v5.get())
    labelA5.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 380, width=400, window=labelA5)

    labelA6 = tk.Label(root2, text=v6.get())
    labelA6.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 410, width=400, window=labelA6)

    labelA7 = tk.Label(root2, text=v7.get())
    labelA7.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 440, width=400, window=labelA7)

    labelA8 = tk.Label(root2, text=v8.get())
    labelA8.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 470, width=400, window=labelA8)

    labelA9 = tk.Label(root2, text=v9.get())
    labelA9.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 500, width=400, window=labelA9)

    labelA10 = tk.Label(root2, text=v10.get())
    labelA10.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 530, width=400, window=labelA10)

    labelA11 = tk.Label(root2, text=v11.get())
    labelA11.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 560, width=400, window=labelA11)

    labelA12 = tk.Label(root2, text=v12.get())
    labelA12.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 590, width=400, window=labelA12)

    labelA13 = tk.Label(root2, text=v13.get())
    labelA13.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 620, width=400, window=labelA13)

    labelA14 = tk.Label(root2, text=v14.get())
    labelA14.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 650, width=400, window=labelA14)

    labelA15 = tk.Label(root2, text=v15.get())
    labelA15.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 680, width=400, window=labelA15)

    labelA16 = tk.Label(root2, text=v16.get())
    labelA16.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(250, 720, width=400, window=labelA16)
        

  def FantasyB():
    PlayerB.set(PlayerVar.get())
    
    CalculateFantasy()  
    
    labelB0 = tk.Label(root2, text=v0.get())
    labelB0.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 230, width=400, window=labelB0)

    labelB1 = tk.Label(root2, text=v1.get())
    labelB1.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 260, width=400, window=labelB1)

    labelB2 = tk.Label(root2, text=v2.get())
    labelB2.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 290, width=400, window=labelB2)

    labelB3 = tk.Label(root2, text=v3.get())
    labelB3.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 320, width=400, window=labelB3)

    labelB4 = tk.Label(root2, text=v4.get())
    labelB4.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 350, width=400, window=labelB4)

    labelB5 = tk.Label(root2, text=v5.get())
    labelB5.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 380, width=400, window=labelB5)

    labelB6 = tk.Label(root2, text=v6.get())
    labelB6.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 410, width=400, window=labelB6)

    labelB7 = tk.Label(root2, text=v7.get())
    labelB7.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 440, width=400, window=labelB7)

    labelB8 = tk.Label(root2, text=v8.get())
    labelB8.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 470, width=400, window=labelB8)

    labelB9 = tk.Label(root2, text=v9.get())
    labelB9.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 500, width=400, window=labelB9)

    labelB10 = tk.Label(root2, text=v10.get())
    labelB10.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 530, width=400, window=labelB10)

    labelB11 = tk.Label(root2, text=v11.get())
    labelB11.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 560, width=400, window=labelB11)

    labelB12 = tk.Label(root2, text=v12.get())
    labelB12.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 590, width=400, window=labelB12)

    labelB13 = tk.Label(root2, text=v13.get())
    labelB13.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 620, width=400, window=labelB13)

    labelB14 = tk.Label(root2, text=v14.get())
    labelB14.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 650, width=400, window=labelB14)

    labelB15 = tk.Label(root2, text=v15.get())
    labelB15.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 680, width=400, window=labelB15)

    labelB16 = tk.Label(root2, text=v16.get())
    labelB16.config(font=('helvetica', 14), bg = bgc, fg = fgc)
    canvas1.create_window(750, 720, width=400, window=labelB16) 

   
  
  #Function that creates the DataFrame that is going to be used for graphs
  def CreateGraphDF(A, d):
    matches = d.loc[(d["p1Name"]==A)|(d["p2Name"]==A)|(d["p3Name"]==A)|(d["p4Name"]==A)|(d["p5Name"]==A)|(d["p6Name"]==A)|(d["p7Name"]==A)|(d["p8Name"]==A)|(d["p9Name"]==A)|(d["p10Name"]==A), "MatchID"]

    df = pd.DataFrame(columns=["time", "points", "won"])

    #Find the number corresponding to that player for that match in Database     
    for m in matches.values.tolist():
        i = 1
        while i < 11:
            ColPlayerName = "p"+str(i)+"Name"
            name = DatabaseDF.loc[DatabaseDF.MatchID == m, ColPlayerName]
            if name.values[0] == A:
                number = i
                break
            else:
                i = i+1

        time = DatabaseDF.loc[DatabaseDF.MatchID == m, "Duration"]
        time = time.values[0]        
        ColPlayerFantasy = "p"+str(number)+"FantasyTotal"
        points = DatabaseDF.loc[DatabaseDF.MatchID == m, ColPlayerFantasy]
        points = points.values[0]

        Col_Name = "p"+str(number)+"Won"
        IsWon = DatabaseDF.loc[DatabaseDF.MatchID == m, Col_Name]
        isWon = IsWon.values[0]    
        # if isWon == 1: MatchResult = "Win" else: MatchResult = "Loss"

        df = df.append({"time": time, "points": points, "won": isWon}, ignore_index=True)

    return df    


  #Function that draws the graph 
  def ShowGraph():
    A = PlayerA.get()    
    B = PlayerB.get()    
    d = DatabaseDF

    #Dataframe for PlayerA and PlayerB
    dfA = CreateGraphDF(A, d)      
    dfB = CreateGraphDF(B, d)    
    
    # Sort the Dataframes
    dfA = dfA.sort_values("time")
    dfB = dfB.sort_values("time")

    #create sub-dataframes for win lose situation
    dfAwin = dfA[dfA["won"] == 1]
    dfAlose = dfA[dfA["won"] == 0]
    dfBwin = dfB[dfB["won"] == 1]
    dfBlose = dfB[dfB["won"] == 0]

    # Create a figure and two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Calculate the rolling mean with a window of 3
    dfAwin['points_rolling_mean'] = dfAwin['points'].rolling(window=5).mean()
    dfAlose['points_rolling_mean'] = dfAlose['points'].rolling(window=5).mean()
    dfBwin['points_rolling_mean'] = dfBwin['points'].rolling(window=5).mean()
    dfBlose['points_rolling_mean'] = dfBlose['points'].rolling(window=5).mean()
    
    # Plot the first line on the left subplot
    ax1.plot(dfAwin["time"], dfAwin["points_rolling_mean"], label=A)
    # ax1.scatter(dfAwin["time"], dfAwin["points"], label=A)
    ax1.plot(dfBwin["time"], dfBwin["points_rolling_mean"], label=B)
    # ax1.scatter(dfBwin["time"], dfBwin["points"], label=B)

    ax1.set_xlabel("Match Length (s)")
    ax1.set_ylabel("Fantasy Points")
    ax1.set_title("WINS")
    ax1.legend()

    # Plot the second line on the right subplot
    ax2.plot(dfAlose["time"], dfAlose["points_rolling_mean"], label=A)
    # ax2.scatter(dfAlose["time"], dfAlose["points"], label=A)
    ax2.plot(dfBlose["time"], dfBlose["points_rolling_mean"], label=B)
    # ax2.scatter(dfBlose["time"], dfBlose["points"], label=B)

    ax2.set_xlabel("Match Length (s)")
    ax2.set_ylabel("Fantasy Points")
    ax2.set_title("LOSES")
    ax2.legend()

    # Adjust spacing between the subplots
    fig.tight_layout()

    # Show the figure
    plt.show()


  
  def ShowFantasy(event):
    
    buttonA = tk.Button(root2, text='A', command=FantasyA)
    buttonA.config(bg= bgcEntry, fg= fgcEntry, font=('helvetica', 18, 'bold'), activebackground=bgcEntryA, activeforeground=fgcEntryA)
    canvas1.create_window(250, 200, window=buttonA)

    buttonB = tk.Button(root2, text='B', command=FantasyB)
    buttonB.config(bg= bgcEntry, fg= fgcEntry, font=('helvetica', 18, 'bold'), activebackground=bgcEntryA, activeforeground=fgcEntryA)
    canvas1.create_window(750, 200, window=buttonB)

    buttonB = tk.Button(root2, text='Graph', command=ShowGraph)
    buttonB.config(bg= bgcEntry, fg= fgcEntry, font=('helvetica', 18, 'bold'), activebackground=bgcEntryA, activeforeground=fgcEntryA)
    canvas1.create_window(500, 750, window=buttonB)
    pass  
  
  
  dropdown0 = tk.OptionMenu(root2, LeagueVar, *LeagueList, command=ShowTeams)
  dropdown0.config(font=('helvetica', 16), bg = bgcEntry, fg = fgcEntry, activebackground=bgcEntryA, activeforeground=fgcEntryA, highlightbackground=hbgc)
  canvas1.create_window(500, 100, window=dropdown0)

  

  