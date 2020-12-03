from subprocess import PIPE, Popen
from re import search, compile
from threading import Thread
from multiprocessing import Process
from os.path import isfile
import time

def serverCommand(process,text):
    args = text.split(" ")
    if len(args) >= 3 and [args[0],args[1],args[2]] == ["tell","the","server"]:
        print(text[16:])
    else:
        global ServerLoaded
        process.stdin.write((text+"\n").encode())
        if ServerLoaded:
            process.stdin.flush()

def rewriteOps():
    global ops
    opsFile = open("ops.txt","w+")
    for i in ops:
        if i != "the server":
                opsFile.write(i+"\n")
    opsFile.close()

def customCommand(process,command,player="the server"):
    global ServerRestarts, ServerLoaded

    args = command.split(" ")

    if args[0] == "seed":
        #minecraftjson.com
        #{"jformat":6,"jobject":[{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"none","insertion":"","click_event_type":0,"click_event_value":"","hover_event_type":0,"hover_event_value":"","hover_event_object":{},"hover_event_children":[],"id":"221e4bb0-9da9-40f9-b263-d7d4038f82dc","text":"Seed: ["},{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"green","insertion":"","click_event_type":"5","click_event_value":"51109066175183","hover_event_type":"1","hover_event_value":"","hover_event_object":{},"hover_event_children":[{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"none","insertion":"","click_event_type":0,"click_event_value":"","hover_event_type":0,"hover_event_value":"","hover_event_object":{},"hover_event_children":[],"id":"c5465ff7-8419-406b-a3d7-a2826df00a18","text":"Click to Copy to Clipboard"}],"id":"9e517b3b-d072-4ace-a074-d5ff729bcf9c","text":"51109066175183"},{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"none","insertion":"","click_event_type":0,"click_event_value":"","hover_event_type":0,"hover_event_value":"","hover_event_object":{},"hover_event_children":[],"id":"52be9410-07e4-4172-8887-81189f98f24e","text":"]"}],"command":"tellraw @a %s","jtemplate":"tellraw"}
        serverCommand(process,"tellraw @a [\"\",{\"text\":\"Seed: [\"},{\"text\":\"51109066175183\",\"color\":\"green\",\"clickEvent\":{\"action\":\"copy_to_clipboard\",\"value\":\"51109066175183\"},\"hoverEvent\":{\"action\":\"show_text\",\"contents\":{\"text\":\"Click to Copy to Clipboard\"}}},{\"text\":\"]\"}]")
    elif args[0] == "help":
        #https://pastebin.com/raw/LbiSVzQu
        #minecraftjson.com
        #{"jformat":6,"jobject":[{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"none","insertion":"","click_event_type":0,"click_event_value":"","hover_event_type":0,"hover_event_value":"","hover_event_object":{},"hover_event_children":[],"id":"475cb068-cad5-480b-8e25-8278bf39d877","text":"Help: ["},{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"green","insertion":"","click_event_type":"1","click_event_value":"https://pastebin.com/raw/LbiSVzQu","hover_event_type":"1","hover_event_value":"","hover_event_object":{},"hover_event_children":[{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"none","insertion":"","click_event_type":0,"click_event_value":"","hover_event_type":0,"hover_event_value":"","hover_event_object":{},"hover_event_children":[],"id":"c360123b-d3aa-4bef-b0d9-b8357ea37bdc","text":"Click to Open Link"}],"id":"f075467e-18e3-492f-9c76-1523b42b941c","text":"Command List"},{"bold":false,"italic":false,"underlined":false,"strikethrough":false,"obfuscated":false,"font":null,"color":"none","insertion":"","click_event_type":0,"click_event_value":"","hover_event_type":0,"hover_event_value":"","hover_event_object":{},"hover_event_children":[],"id":"c16eea83-be6a-4095-be6d-11d1ec104069","text":"]"}],"command":"tellraw @a %s","jtemplate":"tellraw"}
        serverCommand(process,"tellraw @a [\"\",{\"text\":\"Help: [\"},{\"text\":\"Command List\",\"color\":\"green\",\"clickEvent\":{\"action\":\"open_url\",\"value\":\"https:\/\/pastebin.com\/raw\/LbiSVzQu\"},\"hoverEvent\":{\"action\":\"show_text\",\"contents\":{\"text\":\"Click to Open Link\"}}},{\"text\":\"]\"}]")
    elif args[0] == "clear":
        serverCommand(process,"tellraw @a \""+"\\n"*500+"\"")
    elif args[0] == "shadow":
        if len(args) == 1:
            serverCommand(process,"player "+player+" shadow")
        elif len(args) == 2:
                serverCommand(process,"tell "+player+" Invalid arguments! Type !help for help.")
        elif len(args) == 3:
            if args[1] in ["attack","use"]:
                try:
                    interval = int(args[2])
                    if interval < 2:
                        serverCommand(process,"tell "+player+" Interval must be an integer above 1!")
                    else:
                        serverCommand(process,"player "+player+" shadow")
                        serverCommand(process,"player "+player+" "+args[1]+" interval "+str(interval))
                except:
                    serverCommand(process,"tell "+player+" Interval must be an integer above 1!")

            else:
                serverCommand(process,"tell "+player+" Invalid arguments! Type !help for help.")
    elif args[0] in ["restart","stop"]:
        if player.lower() in ops:
            serverCommand(process,"say Server Restarting in 3...")
            time.sleep(1)
            serverCommand(process,"say Server Restarting in 2...")
            time.sleep(1)
            serverCommand(process,"say Server Restarting in 1...")
            time.sleep(1)
            serverCommand(process,"stop")
            ServerLoaded = False
        else:
            serverCommand(process,"tell "+player+" You don't have permission!")
    elif args[0] == "fullstop":
        if player.lower() in ops:
            ServerRestarts = False
            serverCommand(process,"say Ending server")
            serverCommand(process,"stop")
            ServerLoaded = False
        else:
            serverCommand(process,"tell "+player+" You don't have permission!")
    elif args[0] == "killserver":
        if player.lower() in ops:
            ServerRestarts = False
            ServerLoaded = False
            process.kill()
            process.terminate()
        else:
            serverCommand(process,"tell "+player+" You don't have permission!")
    elif args[0] == "ops":
        if player.lower() in ops:
            if len(args) == 2 and args[1] == "list":
                opsString = ""
                for i in ops:
                    if i != "the server":
                        opsString += ", " + i
                serverCommand(process,"tell "+player+" Server Manager Operators: "+opsString[2:])
            elif len(args) == 3:
                args[2] = args[2].lower()
                if args[1] == "remove":
                    serverCommand(process,"tell "+player+" Removing '"+args[2]+"' from server manager operators.")
                    try:
                        ops.remove(args[2])
                        rewriteOps()
                    except:
                        serverCommand(process,"tell "+player+" Player is not a server manager operator.")
                    
                elif args[1] == "add":
                    if args[2] in ops:
                        serverCommand(process,"tell "+player+" Player already a server manager operator.")
                    else:
                        serverCommand(process,"tell "+player+" Adding '"+args[2]+"' to server manager operators.")
                        ops.append(args[2])
                        rewriteOps()
                else:
                    serverCommand(process,"tell "+player+" Invalid arguments! Type !help for help.")
            else:
                serverCommand(process,"tell "+player+" Invalid arguments! Type !help for help.")
        else:
            serverCommand(process,"tell "+player+" You don't have permission!")
    else:
        serverCommand(process,"tell "+player+" Invalid command.")



