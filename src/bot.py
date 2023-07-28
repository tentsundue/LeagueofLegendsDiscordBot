import discord
from discord.ext import commands
import league
import sys

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def player(ctx, *, summoner_name: str):
    # Getting all player's/summoner's required Information
    await league.getPlayerInfo(summoner_name=summoner_name)
    player = league.playerData[0]
    name = player['name']
    level = player['summonerLevel']
    puuid = player['puuid']

    # Getting all matches, defaulted at 15
    await league.getMatches(player['puuid'])
    totalMatches = len(league.matchIDs[0])

    # Retrieving each Match's Information
    await league.retrieveAllMatchInfo(matchIDs=league.matchIDs[0], puuid=puuid)

    # Calculating player's overall KDA across the last 20 matches played
    # matchIDs = league.getMatchIDs(puuid=puuid)  # List of last 20 matches
    # totalMatches = len(matchIDs)
    kdaPerGame = 0
    wins,losses = 0, 0
    if totalMatches > 0:
        for match in league.matchInfo:
            # IDENTIFYING A PLAYER ID (PUUID) FOR THE MATCH
            playerIndex = match['metadata']['participants'].index(puuid)

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
        value=round(kdaPerGame,3),
        inline=True
    )
    # Winrate percentage field (based on number of games won divided by all games played)
    embed.add_field(
        name="Average WinRate",
        value=round(winloss,3),
        inline=True
    )

    embed.set_thumbnail(
        url="https://e0.pxfuel.com/wallpapers/8/121/desktop-wallpaper-suz-on-memes-beetlejuice-green-beetlejuice-lester-green.jpg")

    await ctx.send(embed=embed)


bot.run("MTEzMTM3NDMzOTUxODkwMjM0Mg.GzMk0f.KaSXzD2FKkYRqpiezX5ukh30mUF4t6Ei987i8I")
