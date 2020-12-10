from subprocess import PIPE, Popen
from re import search, compile
from threading import Thread
from multiprocessing import Process
import time
from sys import platform
from os.path import isfile
import discord
from json import dumps

import pip
import uuid


def pinstall(package):
    pip.main(['install', package])


try:
    from mcuuid import mcuuid
except:
    pinstall("mcuuid")
    from mcuuid import mcuuid

try:
    from discord_webhook import *
except:
    pinstall("discord_webhook")
    from discord_webhook import *


def getUUID(Username):
    return str(uuid.UUID(mcuuid.GetPlayerData(Username).uuid))

def listString(x):
    try:
        xLen = len(x)
        rtnstr = ""
        for i in range(xLen-1):
            rtnstr += x[i] + ", "
        return rtnstr + x[xLen-1]
    except:
        return ""


def serverCommand(process, text):
    args = text.split(" ")
    if len(args) >= 3 and [args[0], args[1], args[2]] == ["tell", "the", "server"]:
        print(text[16:])
    else:
        global serverLoaded
        process.stdin.write((text+"\n").encode())
        if serverLoaded:
            process.stdin.flush()


def rewriteOps():
    global ops
    opsFile = open("ops.txt", "w+")
    for i in ops:
        if i != "the server":
            opsFile.write(i+"\n")
    opsFile.close()


