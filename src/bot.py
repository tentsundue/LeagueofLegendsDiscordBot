import discord
from discord.ext import commands
import league
import sys

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

EMBED_FAILURE_MSG = discord.Embed(
    colour=discord.Color.red(),
    title=f"An Error occured",
    description="Please try again."
)
EMBED_FAILURE_MSG.set_thumbnail(
    url="https://upload.wikimedia.org/wikipedia/commons/5/5f/Icon_Simple_Error.png")


@bot.command()
async def player(ctx, *, summoner_name: str):
    league.reset()

    await league.getVersion()
    version = league.version[0][0]
    # Getting all player's/summoner's required Information
    try:
        await league.getPlayerInfo(summoner_name=summoner_name)
        player = league.playerData[0]
        print(player)
        name = player['name']
        level = player['summonerLevel']
        puuid = player['puuid']
        profileIconId = player['profileIconId']

        # Getting all matches, defaulted at 15
        await league.getMatches(player['puuid'])
        totalMatches = len(league.matchIDs[0])

        # Retrieving each Match's Information
        await league.retrieveAllMatchInfo(matchIDs=league.matchIDs[0], puuid=puuid)
    except Exception as e:
        print("Error calculating Player Stats:", e)
        await ctx.send(embed=EMBED_FAILURE_MSG)

    # Calculating player's overall KDA across the last 20 matches played
    positions = dict()
    champions = dict()
    kills, deaths = 0, 0
    wins, losses = 0, 0
    kdRatio = 0

    if totalMatches > 0:
        for match in league.matchInfo:
            try:
                # IDENTIFYING A PLAYER ID (PUUID) FOR THE MATCH
                playerIndex = match['metadata']['participants'].index(puuid)

                # KDA CALCULATION
                kills += match['info']['participants'][playerIndex]['kills']
                deaths += match['info']['participants'][playerIndex]['deaths']

                # WIN/LOSS CALCULATION
                wl_ratio = match['info']['participants'][playerIndex]['win']
                if wl_ratio == True:
                    wins += 1
                else:
                    losses += 1

                # POSITION AND CHAMPION RECORDS
                maxPosCounter, maxChampCounter = 0, 0
                mostPlayedPos, mostPlayedChamp = "None", "None"
                position = match['info']['participants'][playerIndex]['individualPosition']
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

            except Exception as e:
                print("Error calculating Player Stats:", e)
                await ctx.send(embed=EMBED_FAILURE_MSG)
                break

        if losses == 0:
            winloss = wins
        else:
            winloss = wins/losses
        kdRatio = kills/deaths

    embed = discord.Embed(
        colour=discord.Color.blurple(),
        title=f"Summoner {name}",
        description="Recorded from the last (~15) games played"
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
        value=round(kdRatio, 3),
        inline=True
    )
    # Winrate percentage field (based on number of games won divided by all games played)
    embed.add_field(
        name="Average Win Rate",
        value=round(winloss, 3),
        inline=True
    )
    # Most Played Champion field
    embed.add_field(
        name="Most Played Champ",
        value=mostPlayedChamp,
        inline=False
    )
    # Most Played Position field
    embed.add_field(
        name="Most Played Position",
        value=mostPlayedPos,
        inline=False
    )

    embed.set_thumbnail(
        url=f"https://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{profileIconId}.png")
    # embed.set_image(
    #     url=f"ddragon.leagueoflegends.com/cdn/12.4.1/img/champion/Aatrox.png"
    # )
    await ctx.send(embed=embed)


@bot.command()
async def ranked(ctx, *, summoner_name: str):
    league.reset()

    await league.getVersion()
    version = league.version[0][0]
    # Getting all player's/summoner's required Information
    try:
        await league.getPlayerInfo(summoner_name=summoner_name)
        player = league.playerData[0]
        print(player)
        name = player['name']
        level = player['summonerLevel']
        puuid = player['puuid']
        profileIconId = player['profileIconId']

        # Getting all matches, defaulted at 15
        await league.getMatches(player['puuid'],gamemode="ranked")
        totalMatches = len(league.matchIDs[0])

        # Retrieving each Match's Information
        await league.retrieveAllMatchInfo(matchIDs=league.matchIDs[0], puuid=puuid)
    except Exception as e:
        print("Error calculating Player Stats:", e)
        await ctx.send(embed=EMBED_FAILURE_MSG)

    # Calculating player's overall KDA across the last 20 matches played
    positions = dict()
    champions = dict()
    kills, deaths = 0, 0
    wins, losses = 0, 0
    kdRatio = 0
    winloss = 0
    mostPlayedChamp = "Unknown/Not enough Games Played"
    mostPlayedPos = "Unknown/Not enough Games Played"
    
    if totalMatches > 0:
        for match in league.matchInfo:
            try:
                # IDENTIFYING A PLAYER ID (PUUID) FOR THE MATCH
                playerIndex = match['metadata']['participants'].index(puuid)

                # KDA CALCULATION
                kills += match['info']['participants'][playerIndex]['kills']
                deaths += match['info']['participants'][playerIndex]['deaths']

                # WIN/LOSS CALCULATION
                wl_ratio = match['info']['participants'][playerIndex]['win']
                if wl_ratio == True:
                    wins += 1
                else:
                    losses += 1

                # POSITION AND CHAMPION RECORDS
                maxPosCounter, maxChampCounter = 0, 0
                mostPlayedPos, mostPlayedChamp = "None", "None"
                position = match['info']['participants'][playerIndex]['individualPosition']
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

            except Exception as e:
                print("Error calculating Player Stats:", e)
                await ctx.send(embed=EMBED_FAILURE_MSG)
                break

        if losses == 0:
            winloss = wins
        else:
            winloss = wins/losses
        kdRatio = kills/deaths

    embed = discord.Embed(
        colour=discord.Color.blurple(),
        title=f"Summoner {name}",
        description="Recorded from the last (~15) games played"
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
        value=round(kdRatio, 3),
        inline=True
    )
    # Winrate percentage field (based on number of games won divided by all games played)
    embed.add_field(
        name="Average Win Rate",
        value=round(winloss, 3),
        inline=True
    )
    # Most Played Champion field
    embed.add_field(
        name="Most Played Champ",
        value=mostPlayedChamp,
        inline=False
    )
    # Most Played Position field
    embed.add_field(
        name="Most Played Position",
        value=mostPlayedPos,
        inline=False
    )

    embed.set_thumbnail(
        url=f"https://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{profileIconId}.png")
    # embed.set_image(
    #     url=f"ddragon.leagueoflegends.com/cdn/12.4.1/img/champion/Aatrox.png"
    # )
    await ctx.send(embed=embed)


bot.run(league.DISCORD_KEY)
