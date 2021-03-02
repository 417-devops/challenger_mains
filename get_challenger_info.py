# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 13:22:32 2021

@author: compute
"""

#first the list of challenger players
#Then calculate their role
#get top champions
import cassiopeia as cass
import roleml

from datetime import timedelta
import time
import json

def getAPI_key():
    f = open("../api_key.txt", "r")
    return f.read()

def analyzeMatch(match,summoner):
    p = match.participants[summoner]
    roleml.change_role_formatting('full')
    
    match.timeline.load()
    roleml.predict(match.to_dict(), match.timeline.to_dict(), True)
    roleml.add_cass_predicted_roles(match) 
    role= p.predicted_role  
    
    print(role)
    
def get_challenger_data():
    data= cass.get_challenger_league(cass.Queue.ranked_solo_fives) #get the challenger data
    
    summonerNames=[]
    role_dict= []
    champ_dict= []
    for item in data.entries:
        summonerNames.append(item.summoner.name)
        
        if data.entries.index(item) %10 ==0:
            #print every 10 entries to update user
            print('\nCURRENT LADDER ENTRY= ', data.entries.index(item))
        
        elif data.entries.index(item) ==2:
            break
        
        summoner= item.summoner
        match_history = summoner.match_history(queues={cass.Queue.ranked_solo_fives}, 
                                            begin_index=0, end_index=4)
        roles= []
        champions= []
        for match in match_history:
            if match.is_remake:
                pass
            elif match.duration < timedelta(minutes=15, seconds= 30):
                # skip ff at 15
                pass
            else:
                #now we want the role [top, mid, jg, adc, support] and champion
                #keep track of each one per match to find most common
                analyzeMatch(match,summoner)
    
#%% Main run                 
if __name__ == "__main__":
    start_time = time.time()
    cass.set_riot_api_key(getAPI_key()) #or replace with your own api key
    cass.set_default_region("NA") #or replace with another region
    
    with open('championFull.json', 'r') as champList_file:
        champList = json.load(champList_file)
        champList_file.close()
        champList= champList['keys']
    
    
    get_challenger_data()
    
    print("\n--- %s seconds ---" % (time.time() - start_time))