def getServer():
    global MCServer
    return MCServer

def consoleInput():
    global ServerLoaded
    process = getServer()
    while True:
        inp = input()
        process = getServer()
        if process != None and process.poll() == None:
            if ServerLoaded:
                if inp == "fullstop":
                    print("[Server Hoster] Executing fullstop")
                    customCommand(process,"fullstop")
                elif inp.split(" ")[0] == "ops":
                    customCommand(process,inp)
                elif inp == "killserver":
                    customCommand(process,inp)
                else:
                    serverCommand(process,inp)
            else:
                print("[Server Hoster] Server not yet loaded")
        else:
            if not ServerRestarts:
                exit()
            print("[Server Hoster] No server process")

def consoleOutput():
    global ServerRestarts, ServerLoaded
    #Credit to Miniaczq for help with Regex (I forced him to help by using the plagiarism technique)
    playerReg = compile(r'\[..:..:..\] \[Server thread/INFO\]: <.*?> !.*?').search
    stopReg = compile(r'\[..:..:..\] \[Server thread/INFO\]: Stopping server').search
    doneReg = compile(r'\[..:..:..\] \[Server thread/INFO\]: Done').search
    process = getServer()
    while True:
        if process != None and process.poll() == None:
            for line in process.stdout:
                if islinux:
                    #Interpret Linux
                    line = str(line)
                    line = line[2:len(line)-3]
                else:
                    #Interpret Windows (unknown function for mac)
                    line = str(line.rstrip())[2:len(line)]
                print(line)
                if playerReg(line):
                    customCommand(process,line[line.index(">")+3:],line[line.index("<")+1:line.index(">")])
                if stopReg(line):
                    ServerLoaded = False
                if doneReg(line):
                    print("[Server Hoster] Server is now loaded; ready for inputs.")
                    ServerLoaded = True
                    process.stdin.flush()


        else:
            if not ServerRestarts:
                exit()
            process = getServer()
            time.sleep(2)


if __name__ == '__main__':
    islinux = isfile("islinux")
    if islinux:
        print("[Server Hoster] Linux detected.")
    ops = ["the server"]
    try:
        opsFile = open("ops.txt","r")
        opsFileText = opsFile.read()
        opsFile.close()
        for i in opsFileText.split("\n"):
            if i != "":
                print("[Server Hoster] OP Loaded: "+i)
                ops.append(i.lower())
    except:
        opsFile = open("ops.txt","w+")
        opsFile.write("Enter OPS here, with a new line in between each player (Replace this line)")
        opsFile.close()

    popenCommand = "java -jar server.jar nogui"
    try:
        runFile = open("run.txt","r")
        popenCommand = runFile.read()
        runFile.close()
    except:
        runFile = open("run.txt","w+")
        runFile.write(popenCommand)
        runFile.close()

    ServerRestarts = True
    MCServer = None
    ServerLoaded = False

    consoleInputProcessing = Thread(target=consoleInput,args=[])
    consoleInputProcessing.start()

    consoleOutputThread = Thread(target=consoleOutput,args=[])
    consoleOutputThread.start()

    while ServerRestarts:
        MCServer = Popen(popenCommand,cwd="server",stdin=PIPE,stdout=PIPE,stderr=PIPE, close_fds=True)

        while MCServer.poll() == None:
            time.sleep(0.1)
    print("[Server Hoster] Enter to exit...")