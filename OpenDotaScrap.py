import requests
import time
import json
import os
import pandas as pd

#this script takes the Matches ID in Database and request the match information from OpenDota through their api and store it in a json file

#path is assigned in Database Manager
# path = #assign this variable if you want to use this script by itself
def Run(path):

 UserAgent = {
    'User-Agent': 'Fantasy Dota 2 Database Manager',
    'From': '@gmail.com'
 }

 DBPath = path+os.sep+"Database.xlsx"
 DatabaseDF = pd.read_excel (DBPath)
 DatabaseMatchList = DatabaseDF['MatchID'].values.tolist()

 #this text file contains a counter that can be used to track how many request have been made to OpenDota
 #OpenDota has a limit of 50 000 per month
 CounterPath = path+os.sep+"OpenDotaCounter.txt"
 CounterTXT = pd.read_csv (CounterPath)
 CounterDF = pd.DataFrame(CounterTXT, columns= ['counter'])
 print(CounterDF)
 CounterNumber = CounterDF.loc[0,"counter"]
 print("OpenDota Counter:",CounterNumber)

 for mID in DatabaseMatchList:   
   #Database has a column to check if this match file has already been requested from OpenDota
   IsDoneL = DatabaseDF.loc[DatabaseDF.MatchID == mID, "OpenDota"]
   IsDone = IsDoneL.iat[0]
   print(mID,IsDone)

   if  (IsDone != "done") and (IsDone != "skip"):
      
      mIDstr = str(mID)

      URL = "https://api.opendota.com/api/matches/" + mIDstr[0:10]
      print(URL)

      request = requests.get(URL, headers=UserAgent)
      print("GET:",mIDstr[0:10])
      CounterNumber = CounterNumber+1
      time.sleep(2)
      data = request.json()
      file = open(path+os.sep+"MatchData"+os.sep+mIDstr[0:10]+"_data.json",'w')
      json.dump(data,file)
      file.close()

      DatabaseDF.loc[DatabaseDF.MatchID == mID, "OpenDota"] = "done"

 DataCounterFinal = {'counter': [CounterNumber]}
 DFCounterFinal = pd.DataFrame(DataCounterFinal, columns= ['counter'])
 DFCounterFinal.to_csv(CounterPath, index = False)

 DatabaseDF.to_excel(DBPath, index = False)
