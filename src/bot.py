import discord
from discord.ext import commands
import league
from datetime import datetime
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
async def normal(ctx, *, summoner_name: str):
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
        await league.getMatches(player['puuid'], gamemode='normal')
        totalMatches = len(league.matchIDs[0])

        # Retrieving each Match's Information
        await league.retrieveAllMatchInfo(matchIDs=league.matchIDs[0])
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
        name = player['name']
        level = player['summonerLevel']
        puuid = player['puuid']
        profileIconId = player['profileIconId']
        summoner_ID = player['id']

        # Retrieving Ranked Information
        await league.retrieveRank(summoner_ID=summoner_ID)
        if len(league.rankData[0]) == 0:
            playerRank = "Not Yet Ranked"
            totalMatches = 0
            winloss = 0
        else:
            rankedInfo = league.rankData[0][0]
            playerRank = rankedInfo['tier'] + ' ' + rankedInfo['rank']
            wins, losses = int(rankedInfo['wins']), int(rankedInfo['losses'])
            totalMatches = wins + losses
            if losses == 0:
                winloss = wins
            else:
                winloss = round(wins / losses, 3)

        # Getting all matches, defaulted at 15
        await league.getMatches(player['puuid'], amount=totalMatches, gamemode="ranked")
        totalMatches = len(league.matchIDs[0])

        # Retrieving each Match's Information
        await league.retrieveAllMatchInfo(matchIDs=league.matchIDs[0])
    except Exception as e:
        print("Error calculating Player Stats:", e)
        await ctx.send(embed=EMBED_FAILURE_MSG)

    # Calculating player's overall KDA across the last 20 matches played
    positions = dict()
    champions = dict()
    kills, deaths = 0, 0
    kdRatio = 0
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
                print("Error calculating Match Stats:", e)
                await ctx.send(embed=EMBED_FAILURE_MSG)
                break

        kdRatio = kills/deaths

    if totalMatches == 0:
        embed = discord.Embed(
            colour=discord.Color.blurple(),
            title=f"Summoner {name}",
            description=f"{name} does not have any ranked games played recently"
        )
    else:
        embed = discord.Embed(
            colour=discord.Color.blurple(),
            title=f"Summoner {name}",
            description=f"Recorded from the last {totalMatches} games played"
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

    embed.add_field(
        name="Current Rank",
        value=playerRank,
        inline=False
    )

    embed.set_thumbnail(
        url=f"https://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{profileIconId}.png")
    # embed.set_image(():

    #     url=f"ddragon.leagueoflegends.com/cdn/12.4.1/img/champion/Aatrox.png"
    # )
    await ctx.send(embed=embed)


@bot.command()
async def freerotation(ctx):
    league.reset()

    await league.getVersion()
    version = league.version[0][0]

    # Retrieving a dictionary of Champion Ids as keys and each corresponding name as values
    await league.getChampsByID(version)
    champ_Id_to_Name = league.champ_Id_to_Name

    # Retrieving All Free Champion Rotations
    await league.retrieveRotations()
    rotations = league.rotations[0]

    maxNewPlayerLevel = 10
    freeChamps = rotations['freeChampionIds']
    freeChampsNew = rotations['freeChampionIdsForNewPlayers']

    freeChampsDisplay = ""
    freeChampsNewDisplay = ""
    for ids in range(len(freeChamps)):
        champConverted = champ_Id_to_Name[str(freeChamps[ids])]
        freeChampsDisplay += f"{champConverted}\n"
    for ids in range(len(freeChampsNew)):
        champConvertedNew = champ_Id_to_Name[str(freeChampsNew[ids])]
        freeChampsNewDisplay += f"{champConvertedNew}\n"

    embed = discord.Embed(
        colour=discord.Color.blurple(),
        title="Free Champions Currently in Rotation",
        description="Subject to change!"
    )

    embed.add_field(
        name='Free Champs',
        value=freeChampsDisplay,
        inline=True
    )
    embed.add_field(
        name='Free Champs (NEW PLAYERS ONLY)',
        value=freeChampsNewDisplay,
        inline=True
    )
    await ctx.send(embed=embed)



@bot.command()
async def champmastery(ctx, *, summoner_name):
    league.reset()

    await league.getVersion()
    version = league.version[0][0]

    try:
        await league.getPlayerInfo(summoner_name=summoner_name)
        player = league.playerData[0]
        name = player['name']
        profileIconId = player['profileIconId']
        summoner_ID = player['id']
    except Exception as e:
        print(f"Error with retrieving Player Data: {e}")
        await ctx.send(embed=EMBED_FAILURE_MSG)

    try:
        await league.getChampMastery(summoner_ID=summoner_ID)
        await league.getChampsByID(version)
    except Exception as e:
        print(f"Error with getting champ Info: {e}")
        await ctx.send(EMBED_FAILURE_MSG)

    top5champs = league.allChampsMastery[0][:5]
    champ_Id_to_Name = league.champ_Id_to_Name
    
    embed = discord.Embed(
        colour=discord.Color.blurple(),
        title=f"{name}'s Top Champions"
    )
    counter = 1
    mainChamp = list()
    for champ in top5champs:
        played = int(champ['lastPlayTime']) / 1000
        timePlayed = datetime.fromtimestamp(played)
        timePlayed = str(timePlayed).split()

        # Converting the date from the written date
        date = timePlayed[0].replace('-','')
        date_object = datetime.strptime(str(date), "%Y%m%d")
        written_date = date_object.strftime("%B %d, %Y")
        
        # Converting the time from military to standard time
        time24Hr = timePlayed[1][:5]
        time_object = datetime.strptime(time24Hr, "%H:%M")
        time12Hr = time_object.strftime("%I:%M %p")
        
        # Retrieving the champ name from the id-to-name conversion dictionary
        championName = champ_Id_to_Name[str(champ['championId'])]
        championLevel = champ['championLevel']
        championPoints = champ['championPoints']

        if counter == 1:
            mainChamp.append(championName)
            mainChamp.append(str(champ['championId']))

        embed.add_field(
            name=f"Champion #{counter} - {championName}",
            value=f"LEVEL: {championLevel}\nTOTAL POINTS: {championPoints}\nLAST PLAYED: {written_date} | {time12Hr}",
            inline=True
        )
        counter += 1

    embed.set_thumbnail(
        url=f"https://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{profileIconId}.png"
    )

    embed.set_footer(
        text=f"This Person is a {mainChamp[0]} main!"
    )
    embed.set_image(
    url=f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{mainChamp[1]}.png"
    )

    await ctx.send(embed=embed)

@bot.command()
async def champions(ctx):
    league.reset()

    await league.getVersion()
    version = league.version[0][0]

    await league.getChampsByID(version)

    allChampsFirstHalf = ""
    allChampsSecondHalf = ""
    allChampsThirdHalf = ""
    totalChamps = len(league.champ_Id_to_Name.values())
    counter = 0
    for champ in league.champ_Id_to_Name.values():
        if counter < totalChamps / 3:
            allChampsFirstHalf += f"{champ}\n"
        elif counter < totalChamps - (totalChamps/3):
            allChampsSecondHalf += f"{champ}\n"
        else:
            allChampsThirdHalf += f"{champ}\n"
        counter += 1
    
    embed = discord.Embed(
        color=discord.Color.dark_gold(),
        title=f"All Current Champs as of Version {version}",
        url="https://www.leagueoflegends.com/en-us/champions/"
    )
    
    embed.add_field(
        name=f"Champs 1 - {int(totalChamps/3)}",
        value=allChampsFirstHalf,
        inline=True
    )
    embed.add_field(
        name=f"Champs {int(totalChamps/3) + 1} - {totalChamps - (int(totalChamps/3))}",
        value=allChampsSecondHalf,
        inline=True
    )
    embed.add_field(
        name=f"Champs {totalChamps - (int(totalChamps/3)) + 1} - {totalChamps}",
        value=allChampsThirdHalf,
        inline=True
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def champ(ctx, champion, summoner_name):
    league.reset()

    await league.getVersion()
    version = league.version[0][0]

    await league.getChampsByID(version)
    try:
        championId = league.champ_Name_to_ID[champion]
    except Exception as e:
        print("Error with obtaining champion ID:", e)
        embedFailed = discord.Embed(
            color=discord.Color.red(),
            title="Sorry, I think you might have misspelled the champion Name",
            description="Please try again."
        )
        embedFailed.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/5/5f/Icon_Simple_Error.png"
        )
        await ctx.send(embed=embedFailed)
    try:
        await league.getPlayerInfo(summoner_name=summoner_name)
        player = league.playerData[0]
        puuid = player['puuid']
    except Exception as e:
        print("Error with obtaining player information:", e)
        await ctx.send(embed=EMBED_FAILURE_MSG)

    await league.getMatches(puuid=puuid,amount=20)
    await league.retrieveAllMatchInfo(league.matchIDs[0])

    counter = 0
    kills, deaths = 0, 0
    kdRatio = 0
    wins, losses = 0, 0
    winloss = 0
    for match in league.matchInfo:
        try:
            playerIndex = match['metadata']['participants'].index(puuid)
            if champion == match['info']['participants'][playerIndex]['championName']:
                counter+=1            
            kills += match['info']['participants'][playerIndex]['kills']
            deaths += match['info']['participants'][playerIndex]['deaths']

            # WIN/LOSS CALCULATION
            wonGame = match['info']['participants'][playerIndex]['win']
            if wonGame == True:
                wins += 1
            else:
                losses += 1
        except KeyError:
            print(f"Skipping match due to missing 'metadata' key.")
            continue

    if losses == 0:
        winloss = wins
    else:
        winloss = wins/losses

    if deaths == 0:
        kdRatio = kills
    else:
        kdRatio = kills/deaths

    embed = discord.Embed(
        color=discord.Color.blurple(),
        title=f"{summoner_name}'s {champion} Stats",
        description= "NOTE: if stats show 0, we might not have enough recent data to calculate from."
    )

    embed.add_field(
        name="KDA",
        value=round(kdRatio,2),
        inline=True
    )
    embed.add_field(
        name="W/L",
        value=round(winloss,2),
        inline=True
    )
    embed.set_thumbnail(
        url=f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{championId}.png"
    )

    await ctx.send(embed=embed)


# Running the bot using the Discord Key
bot.run(league.DISCORD_KEY)
