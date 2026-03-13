# Importing all the libraries for works (everything is preinstalled to python so no need to download anything)
import os
import pathlib
import shutil
import sys
import glob
import fnmatch
import datetime
import subprocess
import cmd
import readline
import string
from tools import renderIcons
from tools import renderPercentage
from tools import manipulateHandler

# creating global variables 

currentPath = "home"
selectedFolders = []
selectedFiles = []
copiedFiles = []
programIsRunning = True
drivers = []
spaceManager = {
    "driverName" : "          ", #10
    "label": "                    ", #20
    "usage": "                    ", #20
    "files": "                              ", #30
    
}
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"
# creating all the functions 
# about the width : width maximum length should be 70

def clear_screen () :
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _= os.system('clear')
    
    cpName = []
    for n in copiedFiles:
        cpName.append(n["name"])    
    print(f"File Manager Location : [{currentPath}] | copied : {cpName}\n")

# Rendering the home screen
def homeScreen ():
    global drivers
    drivers = []
    clear_screen()
    driverNames = list(string.ascii_uppercase)
    for i in driverNames:
        if os.path.isdir(f"{i}:/"):
            path = f"{i}:/"
            usage = shutil.disk_usage(path)
            total = round(usage.total/1024**3)-1
            used = round(usage.used/1024**3)-1
            free = round(usage.free/1024**3)-1
            label = subprocess.check_output(f"vol {i}:",shell=True).decode()
            
            if label in 'has no label':
                label = "No Label"
            else:
                label = label.split('is')[1].split("\n")[0].strip()    
             
            
            drivers.append({
                "path" : path,
                "total":total,
                "used": used,
                "free":free,
                "label": label
                })
            print(f"{len(drivers)}. {(path)+spaceManager['driverName'][len(path)-1:]} [{(label)}]{spaceManager['label'][len(label)-1:]} {total} GB [{used}/{free} GB] {spaceManager['usage'][(len(str(total))-1+len(str(used))-1+len(str(free))-1):]} ({round(used*100/total)-1}% used) {renderPercentage(round(used*100/total)-1)}\n")


# Changing the current path and rendering the new path
def changeLocation (path):
    global currentPath
    global copiedFiles
    
    currentPath = path
    clear_screen()
    files = [[]]
    folders = [[]]
    allFiles = []
    allFolders = []
    
    # saving files and folders
    
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                if len(files[-1]) < 4:
                    files[-1].append(entry.name)
                else:
                    files.append([])
                    files[-1].append(entry.name)
                allFiles.append(entry.name)    
            elif entry.is_dir():
                if len(folders[-1]) < 4:
                    folders[-1].append(entry.name)
                else:
                    folders.append([])
                    folders[-1].append(entry.name)
                allFolders.append(entry.name)
    # Showing all the files and folders (files are 1st and then folders) 
    for folderNames in folders:
        
        show = ""
        for folderName in folderNames:
            if len(folderName) <= 30:
                show = f"{show}  📁 {BLUE}{folderName}{RESET} {spaceManager['files'][len(folderName)-1:]}"
            else:
                
                show = f"{show}  📁 {BLUE}{folderName[0:30]}... {RESET} {spaceManager['files'][len(folderName):]}"
                
        if show.strip():
            print(show.rstrip())
            print("")
    
    
    print("")    
    for fileNames in files:
        show = ""
        for fileName in fileNames:
            if len(fileName) <= 30:
                show = f"{show}  {renderIcons(fileName)} {BLUE}{fileName}{RESET} {spaceManager['files'][len(fileName)-1:]}"
            else:
                
                show = f"{show}  {renderIcons(fileName)} {BLUE}{fileName[0:30]}... {RESET} {spaceManager['files'][len(fileName):]} "
               
            
        if show.strip():
            print(show.rstrip())
            print("")

        
    print("""\nCommands:
• name              → open file/folder
• copy <name/s>     → copy (comma ',' to separate)
• clear copy        → clear the copy list
• paste             → paste copied items
• delete <name>     → delete a file/folder (comma ',' to separate)
• new <name>        → new file (comma ',' to separate)
• new folder <name> → new folder (comma ',' to separate)
• /back             → go back to the pervious folder )
• /home             → go to home screen""")
    userInput = str(input("\n> "))
    if userInput.lower() == "/home":
        currentPath = "home"
        homeScreen()
    elif userInput.lower() == "/back":
        p = pathlib.Path(currentPath)
        
        if p.parent == p:
            currentPath = "home"
            homeScreen()
        else:
            currentPath = p.parent
            changeLocation(currentPath)
                

                    
    elif userInput in allFiles:
        if len(str(path)) == 3:
            os.startfile(pathlib.Path(str(path)+userInput))
        else:
            os.startfile(pathlib.Path(str(path)+"/"+userInput))
                
        changeLocation(path)
    elif userInput in allFolders:
        if len(str(currentPath)) == 3: 
            currentPath = pathlib.Path(str(currentPath)+userInput)
        else:
            currentPath = pathlib.Path(str(currentPath)+"/"+userInput)
        
        changeLocation(currentPath)    
    elif userInput.lower().startswith("copy "):
        copiedFiles = manipulateHandler("copy",userInput[5:],path)
        if isinstance(copiedFiles,list):
            copiedFiles = copiedFiles
        else:
            copiedFiles = []    
        changeLocation(path)
    elif userInput.lower().startswith("paste"):
        answer = manipulateHandler("paste",copiedFiles,path)
        if answer:
            changeLocation(path)
        else:
            input("Press enter ...")
            changeLocation(path)    
    elif userInput.lower().startswith("delete "):
        manipulateHandler("delete",userInput[7:],path)
        changeLocation(path)
    elif userInput.lower().startswith("new folder "):
        manipulateHandler("new folder",userInput[11:],path)
        changeLocation(path) 
    elif userInput.lower().startswith("new "):
        manipulateHandler("new",userInput[4:],path)
        changeLocation(path)
    elif userInput.lower().startswith("clear copy"):
        copiedFiles = []
        changeLocation(path)
    else:
        input(f"{RED}Type error please try again, press Enter{RESET}")
        changeLocation(path)                               


# rendering the main loop to handle everything
while programIsRunning:
    
    
    # checking if the user's current path is home or not
    if currentPath == "home":
        homeScreen()
        print(f"Enter a number (1-{len(drivers)}) to open")
        userInput = input("> ")
        if userInput.isdigit():
            userInput = int(userInput)
        else:
            userInput = 0                  
        
        if userInput != 0 and userInput <= len(drivers) :
            userInput = int(userInput)
            changeLocation(pathlib.Path(f"{drivers[userInput-1]['path']}"))
            
        else : 
            input(f"{RED}Path doesn't exist, press Enter and try again..{RESET}")    
            
        
                    