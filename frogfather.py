# Import ?
import os
import json
import pprint
import random
import logging 

from pprint import pprint

import asyncio

# pip install beautifulsoup4
from bs4 import BeautifulSoup
# pip install -U discord.py    
import discord

from discord.ext import commands
from discord.ext.commands.core import before_invoke

# Import all files defined in __init__.py from the utilities folder
from utilities import *

# Import all files defined in __init__.py from the commands folder
from commands import *

# pip install python-dotenv
from dotenv import load_dotenv

from utilities import config
# Load the .env file
load_dotenv()
# Get a variable by it's name
token = os.getenv("TOKEN")


# Playing -> activity = discord.Game(name="!help")
# Streaming -> activity = discord.Streaming(name="!help", url="twitch_url_here")
# Listening -> activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
# Watching -> activity = discord.Activity(type=discord.ActivityType.watching, name="!help")
activity = discord.Game(
    name = f"{config.prefixes[0]}help"
)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix = config.prefixes,
    activity = activity, 
    status = discord.Status.dnd,
    intents = intents,
    help_command = None
)

#bot.remove_command('help')


async def logCmd(ctx, bot, args):

    log = 798411134877040671
    argsStr = " ".join(args)

    if ctx.guild != None:
        guildName = ctx.guild
        _id = ctx.guild.id
    else:
        guildName = "NA"
        _id = "NA"

    embed = discord.Embed(
        color = 0x2AF4C8,
        title = f"Command Used",
        description = f"**Command Used**: `{ctx.command}`\n**Args**:\n> {argsStr}\n**User**: <@{ctx.author.id}>\n**Guild Name**: {guildName}\n**Guild ID**: {_id}\n**Channel**: <#{ctx.channel.id}>"
    )

    await bot.get_channel(log).send(embed = embed)


async def cmdFail(ctx, bot, args):

    log = 798411134877040671
    argsStr = " ".join(args)

    embed = discord.Embed(
        color = 0xFF0000,
        title = f"Command Failed!",
        description = f"Command Used**: `{ctx.command}`\nArgs:\n> {argsStr}\nUser: <@{ctx.author.id}>\nServer: {ctx.guild}\nChannel: <#{ctx.channel.id}>\nReason for failuren> Coming soon.."
    )

    await bot.get_channel(log).send(embed = embed)




#Initiate the bot
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

    await bot.get_channel(791216444548579339).send("bot online")


@bot.event
async def on_message(message):

    # Reject other bots
    if message.author.bot == True:
        return

    # turn the message to lowercase before being processed as a command
    message.content = message.content.lower()

    # Process the message as a command, you must run this if ou want to use @bot.commands with the on message event
    await bot.process_commands(message)

@bot.command(
    enabled = True,
    hidden = True,
    name = "allservers"
)
async def _dev(ctx, *args):
    if ctx.author.id != 750304052184612865:
        return

    await ctx.message.delete()

    for guild in bot.guilds:
        pprint(guild.invites)

        if guild.icon != None:
            icon = guild.icon
        else:
            icon = "https://imgs.search.brave.com/Ap0sljFMHTsNO5kHX8ASpe0cJbd8IdvBd5PSCHKBnfo/rs:fit:1000:1000:1/g:ce/aHR0cHM6Ly9pY29u/LWxpYnJhcnkuY29t/L2ltYWdlcy9kaXNj/b3JkLWljb24tdGVt/cGxhdGUvZGlzY29y/ZC1pY29uLXRlbXBs/YXRlLTIwLmpwZw"

        guildOwner = bot.get_user(guild.owner_id)

        embed = discord.Embed(
            color = 0x307826,
            title = f"{guild.name}",
            description = f"Guild ID: {guild.id}\nMembers: {guild.member_count}\n\nServer Owner: {guildOwner.name}#{guildOwner.discriminator}\nServer Owner ID: {guild.owner_id}\nServer Owner Mention: <@{guildOwner.id}>"
        ).set_thumbnail(
            url = icon
        ).set_footer(
            text = f"Requested by {ctx.author}"
        )

        await bot.get_user(750304052184612865).send(embed = embed)

    await bot.get_user(750304052184612865).send(f"> Total Servers: {len(bot.guilds)}")

