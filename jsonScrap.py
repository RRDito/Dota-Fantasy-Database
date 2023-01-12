import json
import time
import os
import pandas as pd

#this script extracts information relevant to Fantasy Points calculation and adds them to the Database

#path is assigned in Database Manager
# path = #assign this variable if you want to use this script by itself
def Run(path):

 path1 = path+os.sep+"MatchData"

 #this file has the stats of heroes, is needed to convert hero_id into hero names
 HeroStatsPath = path+os.sep+"HeroStats.json"
 HeroStatsFile = open(HeroStatsPath)
 heroStats = json.load(HeroStatsFile)
 HeroStatsFile.close()
 DBPath = path+os.sep+"Database.xlsx"
 DBPath_Old = path+os.sep+"Database_Old.xlsx"

 DatabaseDF = pd.read_excel (DBPath)
 DatabaseDF.to_excel(DBPath_Old, index = False)

 for f in os.listdir(path1):
    file = open(path1+os.sep+f)
    data = json.load(file)
    file.close()

    if "error" in data.keys():
        continue

    mID = data["match_id"]
    print(mID)

    IsDoneL = DatabaseDF.loc[DatabaseDF.MatchID == mID, "OpenDota"]
    IsDone = IsDoneL.iat[0]
    if IsDone == "skip":
        continue

    Duration = data["duration"]
    DatabaseDF.loc[DatabaseDF.MatchID == mID, "Duration"] = Duration
    
    Patch = data["patch"]
    DatabaseDF.loc[DatabaseDF.MatchID == mID, "Patch"] = Patch

    if data["radiant_win"] == False:
        DatabaseDF.loc[DatabaseDF.MatchID == mID, "Winner"] = "Dire"
    else:
         DatabaseDF.loc[DatabaseDF.MatchID == mID, "Winner"] = "Radiant"

    radiant = data["radiant_team"]
    DatabaseDF.loc[DatabaseDF.MatchID == mID, "RadiantTeamID"] = radiant["team_id"] 
    DatabaseDF.loc[DatabaseDF.MatchID == mID, "RadiantTeamName"] = radiant["name"]
    
    DatabaseDF.loc[DatabaseDF.MatchID == mID, "RadiantScore"] = data["radiant_score"]     

    dire = data["dire_team"]
    DatabaseDF.loc[DatabaseDF.MatchID == mID, "DireTeamID"] = dire["team_id"] 
    DatabaseDF.loc[DatabaseDF.MatchID == mID, "DireTeamName"] = dire["name"]

    DatabaseDF.loc[DatabaseDF.MatchID == mID, "DireScore"] = data["dire_score"]   

    player = data["players"]    
    FBtime = data["first_blood_time"] #this may be inexact       

    i=0

    for p in player:
        playerData = player[i]
        i=i+1

        Col_pSide = "p"+str(i)+"Side"
        if playerData["isRadiant"]== True:
            DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pSide] = "Radiant"
            TotalScore = data["radiant_score"]
        else:
            DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pSide] = "Dire"
            TotalScore = data["dire_score"]

        Col_pID = "p"+str(i)+"ID"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pID] = playerData["account_id"]
        Col_pName = "p"+str(i)+"Name"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pName] = playerData["name"]
        
        Col_pHero = "p"+str(i)+"Hero"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pHero] = playerData["hero_id"]
        Col_pHeroName = "p"+str(i)+"HeroName"
        
        for heroData in heroStats:
            if heroData["id"] == playerData["hero_id"]:
                DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pHeroName] = heroData["localized_name"]
                break

        Col_pKills = "p"+str(i)+"Kills"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pKills] = playerData["kills"]
        Col_pFantasyKills = "p"+str(i)+"FantasyKills"
        FantasyKills = 0.3*playerData["kills"]
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFantasyKills] = FantasyKills

        Col_pDeaths = "p"+str(i)+"Deaths"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pDeaths] = playerData["deaths"]
        Col_pFantasyDeaths = "p"+str(i)+"FantasyDeaths"
        FantasyDeaths = 3 - 0.3*playerData["deaths"]
        if FantasyDeaths < 0:
            FantasyDeaths = 0
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFantasyDeaths] = FantasyDeaths

        Col_pGPM = "p"+str(i)+"GPM"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pGPM] = playerData["gold_per_min"]
        Col_pFantasyGPM = "p"+str(i)+"FantasyGPM"
        FantasyGPM = 0.002 * playerData["gold_per_min"]
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFantasyGPM] = FantasyGPM

        Col_pLH = "p"+str(i)+"LastHits"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pLH] = playerData["last_hits"]
        Col_pDenies = "p"+str(i)+"Denies"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pDenies] = playerData["denies"]
        Col_pFantasyCS = "p"+str(i)+"FantasyCreepScore"
        FantasyCS = 0.003 * (playerData["last_hits"]+playerData["denies"])
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFantasyCS] = FantasyCS

        Col_pTowerKills = "p"+str(i)+"TowerKills"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pTowerKills] = playerData["tower_kills"]
        Col_pFantasyTowerDestroyed = "p"+str(i)+"FantasyTowerDestroyed"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFantasyTowerDestroyed] = playerData["tower_kills"]

        Col_pRoshanKills = "p"+str(i)+"RoshanKills"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pRoshanKills] = playerData["roshan_kills"]
        Col_pFantasyRoshanKills = "p"+str(i)+"FantasyRoshanKills"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFantasyRoshanKills] = playerData["roshan_kills"]

        Col_pAssists = "p"+str(i)+"Assists"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pAssists] = playerData["assists"]
        Col_pFantasyTeamfight = "p"+str(i)+"FantasyTeamfight"        
        Teamfight = 3*(playerData["kills"]+playerData["assists"])/(TotalScore)
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFantasyTeamfight] = Teamfight

        Col_pObsPlaced = "p"+str(i)+"ObsPlaced"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pObsPlaced] = playerData["obs_placed"]
        Col_pFantasyObsPlaced = "p"+str(i)+"FantasyObsPlaced"
        FantasyObsPlaced = 0.5*playerData["obs_placed"]
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFantasyObsPlaced] = FantasyObsPlaced

        Col_pCampsStacked = "p"+str(i)+"CampsStacked"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pCampsStacked] = playerData["camps_stacked"]
        Col_pFantasyCampsStacked = "p"+str(i)+"FantasyCampsStacked"
        FantasyCampsStacked = 0.5*playerData["camps_stacked"]
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFantasyCampsStacked] = FantasyCampsStacked

        Col_pRunes = "p"+str(i)+"Runes"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pRunes] = playerData["rune_pickups"]
        Col_pFantasyRunes = "p"+str(i)+"FantasyRunes"
        FantasyRunes = 0.5*playerData["rune_pickups"]
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFantasyRunes] = FantasyRunes

        Col_pFirstBlood = "p"+str(i)+"FirstBlood"
        kill_log = playerData["kills_log"]           
        if len(kill_log) > 0:            
            firstkill= kill_log[0]
        else:
            firstkill= ""
        if firstkill != "":
            if firstkill['time'] == FBtime:  
                DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFirstBlood] = 1
                FantasyFirstBlood = 4
            else:
                DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFirstBlood] = 0
                FantasyFirstBlood = 0
        else:
            DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFirstBlood] = 0
        Col_pFantasyFirstBlood = "p"+str(i)+"FantasyFirstBlood"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFantasyFirstBlood] = FantasyFirstBlood

        Col_pStuns = "p"+str(i)+"Stuns"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pStuns] = playerData["stuns"]
        Col_pFantasyStuns = "p"+str(i)+"FantasyStuns"
        FantasyStuns = 0.05*playerData["stuns"]
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFantasyStuns] = FantasyStuns        

        Col_pWon = "p"+str(i)+"Won"
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pWon] = playerData["win"]

        Col_pFantasyTotal = "p"+str(i)+"FantasyTotal"        
        FantasyTotalA=FantasyKills+FantasyDeaths+FantasyGPM+FantasyCS+playerData["tower_kills"]+playerData["roshan_kills"]
        FantasyTotalB=Teamfight+FantasyObsPlaced+FantasyCampsStacked+FantasyRunes+FantasyFirstBlood+FantasyStuns
        DatabaseDF.loc[DatabaseDF.MatchID == mID, Col_pFantasyTotal] = FantasyTotalA + FantasyTotalB
       

 DatabaseDF.to_excel(DBPath, index = False)