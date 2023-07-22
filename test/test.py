import requests

API_KEY = "RGAPI-6d554b70-e111-492e-a941-5ef893332960"

def getPuuid(summoner_name: str) -> str:
    response = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={API_KEY}")
    data = response.json()
    return data['puuid']

def getLast20Matches(puuid: str) -> list:
    response = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={API_KEY}")
    data = response.json()
    return data

def retrieveMatchKDA(matchID: str, puuid: str) -> float:
    response = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={API_KEY}")
    matchInfo = response.json()
    playerIndex = matchInfo['metadata']['participants'].index(puuid)
    kda = matchInfo['info']['participants'][playerIndex]['challenges']['kda']
    return kda

def retrieveWinLoss(matchID: str, puuid:str) -> bool:
    response = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={API_KEY}")
    if response.status_code == 200:
        matchInfo = response.json()
        playerIndex = matchInfo['metadata']['participants'].index(puuid)
        wl_ratio = matchInfo['info']['participants'][playerIndex]['win']
        return wl_ratio
    else:
        return response.status_code

p = getPuuid("FrijoleQuemado2")
# print("Puuid:", puuid)

matchIDs = getLast20Matches(p)
#print(matchID)
#print(retrieveMatchKDA(matchID=matchIDs[0], puuid=p))

# wl = retrieveWinLoss(matchID=matchIDs[0], puuid=p)
# print(wl)

totalMatches = len(matchIDs)
kdaPerGame = 0
wins,losses = 0, 0

if totalMatches > 0:
    for i in range(totalMatches):
        matchKDA = retrieveMatchKDA(matchID=matchIDs[i], puuid=p)
        kdaPerGame += matchKDA

        wl = retrieveWinLoss(matchID=matchIDs[i], puuid=p)
        if wl == True:
            wins+=1
        else:
            losses+=1

    winloss = wins/losses
    kdaPerGame /= totalMatches

print(winloss)
print(kdaPerGame)





# res = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/_9Y2xOhOKoZO9BMgYko8o6Ao7WHg78OpTWWKmJnw1GdoPKs6QGd3_R0pUNPhGXbVVGZYDB5Pwwv7Qg/ids?start=0&count=20&api_key=RGAPI-6d554b70-e111-492e-a941-5ef893332960")
# print(res.json())