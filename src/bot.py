import discord
from discord.ext import commands
import requests
import league

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# # FOR API CALLS
# API_KEY = "RGAPI-b7978728-8d64-4cb6-b72f-8f58e7774014"
# REGION = "na1"


# def getPlayerInfo(summoner_name: str):
#     response = requests.get(
#         f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={API_KEY}")
#     if response.status_code == 200:
#         data = response.json()
#         return data
#     else:
#         return response.status_code


# def getMatchIDs(puuid: str) -> list:
#     response = requests.get(
#         f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={API_KEY}")
#     if response.status_code == 200:
#         data = response.json()
#         return data
#     else:
#         return response


# def retrieveMatchKDA(matchID: str, puuid: str) -> float:
#     response = requests.get(
#         f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={API_KEY}")
#     matchInfo = response.json()
#     playerIndex = matchInfo['metadata']['participants'].index(puuid)
#     kda = matchInfo['info']['participants'][playerIndex]['challenges']['kda']
#     return kda


# def retrieveWinLoss(matchID: str, puuid: str) -> bool:
#     response = requests.get(
#         f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={API_KEY}")
#     if response.status_code == 200:
#         matchInfo = response.json()
#         playerIndex = matchInfo['metadata']['participants'].index(puuid)
#         wl_ratio = matchInfo['info']['participants'][playerIndex]['win']
#         return wl_ratio
#     else:
#         return response.status_code


@bot.command()
async def summoner(ctx, *, summoner_name: str):
    playerInfo = league.getPlayerInfo(summoner_name=summoner_name)
    if type(playerInfo) == int:
        await ctx.send(f"Error: {playerInfo} | Please try again later")
    else:
        # Storing player name, level, and puuid
        # Note: PUUID will be used for later api calls and such
        name = playerInfo['name']
        level = playerInfo['summonerLevel']
        puuid = playerInfo['puuid']

        # Calculating player's overall KDA across the last 20 matches played
        matchIDs = league.getMatchIDs(puuid=puuid)  # List of last 20 matches
        totalMatches = len(matchIDs)
        kdaPerGame = 0
        wins, losses = 0, 0

        if totalMatches > 0:
            for i in range(totalMatches):
                matchKDA = league.retrieveMatchKDA(matchID=matchIDs[i], puuid=puuid)
                kdaPerGame += matchKDA

                wl = league.retrieveWinLoss(matchID=matchIDs[i], puuid=puuid)
                if wl == True:
                    wins += 1
                else:
                    losses += 1

            winloss = round(wins/losses, 2)
            kdaPerGame /= totalMatches
            kdaPerGame = round(kdaPerGame, 2)

        embed = discord.Embed(
            colour=discord.Color.blurple(),
            title=f"Summoner {name}",
            description="Recorded from the last ~20 games played"
        )
        # Level field
        embed.add_field(
            name="Level",
            value=level,
            inline=True
        )
        # Overall KDA per game field
        embed.add_field(
            name="Average KDA",
            value=kdaPerGame,
            inline=True
        )
        # Winrate percentage field (based on number of games won divided by all games played)
        embed.add_field(
            name="Average WinRate",
            value=winloss,
            inline=True
        )

        embed.set_thumbnail(
            url="https://e0.pxfuel.com/wallpapers/8/121/desktop-wallpaper-suz-on-memes-beetlejuice-green-beetlejuice-lester-green.jpg")

        await ctx.send(embed=embed)


bot.run("MTEzMTM3NDMzOTUxODkwMjM0Mg.GzMk0f.KaSXzD2FKkYRqpiezX5ukh30mUF4t6Ei987i8I")
