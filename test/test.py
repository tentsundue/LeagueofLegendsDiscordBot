import requests
import aiohttp
import discord
from discord.ext import commands
import asyncio
import time

API_KEY = "RGAPI-6642c4d6-3c07-4755-bbdd-60969dfafebe"


start = time.time()
playerData = list()


async def getPuuid(summoner_name: str) -> str:
    # response = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={API_KEY}")
    # data = response.json()
    # return data['puuid']

    async with aiohttp.ClientSession() as session:
        response = await session.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={API_KEY}", ssl=False)
        playerData.append(await response.json())

matchIDs = list()


async def getMatches(puuid: str, amount=15) -> list:
    async with aiohttp.ClientSession() as session:
        response = await session.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={amount}&api_key={API_KEY}")
        matchIDs.append(await response.json())


def get_tasks(session, matchIDs: list):
    tasks = []
    for i in range(len(matchIDs)):
        # print(len(matchIDs))
        # print(f"Match: {matchIDs[i]}")
        tasks.append(session.get(
            f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchIDs[i]}?api_key={API_KEY}", ssl=False))
    return tasks


matchInfo = list()
async def retrieveAllMatchInfo(matchIDs: str, puuid: str) -> float:
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, matchIDs=matchIDs)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            matchInfo.append(await response.json())

# def retrieveWinLoss(matchID: str, puuid:str) -> bool:
#     response = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={API_KEY}")
#     if response.status_code == 200:
#         matchInfo = response.json()
#         playerIndex = matchInfo['metadata']['participants'].index(puuid)
#         wl_ratio = matchInfo['info']['participants'][playerIndex]['win']
#         return wl_ratio
#     else:
#         return response.status_code

################# TESTING PUUID #################

asyncio.run(getPuuid("FrijoleQuemado2"))
# end = time.time()

# totaltime = end - start
# print('Time taken:', round((totaltime), 3), 'seconds')
p = playerData[0]['puuid']
print(f"Response: {p}")
print("-------------------------END-------------------------\n")

################# END OF PUUID TESTING #################


################# TESTING LAST 20 MATCHES RETRIEVAL #################

asyncio.run(getMatches(playerData[0]['puuid']))
print(matchIDs)
# end = time.time()

# totaltime = end - start
# print('Time taken:', round((totaltime), 3), 'seconds')
print("-------------------------END-------------------------\n")

################# END OF TESTING LAST 20 MATCHES RETRIEVAL #################


################# TESTING RETRIEVE MATCH KDA #################

# print(retrieveMatchKDA(matchID=matchIDs[0], puuid=p))
# retrieveMatchKDA(matchID=matchIDs[0], puuid=p)
# wl = retrieveWinLoss(matchID=matchIDs[0], puuid=p)
# print(wl)
print("TESTING RETRIEVE MATCH KDA\n")
totalMatches = len(matchIDs[0])
print(f"Total Matches: {totalMatches}")

asyncio.run(retrieveAllMatchInfo(matchIDs=matchIDs[0], puuid=p))
# print("MatcKDAs: ", matchKDAs)
end = time.time()
totaltime = end - start
print('Time taken:', round((totaltime), 3), 'seconds')
print(f"length of match KDAs: {len(matchInfo)}")

i = 0

# Implementation of KDAs and Win/Loss Calculations
kdaPerGame = 0
wins,losses = 0, 0
if totalMatches > 0:
    for match in matchInfo:
        # IDENTIFYING A PLAYER ID (PUUID) FOR THE MATCH
        playerIndex = match['metadata']['participants'].index(p)

        # KDA CALCULATION
        kda = match['info']['participants'][playerIndex]['challenges']['kda']
        kdaPerGame += kda

        # WIN/LOSS CALCULATION
        wl_ratio = match['info']['participants'][playerIndex]['win']
        if wl_ratio == True:
            wins += 1
        else:
            losses += 1
    
    winloss = wins/losses
    kdaPerGame /= totalMatches

    print("Winloss:", winloss)
    print("KDA:", kdaPerGame)


# print(i)
# if totalMatches > 0:
#     for i in range(totalMatches):
#         asyncio.run(retrieveMatchKDA(matchID=matchIDs[0][i], puuid=p))
#         kdaPerGame += matchKDA

#         wl = retrieveWinLoss(matchID=matchIDs[i], puuid=p)
#         if wl == True:
#             wins+=1
#         else:
#             losses+=1

#     winloss = wins/losses
#     kdaPerGame /= totalMatches

# print(winloss)
# print(kdaPerGame)


# res = requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/_9Y2xOhOKoZO9BMgYko8o6Ao7WHg78OpTWWKmJnw1GdoPKs6QGd3_R0pUNPhGXbVVGZYDB5Pwwv7Qg/ids?start=0&count=20&api_key=RGAPI-6d554b70-e111-492e-a941-5ef893332960")
# print(res.json())
