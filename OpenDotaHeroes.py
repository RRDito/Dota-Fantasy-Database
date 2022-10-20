import requests
import time
import json
import os
import pandas as pd

#this script extracts the hero data from OpenDota and stores it in a json file

#path is assigned in Database Manager
# path = #assign this variable if you want to use this script by itself
def Run(path):

 UserAgent = {
    'User-Agent': 'Fantasy Dota 2 Database Manager',
    'From': 'https://github.com/RRDito/Dota-Fantasy-Database'
 }
 CounterPath = path+os.sep+"OpenDotaCounter.txt"
 CounterTXT = pd.read_csv (CounterPath)
 CounterDF = pd.DataFrame(CounterTXT, columns= ['counter'])
 print(CounterDF)
 CounterNumber = CounterDF.loc[0,"counter"]
 print("OpenDota Counter:",CounterNumber)

 URL = "https://api.opendota.com/api/heroStats"
 print(URL)

 request = requests.get(URL, headers=UserAgent)
 CounterNumber = CounterNumber+1
 time.sleep(2)
 data = request.json()
 file = open(path+os.sep+"HeroStats.json",'w')
 json.dump(data,file)
 file.close()

 DataCounterFinal = {'counter': [CounterNumber]}
 DFCounterFinal = pd.DataFrame(DataCounterFinal, columns= ['counter'])
 DFCounterFinal.to_csv(CounterPath, index = False)