def customCommand(process, command, player="the server"):
    global serverRestarts, serverLoaded

    args = command.split(" ")

    if args[0] == "seed":
        # minecraftjson.com
        #{"jformat":6,"jobject":[{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"none","insertion":"","click_event_type":0,"click_event_value":"","hover_event_type":0,"hover_event_value":"","hover_event_object":{},"hover_event_children":[],"id":"221e4bb0-9da9-40f9-b263-d7d4038f82dc","text":"Seed: ["},{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"green","insertion":"","click_event_type":"5","click_event_value":"51109066175183","hover_event_type":"1","hover_event_value":"","hover_event_object":{},"hover_event_children":[{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"none","insertion":"","click_event_type":0,"click_event_value":"","hover_event_type":0,"hover_event_value":"","hover_event_object":{},"hover_event_children":[],"id":"c5465ff7-8419-406b-a3d7-a2826df00a18","text":"Click to Copy to Clipboard"}],"id":"9e517b3b-d072-4ace-a074-d5ff729bcf9c","text":"51109066175183"},{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"none","insertion":"","click_event_type":0,"click_event_value":"","hover_event_type":0,"hover_event_value":"","hover_event_object":{},"hover_event_children":[],"id":"52be9410-07e4-4172-8887-81189f98f24e","text":"]"}],"command":"tellraw @a %s","jtemplate":"tellraw"}
        serverCommand(process, "tellraw @a [\"\",{\"text\":\"Seed: [\"},{\"text\":\"51109066175183\",\"color\":\"green\",\"clickEvent\":{\"action\":\"copy_to_clipboard\",\"value\":\"51109066175183\"},\"hoverEvent\":{\"action\":\"show_text\",\"contents\":{\"text\":\"Click to Copy to Clipboard\"}}},{\"text\":\"]\"}]")
    elif args[0] == "help":
        # https://pastebin.com/raw/LbiSVzQu
        # minecraftjson.com
        #{"jformat":6,"jobject":[{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"none","insertion":"","click_event_type":0,"click_event_value":"","hover_event_type":0,"hover_event_value":"","hover_event_object":{},"hover_event_children":[],"id":"475cb068-cad5-480b-8e25-8278bf39d877","text":"Help: ["},{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"green","insertion":"","click_event_type":"1","click_event_value":"https://pastebin.com/raw/LbiSVzQu","hover_event_type":"1","hover_event_value":"","hover_event_object":{},"hover_event_children":[{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"none","insertion":"","click_event_type":0,"click_event_value":"","hover_event_type":0,"hover_event_value":"","hover_event_object":{},"hover_event_children":[],"id":"c360123b-d3aa-4bef-b0d9-b8357ea37bdc","text":"Click to Open Link"}],"id":"f075467e-18e3-492f-9c76-1523b42b941c","text":"Command List"},{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"none","insertion":"","click_event_type":0,"click_event_value":"","hover_event_type":0,"hover_event_value":"","hover_event_object":{},"hover_event_children":[],"id":"c16eea83-be6a-4095-be6d-11d1ec104069","text":"]"}],"command":"tellraw @a %s","jtemplate":"tellraw"}
        serverCommand(process, "tellraw @a [\"\",{\"text\":\"Help: [\"},{\"text\":\"Command List\",\"color\":\"green\",\"clickEvent\":{\"action\":\"open_url\",\"value\":\"https:\/\/pastebin.com\/raw\/LbiSVzQu\"},\"hoverEvent\":{\"action\":\"show_text\",\"contents\":{\"text\":\"Click to Open Link\"}}},{\"text\":\"]\"}]")
    elif args[0] == "clear":
        serverCommand(process, "tellraw @a \""+"\\n"*500+"\"")
    elif args[0] == "shadow":
        if len(args) == 1:
            serverCommand(process, "player "+player+" shadow")
        elif len(args) == 2:
            serverCommand(process, "tell "+player +
                          " Invalid arguments! Type !help for help.")
        elif len(args) == 3:
            if args[1] in ["attack", "use"]:
                try:
                    interval = int(args[2])
                    if interval < 2:
                        serverCommand(process, "tell "+player +
                                      " Interval must be an integer above 1!")
                    else:
                        serverCommand(process, "player "+player+" shadow")
                        serverCommand(process, "player "+player +
                                      " "+args[1]+" interval "+str(interval))
                except:
                    serverCommand(process, "tell "+player +
                                  " Interval must be an integer above 1!")

            else:
                serverCommand(process, "tell "+player +
                              " Invalid arguments! Type !help for help.")
    elif args[0] in ["restart", "stop"]:
        if player.lower() in ops:
            serverCommand(process, "say Server Restarting in 3...")
            time.sleep(1)
            serverCommand(process, "say Server Restarting in 2...")
            time.sleep(1)
            serverCommand(process, "say Server Restarting in 1...")
            time.sleep(1)
            serverCommand(process, "stop")
            serverLoaded = False
        else:
            serverCommand(process, "tell "+player +
                          " You don't have permission!")
    elif args[0] == "fullstop":
        if player.lower() in ops:
            serverRestarts = False
            serverCommand(process, "say Ending server")
            serverCommand(process, "stop")
            serverLoaded = False
            DiscordWebhook(url=DiscordWebhookURL,content="Server host has been stopped.",username="Server Hoster").execute()
        else:
            serverCommand(process, "tell "+player +
                          " You don't have permission!")
    elif args[0] == "killserver":
        if player.lower() in ops:
            serverRestarts = False
            serverLoaded = False
            process.kill()
            process.terminate()
        else:
            serverCommand(process, "tell "+player +
                          " You don't have permission!")
    elif args[0] == "ops":
        if player.lower() in ops:
            if len(args) == 2 and args[1] == "list":
                opsString = ""
                for i in ops:
                    if i != "the server":
                        opsString += ", " + i
                serverCommand(process, "tell "+player +
                              " Server Manager Operators: "+opsString[2:])
            elif len(args) == 3:
                args[2] = args[2].lower()
                if args[1] == "remove":
                    serverCommand(process, "tell "+player+" Removing '" +
                                  args[2]+"' from server manager operators.")
                    try:
                        ops.remove(args[2])
                        rewriteOps()
                    except:
                        serverCommand(process, "tell "+player +
                                      " Player is not a server manager operator.")

                elif args[1] == "add":
                    if args[2] in ops:
                        serverCommand(process, "tell "+player +
                                      " Player already a server manager operator.")
                    else:
                        serverCommand(
                            process, "tell "+player+" Adding '"+args[2]+"' to server manager operators.")
                        ops.append(args[2])
                        rewriteOps()
                else:
                    serverCommand(process, "tell "+player +
                                  " Invalid arguments! Type !help for help.")
            else:
                serverCommand(process, "tell "+player +
                              " Invalid arguments! Type !help for help.")
        else:
            serverCommand(process, "tell "+player +
                          " You don't have permission!")
    else:
        serverCommand(process, "tell "+player+" Invalid command.")


def getServer():
    global mcServer
    return mcServer