@bot.command(
    enabled = True,
    hidden = True,
    name = "leave"
)
async def _leave(ctx, *args):
    if ctx.author.id != 750304052184612865:
        return
    await ctx.message.delete()

    if len(args) == 1:
        if args[0].isdigit():
            leaveme = await bot.fetch_guild(args[0])
            await leaveme.leave()
            await bot.get_user(750304052184612865).send(f"Force left {leaveme.name}")





@bot.command(
    enabled = True,
    hidden = False,
    name = "wait",
    aliases = ["w", "remindme", "remind", "reme"],
    brief = "waits a time in minutes",
    usage = f"wait <time in minutes> <note>",
    help = f"Example:\n> {config.prefixes[0]}wait 45 beastmoon match ends"
)
async def _wait(ctx, *args):

    if args[0].isdigit():

        await ctx.message.delete()

        note = " ".join(args[1:])
        waitfor = (int(args[0]) - 5) * 60

        embed1 = discord.Embed(
            color = 0x307826,
            description = f"I will remind you in {int(args[0])} minutes\nNote:\n> {note}"
        ).set_footer(
            text = f"Requested by {ctx.author}",
            icon_url = ctx.author.avatar_url
        )
        sent1 = await ctx.send(embed = embed1)

        await asyncio.sleep(waitfor)

        await sent1.delete()
        embed2 = discord.Embed(
            color = 0x307826,
            description = f"5 minute warning\nNote:\n> {note}"
        ).set_footer(
            text = f"Requested by {ctx.author}",
            icon_url = ctx.author.avatar_url
        )
        sent2 = await ctx.send(f"<@{ctx.author.id}>", embed = embed2)

        await asyncio.sleep(60)

        await sent2.delete()
        embed3 = discord.Embed(
            color = 0x307826,
            description = f"4 minute warning\nNote:\n> {note}"
        ).set_footer(
            text = f"Requested by {ctx.author}",
            icon_url = ctx.author.avatar_url
        )
        sent3 = await ctx.send(embed = embed3)

        await asyncio.sleep(60)
        
        await sent3.delete()
        embed4 = discord.Embed(
            color = 0x307826,
            description = f"3 minute warning\nNote:\n> {note}"
        ).set_footer(
            text = f"Requested by {ctx.author}",
            icon_url = ctx.author.avatar_url
        )
        sent4 = await ctx.send(embed = embed4)

        await asyncio.sleep(60)

        await sent4.delete()
        embed5 = discord.Embed(
            color = 0x307826,
            description = f"2 minute warning\nNote:\n> {note}"
        ).set_footer(
            text = f"Requested by {ctx.author}",
            icon_url = ctx.author.avatar_url
        )
        sent5 = await ctx.send(embed = embed5)

        await asyncio.sleep(60)

        await sent5.delete()
        embed6 = discord.Embed(
            color = 0x307826,
            description = f"1 minute warning\nNote:\n> {note}"
        ).set_footer(
            text = f"Requested by {ctx.author}",
            icon_url = ctx.author.avatar_url
        )
        sent6 = await ctx.send(embed = embed6)

        await asyncio.sleep(60)
        
        await sent6.delete()
        embed7 = discord.Embed(
            color = 0x307826,
            description = f"Note:\n> {note}"
        ).set_footer(
            text = f"Requested by {ctx.author}",
            icon_url = ctx.author.avatar_url
        )
        await ctx.send(f"<@{ctx.author.id}>", embed = embed7)

    else:
        await ctx.send(f"{args[0]} is not a digit")

@bot.command(
    enabled = True,
    hidden = False,
    name = "help",
    #aliases = [],
    brief = "new help cmd"
)
async def _newHelp(ctx, *args):

    prefixes = ", ".join(config.prefixes)

    print(len(args))

    if len(args) == 0:

        embed = discord.Embed(
            title = ctx.author,
            color = await s.randomColour(),
            description = f"Bot Prefixes:\n> {prefixes.strip()}"
        )

        for cmd in bot.commands:

            if cmd.hidden == False:
                aliases = "`, `".join(cmd.aliases)
                embed.add_field(
                    name = f"`{cmd}`",
                    value = f"> {cmd.brief}\n> **Aliases**: `{aliases}`\n> Ex. {config.prefixes[0]}{cmd.usage}\nEnabled: {cmd.enabled}",
                    inline = False
                )
    
        await ctx.send(embed = embed)

    else:
        joint = " ".join(args)

        print(joint)
        for cmd in bot.commands:
            print(cmd.hidden)

            if cmd.name.lower() == joint.lower() and cmd.hidden == False:

                aliases = "`, `".join(cmd.aliases)

                embed = discord.Embed(
                    title = f"Help page for {cmd.name}",
                    color = await s.randomColour(),
                    description = f"> {cmd.brief}\n> **Aliases**: `{aliases}`\n> Ex. {cmd.usage}"
                )

                await ctx.send(embed = embed)
            # have to reformat this so that the embed isn't send in the loop. Have the loop return talents, if the found array or something len() is 0, then send couldnt find msg
           # else:
            #    await ctx.send(f"Could not find command called: `{joint}`")

