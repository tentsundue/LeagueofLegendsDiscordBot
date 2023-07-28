import league
import hiddenInfo
import aiohttp
import discord
from discord.ext import commands
import asyncio
import time
import sys
sys.path.insert(1, r"C:\\Users\\tents\\LeagueBotV_0\\hidden")
sys.path.insert(1, r"C:\Users\tents\LeagueBotV_0\src")


rankedIcons = []
API_KEY = hiddenInfo.LEAGUE_KEY
REGION = hiddenInfo.DISCORD_KEY

start = time.time()

version = list()


async def getVersion():
    async with aiohttp.ClientSession() as session:
        response = await session.get(f"https://ddragon.leagueoflegends.com/api/versions.json", ssl=False)
        version.append(await response.json())

playerData = list()


async def getPuuid(summoner_name: str) -> str:
    async with aiohttp.ClientSession() as session:
        response = await session.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={API_KEY}", ssl=False)
        playerData.append(await response.json())

matchIDs = list()


async def getMatches(puuid: str, amount=15, gamemode="") -> list:
    async with aiohttp.ClientSession() as session:
        response = await session.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type={gamemode}&start=0&count={amount}&api_key={API_KEY}")
        matchIDs.append(await response.json())


def get_tasks(session, matchIDs: list):
    tasks = []
    for i in range(len(matchIDs)):
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
wins, losses = 0, 0
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
print("-------------------------END-------------------------\n")

# IMPLEMENTATION OF MOST PLAYED POSITIONS AND CHAMPIONS
positions = dict()
champions = dict()
if totalMatches > 0:
    for match in matchInfo:
        # IDENTIFYING A PLAYER ID (PUUID) FOR THE MATCH
        playerIndex = match['metadata']['participants'].index(p)
        # POSITION AND CHAMPION RECORDS
        maxPosCounter, maxChampCounter = 0, 0
        mostPlayedPos, mostPlayedChamp = "None", "None"
        position = match['info']['participants'][playerIndex]['teamPosition']
        champ = match['info']['participants'][playerIndex]['championName']
        if position in positions:
            positions[position] += 1
        else:
            positions[position] = 1

        if champ in champions:
            champions[champ] += 1
        else:
            champions[champ] = 1

        if maxPosCounter <= positions[position]:
            maxPosCounter = positions[position]
            mostPlayedPos = position
        if maxChampCounter <= positions[position]:
            maxChampCounter = positions[position]
            mostPlayedChamp = champ

print("MOST PLAYED POSITION AND CHAMP:", mostPlayedPos, mostPlayedChamp)
print("-------------------------END-------------------------\n")

# TESTING DATADRAGON VERSION API CALL
asyncio.run(getVersion())
print("VERSION:", version[0][0])
