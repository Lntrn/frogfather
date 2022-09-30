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
    await ctx.send("searching, please wait.")
    
    argsStr = " ".join(args)
    splitArgs = argsStr.split(",")

    epicArr = ["epic", "e", "4"]
    urArr = ["ultra rare", "ur", "3"]
    rareArr = ["rare", "r", "2"]
    ucArr = ["uncommon", "uc", "1"]
    commonArr = ["common", "c", "0"]

    desRank = None
    desiredTalents = []
    if len(splitArgs) > 3:
        return await ctx.send("too many args, try again with a max of 3")

    for arg in splitArgs:
        arg = arg.strip()
        if "defy" in arg.lower() and "defying" not in arg.lower():
            arg = arg.replace("defy", "defying")

        if "armour" in arg.lower():
            arg = arg.replace("armour", "armor")

        if "-" in arg:
            arg = arg.replace("-", " ")
        if "." in arg:
            arg = arg.replace(".", "")
        if "'" in arg:
            arg = arg.replace("'", "")
    
        if arg.lower() in epicArr:
            desRank = "Epic"
        elif arg.lower() in urArr:
            desRank = "Ultra Rare"
        elif arg.lower() in rareArr:
            desRank = "Rare"
        elif arg.lower() in ucArr:
            desRank = "Uncommon"
        elif arg.lower() in commonArr:
            desRank = "Common"
        else:
            if arg.isdigit():
                desiredTalents.append(talents[int(arg)]["name"].lower().replace("-", " "))
            elif arg == "top":
                desiredTalents.append(talents[0]["name"].lower().replace("-", " "))
            elif arg == "bottom":
                desiredTalents.append(talents[-1]["name"].lower().replace("-", " "))
            else:
                desiredTalents.append(arg.lower())

    print(desRank)
    print(desiredTalents)

    arr = []
    c = 0

    for talent in talents:
        name = talent["name"]
        if "-" in name:
            name = name.replace("-", " ")
        if "'" in name:
            name = name.replace("'", "")
        if "." in name:
            name = name.replace(".", "")

        if name.lower() in desiredTalents:
            tal = {
                "name": name,
                "rank": talent["rank"],
                "url": talent["url"],
                "valid_url": talent["valid_url"],
                "locked": talent["locked"],
                "priority": c
            }
            arr.append(tal)
        c += 1

    if arr[0]["priority"] > arr[1]["priority"]:
        _max = arr[0]
        _min = arr[1]
    else:
        _max = arr[1]
        _min = arr[0]

    print(f"Min: {_min['priority']}")
    print(f"Max: {_max['priority']}")

    foundTalents = []
    c = 0

    for talent in talents[_min['priority']+1:_max['priority']]:
        name = talent["name"]
        if "-" in name:
            name = name.replace("-", " ")
        if "'" in name:
            name = name.replace("'", "")
        if "." in name:
            name = name.replace(".", "")

        tal = {
            "name": name,
            "rank": talent["rank"],
            "url": talent["url"],
            "valid_url": talent["valid_url"],
            "locked": talent["locked"],
            "priority": talents.index(talent)
        }

        if desRank != None:
            if talent['rank'] == desRank:
                foundTalents.append(tal)
        else:
            foundTalents.append(tal)
            
        c += 1

    foundTalents = sorted(foundTalents, key = lambda x : x["priority"])

    anotherArr = []

    if desRank != None:
        await ctx.send(f"Only returning `{desRank}` talents.")

    for talent in foundTalents:
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

        unlocked = ""
        unlockables = ["finder", "hunter", "scout", "farmer", "trained", "track r treater", "elemental retriever", "hatch catcher"]
        for u in unlockables:
            if u in name.lower():
                print(name.lower())
                if name.lower() != "well trained":
                    print("not")
                    #print("match!!!")
                    if talent["locked"] == True:
                        unlocked = " | Locked"
                    elif talent["locked"] == False:
                        unlocked = " | Unlocked"
                    else:
                        print("this shouldnt happen ever")

        talentMsg = f"> `{priority}` | `{rank}` | {name}{unlocked}"
        anotherArr.append(talentMsg)

    minRank = _min['rank']
    if minRank == "Common":
        minRank = "C "
    elif minRank == "Uncommon":
        minRank = "UC"
    elif minRank == "Rare":
        minRank = "R "
    elif minRank == "Ultra Rare":
        minRank = "UR"
    elif minRank == "Epic":
        minRank = "E "

    maxRank = _max['rank']
    if maxRank == "Common":
        maxRank = "C "
    elif maxRank == "Uncommon":
        maxRank = "UC"
    elif maxRank == "Rare":
        maxRank = "R "
    elif maxRank == "Ultra Rare":
        maxRank = "UR"
    elif maxRank == "Epic":
        maxRank = "E "

    minPrio = _min['priority']
    if len(str(minPrio)) == 1:
        minPrio = f"00{minPrio}"
    elif len(str(minPrio)) == 2:
        minPrio = f"0{minPrio}"

    maxPrio = _max['priority']
    if len(str(maxPrio)) == 1:
        maxPrio = f"00{maxPrio}"
    elif len(str(maxPrio)) == 2:
        maxPrio = f"0{maxPrio}"

    minMsg = f"`{minPrio}` | `{minRank}` | {_min['name']}"
    maxMsg = f"`{maxPrio}` | `{maxRank}` | {_max['name']}"

    anotherArr.insert(0, minMsg)
    anotherArr.append(maxMsg)
    print(len(anotherArr))

    chunks = []
    while anotherArr:
        chunks.append(anotherArr[:20])
        anotherArr = anotherArr[20:]

    for chunk in chunks:
        try:
            await ctx.author.send("\n".join(chunk))
        except:
            await ctx.send("could not dm you the results, make sure you have dms enabled for this server.")
            break

    await ctx.send("task completed!")