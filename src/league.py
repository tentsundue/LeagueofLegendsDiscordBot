import requests
import aiohttp

API_KEY = "RGAPI-b7978728-8d64-4cb6-b72f-8f58e7774014"
REGION = "na1"

def getPlayerInfo(summoner_name: str):
    response = requests.get(
        f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={API_KEY}")
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return response.status_code


def getMatchIDs(puuid: str) -> list:
    response = requests.get(
        f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={API_KEY}")
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return response


def retrieveMatchKDA(matchID: str, puuid: str) -> float:
    response = requests.get(
        f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={API_KEY}")
    matchInfo = response.json()
    playerIndex = matchInfo['metadata']['participants'].index(puuid)
    kda = matchInfo['info']['participants'][playerIndex]['challenges']['kda']
    return kda


def retrieveWinLoss(matchID: str, puuid: str) -> bool:
    response = requests.get(
        f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={API_KEY}")
    if response.status_code == 200:
        matchInfo = response.json()
        playerIndex = matchInfo['metadata']['participants'].index(puuid)
        wl_ratio = matchInfo['info']['participants'][playerIndex]['win']
        return wl_ratio
    else:
        return response.status_code