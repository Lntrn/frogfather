import random

async def randomColour():
    colours = [0x4dff58, 0x9740dd, 0x3455f9, 0xec7a22, 0x5dfdf3, 0xff0000, 0x3a2848, 0x3f798d, 0x86a15e, 0xabff66, 0xfbff14, 0x9fa073, 0x235333, 0x010698, 0xff00d4, 0x8c184c, 0x000000, 0x5865F2, 0x2f3136]
    return 0x307826 #random.choice(colours)

async def processArgs(args):
    joint = " ".join(args)
    split = joint.split(",")
    data = []
    for x in split:
        d = {
            "content": x.strip(),
            "exact": False
        }
        data.append(d)

    return data

async def cmdFail(discord, ctx, bot, args):
    log = 798411134877040671
    argsStr = " ".join(args)
    embed = discord.Embed(
        color = 0xFF0000,
        title = f"Command Failed!",
        description = f"Command Used**: `{ctx.command}`\nArgs:\n> {argsStr}\nUser: <@{ctx.author.id}>\nServer: {ctx.guild}\nChannel: <#{ctx.channel.id}>\nReason for failuren> Coming soon.."
    )
    await bot.get_channel(log).send(embed = embed)

async def logCmd(discord, ctx, bot, args):
    log = 798411134877040671
    argsStr = " ".join(args)
    embed = discord.Embed(
        color = 0x2AF4C8,
        title = f"Command Used",
        description = f"**Command Used**: `{ctx.command}`\n**Args**:\n> {argsStr}\n**User**: <@{ctx.author.id}>\n**Guild Name**: {ctx.guild}\n**Guild ID**: {ctx.guild.id}\n**Channel**: <#{ctx.channel.id}>"
    )


async def getPedigree(pool):
    pedigree = 0
    for talent in pool:
        print(talent)
        if talent['rank'] == "Common":
            pedigree += 1
        elif talent['rank'] == "Uncommon":
            pedigree += 2
        elif talent['rank'] == "Rare":
            pedigree += 3
        elif talent['rank'] == "Ultra Rare":
            pedigree += 4
        elif talent['rank'] == "Epic":
            pedigree += 5
    return pedigree