# Import all files defined in __init__.py from the utilities folder
from utilities import *

async def start(json, discord, ctx, bot, args):
    desired = await s.processArgs(args)
    print(len(desired))
    for des in desired:
        #print(des)
        clone = des['content'].strip()
        split = clone.split(" ")
        exactArr = ["-e", "exact"]
        for x in split:
            if x in exactArr:
                index = desired.index(des)
                desired[index]['exact'] = True
                desired[index]['content'] = desired[index]['content'].replace(x, "")

    await cmd(json, discord, ctx, bot, desired)

async def cmd(json, discord, ctx, bot, desired):    
    jsonFile = open("./utilities/newbodydata.json")
    bodiesArr = json.load(jsonFile)
    #bodiesArr = bodies["pets"]
    found = [] 
    for body in bodiesArr:
        for des in desired:
            #print(des['content'])
            content = des['content'].strip()
            if "'" in des:
                content = content.replace("'", "")

            if des['exact'] != True:
                if content.lower().strip() in body['name'].replace("'", "").lower():
                    found.append(body)

            else:
                if content.lower().strip() == body['name'].replace("'", "").lower():
                    found.append(body)

    found = sorted(found, key = lambda x : x["wow_factor"], reverse = True)
    returned = len(found)
    chunks = []
    while found:
        chunks.append(found[:10])
        found = found[10:]

    if len(chunks) < 25:
        await ctx.send(f"Found {returned} matches, please wait.")
        colour = await s.randomColour()
        embed = discord.Embed(
            title = ctx.author,
            color = colour
        ).set_footer(
            text = f"Returned {returned} bodies"
        )
        for chunk in chunks:
            msgArr = []
            for body in chunk:
                print(body["wow_factor"])
                if body['wow_factor'] == 1:
                    wow = "` 1`"
                elif body['wow_factor'] == 2:
                    wow = "` 2`"
                elif body['wow_factor'] == 3:
                    wow = "` 3`"
                elif body['wow_factor'] == 4:
                    wow = "` 4`"
                elif body['wow_factor'] == 5:
                    wow = "` 5`"
                elif body['wow_factor'] == 6:
                    wow = "` 6`"
                elif body['wow_factor'] == 7:
                    wow = "` 7`"
                elif body['wow_factor'] == 8:
                    wow = "` 8`"
                elif body['wow_factor'] == 9:
                    wow = "` 9`"
                elif body['wow_factor'] == 10:
                    wow = "`10`"
                
                egg = body['egg_name']
                if body['exclusive'] == "True":
                    msgArr.append(f"> {wow} | {body['name']} | {egg} | **Exclusive**")
                else:
                    msgArr.append(f"> {wow} | {body['name']} | {egg}")

            embed.add_field(
                name = "Wow Factor | Name | Egg Type",
                value = "\n".join(msgArr),
                inline = False
            )

        await ctx.send(embed = embed)

    else: 
        await ctx.send(f"Found {returned} matches, please wait.")
        await ctx.author.send(f"Found {returned} matches, please wait.")
        for chunk in chunks:
            msgArr = []
            for body in chunk:
                print(body)
                if body['wow_factor'] == 1:
                    wow = "` 1`"
                elif body['wow_factor'] == 2:
                    wow = "` 2`"
                elif body['wow_factor'] == 3:
                    wow = "` 3`"
                elif body['wow_factor'] == 4:
                    wow = "` 4`"
                elif body['wow_factor'] == 5:
                    wow = "` 5`"
                elif body['wow_factor'] == 6:
                    wow = "` 6`"
                elif body['wow_factor'] == 7:
                    wow = "` 7`"
                elif body['wow_factor'] == 8:
                    wow = "` 8`"
                elif body['wow_factor'] == 9:
                    wow = "` 9`"
                elif body['wow_factor'] == 10:
                    wow = "`10`"

                egg = body['egg_name']
                if body['exclusive'] == "True":
                    msgArr.append(f"> {wow} | {body['name']} | {egg} | **is Exclusive")
                else:
                    msgArr.append(f"> {wow} | {body['name']} |  {egg}")
                    
            try:
                await ctx.author.send("\n".join(msgArr))
            except:
                await ctx.send("cannot dm you, make sure they are enabled in a server we have in common")
                break

        await ctx.send(f"task completed. check your dms.")