def consoleInput():
    global serverLoaded, updatePlayerList
    process = getServer()
    while True:
        inp = input()
        process = getServer()
        if process != None and process.poll() == None:
            if serverLoaded:
                if inp == "fullstop":
                    print("[Server Hoster] Executing fullstop")
                    customCommand(process, "fullstop")
                elif inp[:4] == "list":
                    playerListUpdate()
                    print("Players: ",end="")
                    if len(playerList) == 1:
                        if playerList[0] == "":
                            print("Nobody Online")
                        else:
                            print(playerList[0])
                    else:
                        print(listString(playerList))

                elif inp.split(" ")[0] == "ops":
                    customCommand(process, inp)
                elif inp == "killserver":
                    customCommand(process, inp)
                else:
                    serverCommand(process, inp)
            else:
                print("[Server Hoster] Server not yet loaded")
        else:
            if not serverRestarts:
                exit()
            print("[Server Hoster] No server process")


def consoleOutput():
    global serverRestarts, serverLoaded, hasDiscord, playerList, updatePlayerList
    # Credit to Miniaczq for help with Regex (I forced him to help by using the plagiarism technique)
    playerComReg = compile(
        r'\[..:..:..\] \[Server thread/INFO\]: <.*?> !.*?').search
    playerReg = compile(
        r'\[..:..:..\] \[Server thread/INFO\]: <.*?> .*?').search
    stopReg = compile(
        r'\[..:..:..\] \[Server thread/INFO\]: Stopping server').search
    listReg = compile(
        r'\[..:..:..\] \[Server thread/INFO\]: .*? players online:.*?').search
    doneReg = compile(r'\[..:..:..\] \[Server thread/INFO\]: Done').search
    process = getServer()
    while True:
        if process != None and process.poll() == None:
            for line in process.stdout:
                if islinux:
                    # Interpret Linux
                    line = str(line)
                    line = line[2:len(line)-3]
                else:
                    # Interpret Windows (unknown function for mac)
                    line = str(line.rstrip())[2:len(line)]
                if listReg(line):
                    playerList = line[line.index("online:")+8:].split(", ")
                    updatePlayerList = False
                else:
                    print(line)
                if playerReg(line):
                    if(hasDiscord):
                        if (not playerComReg(line)) or "!clear" in line[line.index(">")+2:]:
                            discordMessageQueue.append(
                                [line[line.index(">")+2:], line[line.index("<")+1:line.index(">")]])
                    if playerComReg(line):
                        customCommand(process, line[line.index(
                            ">")+3:], line[line.index("<")+1:line.index(">")])
                if stopReg(line):
                    serverLoaded = False
                    if hasDiscord:
                        DiscordWebhook(url=DiscordWebhookURL,content="Server has stopped.",username="Server Hoster").execute()
                if doneReg(line):
                    print("[Server Hoster] Server is now loaded; ready for inputs.")
                    serverLoaded = True
                    process.stdin.flush()
                    if hasDiscord:
                        DiscordWebhook(url=DiscordWebhookURL,content="Server has loaded.",username="Server Hoster").execute()

        else:
            if not serverRestarts:
                exit()
            process = getServer()
            time.sleep(2)


class ReaderBot(discord.Client):
    global discordChannel

    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message):
        if message.channel.id == int(discordChannel):
            content = str(message.content)

            if content == "!list":
                if serverLoaded:
                    playerList = playerListUpdate()
                    print("Got player list")
                    if playerList[0] == "":
                        totalPlayers = 0
                    else:
                        totalPlayers = len(playerList)

                    DiscordWebhook(url=DiscordWebhookURL,content="Players Online ("+str(totalPlayers)+"): "+listString(playerList),username="Server Hoster").execute()
                else:
                    DiscordWebhook(url=DiscordWebhookURL,content="Server currently not loaded.",username="Server Hoster").execute()
            else:
                if not message.author.bot:                
                    if serverLoaded:
                        player = str(message.author)
                        player = player[:len(player)-5]
                        serverCommand(
                            getServer(), "tellraw @a \"[Discord] <"+player+"> "+dumps(content)[1:])
                    else:
                        DiscordWebhook(url=DiscordWebhookURL,content="Server currently not loaded.",username="Server Hoster").execute()
                if content[:6] == "!clear":
                    if not message.author.bot:
                        customCommand(getServer(),"clear")
                    messages = await message.channel.history().flatten()
                    for i in messages:
                        await i.delete()

                if content == "Server host has been stopped." and message.author.bot and str(message.author) == "Server Hoster#0000":
                    await self.close()


