import os
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

#this script extracts the text data from a Liquipedia page and takes all MatchIDs that appear on the page

#path is assigned in Database Manager
# path = #assign this variable if you want to use this script by itself
def Run(path):
 
 UserAgent = {
    'User-Agent': 'Fantasy Dota 2 Database Manager',
    'From': 'rromanmartin@gmail.com'
 }
 
 #Links from liquipedia are in this file
 LinkTPath = path+os.sep+"liquipedia.txt"
 LinkTXT = pd.read_csv (LinkTPath)
 LinkDF = pd.DataFrame(LinkTXT, columns= ['Link'])
 LinkList = LinkDF['Link'].values.tolist()

 #Links that have been added already are stored in this file so they arent added again
 LinkAPath = path+os.sep+"liquipediaAdded.txt"
 LinkAddedTXT = pd.read_csv (LinkAPath)
 LinkAddedDF = pd.DataFrame(LinkAddedTXT, columns= ['Link'])
 LinkAddedList = LinkAddedDF['Link'].values.tolist()

 #this takes the current existing Database to add the new matches
 DBPath = path+os.sep+"Database.xlsx"
 DatabaseDF = pd.read_excel (DBPath)

 MatchDBList = DatabaseDF["MatchID"].values
 #print(MatchDBList)
 
 for u in LinkList: 
    #changes the webpage so the Match Id information appears in the text body instead of popup windows, as occurs in most liquipedia pages 
    u2 = u.replace("https://liquipedia.net/dota2/","")
    url= "https://liquipedia.net/dota2/index.php?title="+u2+"&action=edit"

    if (u != "Link") and ( u in LinkAddedList ):
        LinkList.remove(u)

    if (u != "Link") and ( (u in LinkAddedList)== False ):                
        print(u)
        page = requests.get(url, headers=UserAgent)
        time.sleep(2)
        soup = BeautifulSoup(page.content, "html.parser")

        FullText = soup.find(id="wpTextbox1")
        string = FullText.text
        substring = "matchid"
          
        MatchList = []        

        #finds the index of all substring in string
        allindex = [i for i in range(len(string)) if string.startswith(substring, i)]

        #prints all match id
        for a in allindex:
            startIndex = int(a) + 9
            endIndex = startIndex + 10
            MatchList.append(string[startIndex:endIndex])

        Words = string.split("|")

        # m is every match id, w is every word in text (using | as the separator)                
        for m in MatchList:
            for w in Words:
                if m in w:                    
                    if int(m) in MatchDBList:
                        print(m," already in Database")
                    else:
                        DatabaseDF.loc[len(DatabaseDF), "MatchID"] = m
                        DatabaseDF.loc[DatabaseDF.MatchID == m, "Liquipedia"] = u2                    
                        print(m," added")

        LinkAddedList.append(u)
        LinkList.remove(u)            
 
 DatabaseDF.to_excel(DBPath, index = False)

 #Print a new liquipediaAdded and liquipedia txt file
 DFLinkTFinal = pd.DataFrame (LinkList, columns = ['Link'])
 DFLinkTFinal.to_csv(LinkTPath, index = False)
 DFLinkAFinal = pd.DataFrame (LinkAddedList, columns = ['Link'])
 DFLinkAFinal.to_csv(LinkAPath, index = False)
            
            
