# Import everything from the utilities folder. Defined in __init__.py of the relevant folder
from utilities import *

import pprint # https://docs.python.org/3.6/library/pprint.html

import random
import discord
import json

from utilities import config


async def main(ctx, bot, args):
    talentsJson = open("./priorities/wiztalents.json")
    talents = json.load(talentsJson)

    # Preprare args for use.
    argsStr = " ".join(args)
    splitArgs = argsStr.split(",")
    desiredTalents = []
    desPriorities = []
    for arg in splitArgs:
        arg = arg.strip()
        arg = arg.lower()
        if "defy" in arg and "defying" not in arg:
            arg = arg.replace("defy", "defying")
        if "armour" in arg:
            arg = arg.replace("armour", "armor")

        if "'" in arg:
            arg = arg.replace("'", "")
        if "." in arg:
            arg = arg.replace(".", "")
        if "-" in arg:
            arg = arg.replace("-", " ")

        if arg.isdigit():
            desPriorities.append(int(arg))
        elif arg.lower() == "top":
            desPriorities.append(0)
        elif arg.lower() == "bottom":
            desPriorities.append(len(talents)-1)

        desiredTalents.append(arg)

    foundTalents = []

    for num in desPriorities:
        name = talents[num]["name"]
        if "-" in name:
            name = name.replace("-", " ")
        if "'" in name:
            name = name.replace("'", "")
        if "." in name:
            name = name.replace(".", "")

        tal = {
                "name": name,
                "rank": talents[num]["rank"],
                "url": talents[num]["url"],
                "valid_url": talents[num]["valid_url"],
                "locked": talents[num]["locked"],
                "priority": num
            }
        foundTalents.append(tal)

    c = 0
    for talent in talents:
        name = talent["name"]
        if "-" in name:
            name = name.replace("-", " ")
        if "'" in name:
            name = name.replace("'", "")
        if "." in name:
            name = name.replace(".", "")

        if [d for d in desiredTalents if d in name.lower()]:
            tal = {
                "name": name,
                "rank": talent["rank"],
                "url": talent["url"],
                "valid_url": talent["valid_url"],
                "locked": talent["locked"],
                "priority": c
            }

            foundTalents.append(tal)
        c += 1

    # Order the array by priority
    foundTalents = sorted(foundTalents, key = lambda x : x["priority"])    
    if len(foundTalents) < 16:
        return await returnEmbed(ctx, foundTalents)
    else:
        print("else")
        chunks = []
        while foundTalents:
            chunks.append(foundTalents[:10])
            foundTalents = foundTalents[10:]

        await ctx.author.send("start")
        for chunk in chunks:
            talentsArray = ["Priority | Rank | Name | Locked/Unlocked Position"]
            for talent in chunk:
                name = talent["name"]
                priority = talent["priority"]
                if len(str(priority)) == 1:
                    priority = f"00{priority}"
                elif len(str(priority)) == 2:
                    priority = f"0{priority}"

                rank = talent["rank"]
                if rank == "Common":
                    rank = "C "
                elif rank == "Uncommon":
                    rank = "UC"
                elif rank == "Rare":
                    rank = "R "
                elif rank == "Ultra Rare":
                    rank = "UR"
                elif rank == "Epic":
                    rank = "E "

                talentMsg = ""
                unlocked = ""
                unlockables = ["finder", "hunter", "scout", "farmer", "trained", "track r treater", "elemental retriever", "hatch catcher"]
                for u in unlockables:
                    if u in name.lower():
                        print(name.lower())
                        if name.lower() != "well trained":
                            print("not")
                            #print("match!!!")
                            if talent["locked"] == True:
                                #print("true!")
                                unlocked = " | Locked"
                            elif talent["locked"] == False:
                                #print("false!")
                                unlocked = " | Unlocked"
                            else:
                                print("this shouldnt happen ever")

                talentMsg = f"> `{priority}` | `{rank}` | {name}{unlocked}"
                talentsArray.append(talentMsg)

            await ctx.author.send("\n".join(talentsArray))

        await ctx.send("task completed! check your dms")


async def returnEmbed(ctx, foundTalents):
    colour = await s.randomColour()
    imgUrl = ctx.author.avatar
    if imgUrl == None:
        imgUrl = "https://imgs.search.brave.com/939ccTKsYFEeMd6uGxCDJogJz7BoSe99XqJhmqhE-FY/rs:fit:630:630:1/g:ce/aHR0cHM6Ly9pczIt/c3NsLm16c3RhdGlj/LmNvbS9pbWFnZS90/aHVtYi9QdXJwbGUx/MjIvdjQvMDUvOWMv/YWYvMDU5Y2FmM2It/MTE1YS0xZmNhLTE0/MTktODllYzE0NjNk/MGFiL3NvdXJjZS8x/MjAweDYzMGJiLmpw/Zw"

    talentsArray = []
    for talent in foundTalents:
        name = talent["name"]
        url = talent["url"]
        urlCheck = talent["valid_url"]
        priority = talent["priority"]
        if len(str(priority)) == 1:
            priority = f"00{priority}"
        elif len(str(priority)) == 2:
            priority = f"0{priority}"

        rank = talent["rank"]        
        if rank == "Common":
            rank = "C "
        elif rank == "Uncommon":
            rank = "UC"
        elif rank == "Rare":
            rank = "R "
        elif rank == "Ultra Rare":
            rank = "UR"
        elif rank == "Epic":
            rank = "E "

        talentMsg = ""
        unlocked = ""
        unlockables = ["finder", "hunter", "scout", "farmer", "trained", "track r treater", "elemental retriever", "hatch catcher"]
        for u in unlockables:
            if u in name.lower():
                print(name.lower())
                if name.lower() != "well trained":
                    print("not")
                    #print("match!!!")
                    if talent["locked"] == True:
                         #print("true!")
                        unlocked = " | Locked"
                    elif talent["locked"] == False:
                        #print("false!")
                        unlocked = " | Unlocked"
                    else:
                        print("this shouldnt happen ever")

        if urlCheck == True:
            name = f"[{name}]({url})"

        talentMsg = f"`{priority}` | `{rank}` | {name}{unlocked}"
        talentsArray.append(talentMsg)

    embed = discord.Embed(
        title = f"{ctx.author}",
        description = f"Priority | Rank | Name | Locked/Unlocked Position\n" + "\n".join(talentsArray),
        color = colour
    ).set_thumbnail(
        url = imgUrl
    ).set_footer(
        text = f"Returned {len(foundTalents)} talents."
    )
    await ctx.send(embed = embed)