def discordProcessing(discordMessageQueue, DiscordWebhookURL):
    global serverRestarts, serverLoaded, discordInfo
    while serverRestarts:
        time.sleep(0.1)
        while len(discordMessageQueue) > 0:
            player = discordMessageQueue[0][1]
            message = discordMessageQueue[0][0]
            discordMessageQueue.remove(discordMessageQueue[0])
            DiscordWebhook(url=DiscordWebhookURL,
                           content=message, username=player, avatar_url="https://crafatar.com/renders/head/"+getUUID(player)+"?overlay").execute()


def serverRestarter():
    global serverRestarts, serverLoaded, mcServer
    while serverRestarts:
        if platform in ["win32", "win64"]:
            mcServer = Popen(popenCommand, cwd="server", stdin=PIPE,
                             stdout=PIPE, stderr=PIPE, close_fds=True)
        elif islinux:
            mcServer = Popen(["/bin/bash", "-c", popenCommand], cwd="server",
                             stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)

        while mcServer.poll() == None:
            time.sleep(0.1)
    exit()


def playerListUpdate():
    global playerList, updatePlayerList
    updatePlayerList = True
    while updatePlayerList:
        time.sleep(0.1)
    return playerList


def playerListHandler():
    global serverRestarts, serverLoaded, updatePlayerList
    while serverRestarts:
        while not updatePlayerList:
            time.sleep(0.1)
            if not serverRestarts:
                exit()
        serverCommand(getServer(),"list")
        time.sleep(0.1)

if __name__ == '__main__':
    islinux = platform == "linux"
    if islinux:
        print("[Server Hoster] Linux detected.")
    ops = ["the server"]
    try:
        opsFile = open("ops.txt", "r")
        opsFileText = opsFile.read()
        opsFile.close()
        for i in opsFileText.split("\n"):
            if i != "":
                print("[Server Hoster] OP Loaded: "+i)
                ops.append(i.lower())
    except:
        opsFile = open("ops.txt", "w+")
        opsFile.write(
            "Enter OPS here, with a new line in between each player (Replace this line)")
        opsFile.close()

    popenCommand = "java -jar server.jar nogui"
    try:
        runFile = open("run.txt", "r")
        popenCommand = runFile.read()
        runFile.close()
    except:
        runFile = open("run.txt", "w+")
        runFile.write(popenCommand)
        runFile.close()

    serverRestarts = True
    mcServer = None
    serverLoaded = False
    playerList = [""]
    updatePlayerList = False

    consoleInputProcessing = Thread(target=consoleInput, args=[])
    consoleInputProcessing.start()

    consoleOutputThread = Thread(target=consoleOutput, args=[])
    consoleOutputThread.start()

    playerListHandlerThread = Thread(target=playerListHandler,args=[])
    playerListHandlerThread.start()

    hasDiscord = False
    if isfile("discord.txt"):
        hasDiscord = True

        discordInfoFile = open("discord.txt", "r")
        discordInfo = discordInfoFile.read().split("\n")
        discordInfoFile.close()

        for i in discordInfo:
            i = i.split("=")
            if(i[0] == "webhook"):
                DiscordWebhookURL = i[1]
            elif(i[0] == "channel"):
                discordChannel = i[1]
            elif(i[0] == "token"):
                discordToken = i[1]

        discordMessageQueue = []
        discordProcessingThread = Thread(
            target=discordProcessing, args=[discordMessageQueue, DiscordWebhookURL])
        discordProcessingThread.start()

        discordBot = ReaderBot()
        DiscordWebhook(url=DiscordWebhookURL,content="Server host has started.",username="Server Hoster").execute()
    
    serverRestarterThread = Thread(target=serverRestarter,args=[])
    serverRestarterThread.start()

    if hasDiscord:
        discordBot.run(discordToken)

    while mcServer.poll() == None:
        time.sleep(0.1)

    if hasDiscord:
        DiscordWebhook(url=DiscordWebhookURL,content="Server host has finished shutting down.",username="Server Hoster").execute()
    print("[Server Hoster] Enter to exit...")