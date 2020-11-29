from subprocess import PIPE, Popen
from re import search, compile
from threading import Thread
from multiprocessing import Process
from os.path import isfile
import time

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
                else:
                    serverCommand(process,inp)
            else:
                print("[Server Hoster] Server not yet loaded")
        else:
            if not ServerRestarts:
                exit()
            print("[Server Hoster] No server process")

def serverCommand(process,text):
    global ServerLoaded
    process.stdin.write((text+"\n").encode())
    if ServerLoaded:
        process.stdin.flush()

def customCommand(process,command,player="The Server"):
    global ServerRestarts, ServerLoaded

    args = command.split(" ")

    if args[0] == "seed":
        serverCommand(process,"tellraw @a {\"text\":\"51109066175183\",\"color\":\"green\",\"clickEvent\":{\"action\":\"copy_to_clipboard\",\"value\":\"51109066175183\"}}")
    elif args[0] == "clear":
        serverCommand(process,"tellraw @a \""+"\\n"*500+"\"")
    elif args[0] == "shadow":
        serverCommand(process,"player "+player+" shadow")
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
    else:
        serverCommand(process,"tell "+player+" Invalid command.")



def getServer():
    global MCServer
    return MCServer

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
    ops = ["The Server"]
    try:
        opsFile = open("ops.txt","r")
        opsFileText = opsFile.read()
        opsFile.close()
        for i in opsFileText.split("\n"):
            if i != "":
                print("[Server Hoster] OP Loaded: "+i)
                ops.append(i)
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

    for i in range(len(ops)):
        ops[i] = ops[i].lower()

    ServerRestarts = True
    MCServer = None
    ServerLoaded = False

    consoleInputProcessing = Thread(target=consoleInput,args=[])
    consoleInputProcessing.start()

    consoleOutputThread = Thread(target=consoleOutput,args=[])
    consoleOutputThread.start()

    while ServerRestarts:
        MCServer = Popen(popenCommand,cwd="server",stdin=PIPE,stdout=PIPE,stderr=PIPE, close_fds=True, shell=True)

        while MCServer.poll() == None:
            time.sleep(0.1)
        MCServer.terminate()
    print("[Server Hoster] Enter to exit...")