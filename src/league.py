import aiohttp
import asyncio
import sys
sys.path.insert(1,r"C:\Users\tents\LeagueBotV_0\hidden")
import hiddenInfo

API_KEY = hiddenInfo.LEAGUE_KEY
DISCORD_KEY = hiddenInfo.DISCORD_KEY
# REGION = "na1"

version = list()
async def getVersion():
    async with aiohttp.ClientSession() as session:
        response = await session.get(f"https://ddragon.leagueoflegends.com/api/versions.json")
        version.append(await response.json())

playerData = list()
async def getPlayerInfo(summoner_name: str) -> str:
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

rankData = list()
async def retrieveRank(summoner_ID:str):
    async with aiohttp.ClientSession() as session:
        response = await session.get(f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_ID}?api_key={API_KEY}",ssl=False)
        rankData.append(await response.json())

rotations = list()
async def retrieveRotations():
    async with aiohttp.ClientSession() as session:
        response = await session.get(f"https://na1.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={API_KEY}")
        rotations.append(await response.json())


champ_Id_to_Name = dict()
async def getChampsByID(version: str):
    champions = list()
    async with aiohttp.ClientSession() as session:
        response = await session.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json")
        champions.append(await response.json())

    for champ_name, champ_data in champions[0]['data'].items():
        champ_Id_to_Name[champ_data['key']] = champ_name


def reset():
    global version, playerData, matchIDs, matchInfo, rankData, champ_Id_to_Name
    version, playerData, matchIDs, matchInfo, rankData, champ_Id_to_Name = list(), list(), list(), list(), list(), dict()