@bot.command(
    enabled = True,
    hidden = False,
    name = "firstgen",
    aliases = ["fg"],
    usage = "fg <body name>",
    brief = "returns the first gen stats of a specific pet body",
    help = f"."
)
async def _firstGen(ctx, *args):

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

    desired = await processArgs(args)

    for des in desired:

        print(des)

        clone = des['content'].strip()

        split = clone.split(" ")

        exactArr = ["-e", "exact"]

        for x in split:

            print(x)

            if x in exactArr:

                index = desired.index(des)

                desired[index]['exact'] = True

                desired[index]['content'] = desired[index]['content'].replace(x, "")
 
    jsonFile = open("./bodyInfo/wiz.json")
    bodies = json.load(jsonFile)
    bodiesArr = bodies["pets"]

    talentsJson = open("./priorities/wiztalents.json")
    talentsDB = json.load(talentsJson)

    found = []

    for body in bodiesArr:

        for des in desired:
            content = des['content'].strip()

            if "'" in des:
                content = content.replace("'", "")

            if des['exact'] != True:

                if content.lower().strip() in body['name'].replace("'", "").lower():
                    found.append(body)

            else:

                if content.lower().strip() == body['name'].replace("'", "").lower():
                    found.append(body)

    if len(found) == 0:
        return await ctx.send(f"Found no matches")
    else:
        c = 1
        for body in found:

            # Find the talent info for the pet

            poolArr = []
            for talent in body['talents']:

                if "'" in talent:
                    talent = talent.replace("'", "")
                if "-" in talent:
                    talent = talent.replace("-", " ")
                if "." in talent:
                    talent = talent.replace(".", "")

                for talDB in talentsDB:

                    if "-" in talDB['name']:
                        talDB['name'] = talDB['name'].replace("-", " ")
                    if "." in talDB['name']:
                        talDB['name'] = talDB['name'].replace(".", "")

                    if talDB['name'].replace("'", "").lower() == talent.lower():

                        tal = {
                            "name": talDB['name'],
                            "rank": talDB["rank"],
                            "url": talDB["url"],
                            "valid_url": talDB["valid_url"],
                            "locked": talDB["locked"],
                            "priority": talentsDB.index(talDB)
                        }

                        poolArr.append(tal)

            poolArr = sorted(poolArr, key = lambda x : x["priority"])

            # Process the talents in to a message
            talentsArray = []
            for talent in poolArr:
                

                name = talent["name"]
                url = talent["url"]
                urlCheck = talent["valid_url"]

                if urlCheck == True:
                    name = f"[{name}]({url})"
        

                #print(len(str(priority)))


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



                #if talent["name"].lower() 

                unlocked = ""

                unlockables = ["finder", "hunter", "scout", "farmer", "trained", "track r treater", "elemental retriever", "hatch catcher"]

                for u in unlockables:
                    #print(u)
                    #print(name.lower())
                    if u in name.lower():
                        #print("match!!!")

                        if talent["locked"] == True:
                            #print("true!")
                            unlocked = " | Locked"
                        elif talent["locked"] == False:
                            #print("false!")
                            unlocked = " | Unlocked"
                        else:
                            print("this shouldnt happen ever")
                    #else:
                    #    unlocked = "NA"

                talentMsg = f"`{priority}` | `{rank}` | {name}{unlocked}"
                talentsArray.append(talentMsg)

            pool = "\n> ".join(talentsArray)

            print(body['max_stats']['strength'])

            statsMsg = f"**Stats**:\n> {body['max_stats']['strength']} <:Icon_Strength:802528770296250378>\n> {body['max_stats']['intellect']} <:Icon_Intellect:802528770362966046>\n> {body['max_stats']['agility']} <:Icon_Agility:802528770166620192>\n> {body['max_stats']['will']} <:Icon_Will:802528770358771732>\n> {body['max_stats']['power']} <:Icon_Power:802528770492858378>"
            
            wikiUrl = f'http://www.wizard101central.com/wiki/Pet:{body["name"].replace(" ", "_")}'

            #page = requests.get(wikiUrl)

            #soup = BeautifulSoup(page.content, "html.parser")

            #results = soup.find(id="mw-content-text")

            # ????
            #print(soup)

            #pprint(body['derby_talents'])

            #mainPed = await s.getPedigree(poolArr)
            #derbyPed = await s.getPedigree(body['derby_talents'])

            #pedigree = mainPed + derbyPed

            embed = discord.Embed(
                title = f"First Gen {body['name']} Info",
                description = f"{statsMsg}\n\n**Pool**:\n> {pool}",
                color = await s.randomColour(),
                url = wikiUrl
            ).set_footer(
                text = f"Requested by {ctx.author} | Item {c} of {len(found)}."
            )
            c += 1
            await ctx.send(embed = embed)

