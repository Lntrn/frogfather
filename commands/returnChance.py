async def start(json, bot, args, ctx):
    jsonFile = open("./utilities/bodydata.json")
    bodies = json.load(jsonFile)
    bodiesArr = bodies["pets"]
    allDigits = True
    for ar in args:
        if not ar.replace(",", "").isdigit():
            allDigits = False
            print(ar)
    
    if allDigits == True:
        if len(args) != 2:
            return await ctx.send("You must provide two wow factors.")

        wf1 = int(args[0].replace(",", ""))
        wf2 = int(args[1].replace(",", ""))
        percentage1 = await math(wf1, wf2)
        percentage2 = await math(wf2, wf1)
        return await ctx.send(f"> Wow Factor: {wf1}\n> Return Chance: {round(percentage1, 2)}%\n\n\n> Wow Factor: {wf2}\n> Return Chance: {round(percentage2, 2)}%")

    if args[0].lower().strip() == "formula":
        return await ctx.send("`100*(11 - wf1)/(22 - (wf1 + wf2)) = % chance to get wf1 body`")

    joint = " ".join(args)
    desired = joint.split(",")
    if len(desired) != 2:
        return await ctx.send("invalid input")

    for d in desired:
        if "'" in d:
            d = d.replace("'", "")

    found = []
    foundNames = []
    breaker = False
    for body in bodiesArr:
        for des in desired:
            if body['name'].replace("'", "").lower() == des.lower().strip():
                if body['name'].lower().strip() not in foundNames:
                    found.append(body)
                    foundNames.append(body['name'].lower().strip())

                print(des.lower().strip())
                print(f"Matched {body['name']}")
                if len(found) == 2:
                    breaker = True
                    break

        if breaker == True:
            print("BREAKING")
            break

    print(len(found))
    foundBody1, foundBody2 = found
    percentage1 = await math(foundBody1['wow_factor'], foundBody2['wow_factor'])
    percentage2 = await math(foundBody2['wow_factor'], foundBody1['wow_factor'])
    await ctx.send(f"**{foundBody1['name']}**\n> Wow Factor: {foundBody1['wow_factor']}\n> Return Chance: {round(percentage1, 2)}%\n\n**{foundBody2['name']}**\n> Wow Factor: {foundBody2['wow_factor']}\n> Return Chance: {round(percentage2, 2)}%")

async def math (wf1, wf2):
    return 100*(11 - wf1)/(22 - (wf1 + wf2))