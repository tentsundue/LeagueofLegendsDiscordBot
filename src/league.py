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

def reset():
    global version, playerData, matchIDs, matchInfo
    version, playerData, matchIDs, matchInfo = list(), list(), list(), list()