@bot.command(
    enabled = True,
    hidden = False,
    name = "compare",
    aliases = ["comp"],
    usage = "<body name>, <body name>, etc",
    brief = "seperate each body name with a comma",
    help = f"searches for information on specific bodies by name.\n**Example**:\n> {config.prefixes[0]}fbn marshfellow, hamster\nWill return information on the Marshfellow body and any body with \"hamster\" in their name."
)
async def _compare(ctx, *args):

    try:
        await compare.start(json, discord, ctx, bot, args)
    except:
        await cmdFail(ctx, bot, args)
        logging.exception('')
    else:
        await logCmd(ctx, bot, args)


@bot.command(
    enabled = True,
    hidden = False,
    name = "talentsearch",
    aliases = ["ts", "talents"],
    usage = "<talent name>, <talent name>, etc",
    brief = "seperate each talent name with a comma",
    help = f"searches for data on one or more specific talents. Seperate each talent name with a comma.\n**Example**:\n> {config.prefixes[0]}search death dealer, spell-defying, giver\nWill return Death Dealer, Spell Defying, and all talents with the word \"giver\" in their name."
)
async def _search(ctx, *args):

    try:
        await talentSearch.main(ctx, bot, args)
    except:
        await cmdFail(ctx, bot, args)
        logging.exception('')
    else:
        await logCmd(ctx, bot, args)
 

@bot.command(
    enabled = True,
    hidden = False,
    name = "talentsbetween",
    aliases = ["tb", "between"],
    usage = "tb <talent 1>, <talent 2>, <rank>",
    brief = "searches for talents between two talents or priorities, rank is optional. If you input either a digit or \"top\" or \"bottom\" it will use the talent with that priority",
    help = "Searches for talents between two pre determined talents. Rank is optional.\n **Example**:\n> t?tb spell proof, spell defying, ur"
)
async def _talentsbetween(ctx, *args):

    try:
        await talentsBetween.main(ctx, bot, args)
    except:
        await cmdFail(ctx, bot, args)
    else:
        await logCmd(ctx, bot, args)


@bot.command(
    enabled = False,
    hidden = True,
    name = "findmatching",
    aliases = ["fm"],
    usage = "fm <rarity> <wow factor>",
    brief = "searches for all pets that have the desired rarity and wow factor",
    help = "Searches for all pets that have the desired rarity and wow factor.\n **Example**:\n> t?fm 3 9\n> t?fm commom 5"
)
async def _findMatching(ctx, *args):

    jsonFile = open("./utilities/petdata.json")
    bodies = json.load(jsonFile)
    bodiesArr = bodies["pets"]

    rarities = ["common", "c", "uncommon", "uc", "rare", "r", "ultra rare", "ur", "epic", "e"]

    found = []

    if len(args) != 2:
        return await ctx.send("invalid number of args, please provide 2. One for wow factor, one for rarity")

    for arg in args:

        if "-" in arg:
            arg = arg.replace("-", "")
        if "," in arg:
            arg = arg.replace(",", "")

    commonArr = ["c", "0", "common"]
    uncommonArr = ["uc", "1", "uncommon"]
    rareArr = ["r", "2", "rare"]
    ultraRareArr = ["ur", "3", "ultra rare"]
    epicArr = ["e", "4", "epic"]

    if args[1].isdigit():
        desiredWow = int(args[1])
    else:
        return await ctx.send(f"Invalid wow factor:\n> {args[1]}")


    desiredRarity = args[0]


    if desiredRarity.lower() in commonArr:
        desiredRarity = "common"
    elif desiredRarity.lower() in uncommonArr:
        desiredRarity = "uncommon"
    elif desiredRarity.lower() in rareArr:
        desiredRarity = "rare"
    elif desiredRarity.lower() in ultraRareArr:
        desiredRarity = "ultra-rare"
    elif desiredRarity.lower() in epicArr:
        desiredRarity = "epic"
    else:
        return await ctx.send(f"Invalid rarity:\n> {args[0]}")

    colour = await s.randomColour()

    for body in bodiesArr:

        if int(body["wow_factor"]) == desiredWow and body["rarity"].lower() == desiredRarity:

            found.append(body)

    embed = discord.Embed(
        title = ctx.author,
        color = colour
    ).set_footer(
        text = f"Returned {len(found)} bodies"
    )

    for body in found:
        name = body["name"]
        rarity = body["rarity"]
        wow = body["wow_factor"]
        msg = f"Rarity: {rarity}\nWow: {wow}"

        embed.add_field(
            name = name,
            value = msg
        )

    await ctx.send(embed = embed)


@bot.command(
    enabled = True,
    hidden = False,
    name = "wowfactor",
    aliases = ["wf"],
    usage = "wf <wow factor>",
    brief = "searches for all pets that have the desired wow factor",
    help = "Searches for and returns all pets that have the wow factor.\n **Example**:\n> t?fm 5"
)
async def _wowFactor(ctx, *args):

    jsonFile = open("./bodyInfo/wiz.json")
    bodies = json.load(jsonFile)
    bodiesArr = bodies["pets"]

    found = []

    if len(args) != 1:
        return await ctx.send("invalid number of args, please provide 1 for wow factor")

    if args[0].isdigit():
        desiredWow = int(args[0])
    else:
        return await ctx.send(f"Invalid wow factor:\n> {args[0]}")

    colour = await s.randomColour()

    for body in bodiesArr:

        if int(body["wow_factor"]) == desiredWow:

            found.append(body)

    chunks = []
    foundNum = len(found)
    
    while found:
        chunks.append(found[:9])
        found = found[9:]

    if len(chunks) == 1:

        embed = discord.Embed(
            title = ctx.author,
            color = colour
        ).set_footer(
            text = f"Returned {foundNum} bodies"
        )

        for body in chunks[0]:
            name = body["name"]
            wow = body["wow_factor"]
            egg = body["egg_name"]
            msg = f"Wow Factor: {wow}\nEgg Type: {egg}"

            embed.add_field(
                name = name,
                value = msg
            )

        await ctx.send(embed = embed)

    else:


        await ctx.send(f"Found {foundNum} bodies, please wait.")
        await asyncio.sleep(1)


        for chunk in chunks:

            embed = discord.Embed(
                title = ctx.author,
                color = colour
            )

            for body in chunk:
                name = body["name"]
                wow = body["wow_factor"]
                egg = body["egg_name"]
                msg = f"Wow Factor: {wow}\nEgg Type: {egg}"

                embed.add_field(
                    name = name,
                    value = msg
                )

            await ctx.send(embed = embed)

    print("done")

@bot.command(
    enabled = True,
    hidden = False,
    name = "returnchance",
    aliases = ["rech", "rc"],
    usage = "body 1, body 2 | wf1 wf2",
    help = "Returns the chance to get each body during a hatch",
    brief = "Returns the chance to get each body during a hatch"
)
async def _re(ctx, *args):

    try:
        await returnChance.start(json, bot, args, ctx)
    except Exception as e:
        await s.cmdFail(discord, ctx, bot, args)
        logging.exception('')
        print(e)
    else:
        await s.logCmd(discord, ctx, bot, args)

# Start the bot
bot.run(token)