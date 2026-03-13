import shutil
import os


RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"


def renderIcons(fileName):
    fileName = str(fileName).lower()           # good – keep this
    if not '.' in fileName:
        return "📄"                            # no extension

    ext = fileName.rsplit('.', 1)[1]           # get part after last dot

    if ext in ('txt', 'md', 'markdown', 'log'):
        return "📝"
    elif ext == 'mp3':
        return "🎵"
    elif ext in ('mp4', 'mkv', 'avi', 'webm'):
        return "🎬"
    elif ext in ('sh', 'bash', 'bat', 'ps1', 'cmd'):
        return "💻"
    elif ext in ('zip', '7z'):
        return "🗃️"
    elif ext == 'rar':
        return "🗄️"
    elif ext in ('html', 'htm'):
        return "🌐"
    elif ext == 'exe':
        return "💾"
    elif ext in ('png', 'jpg', 'jpeg', 'webp', 'gif', 'bmp'):
        return "🖼️"
    else:
        return "📄"
    
    
    
    
def renderPercentage(amount):
    if amount == 100:
        return f"{RED}『-X-X-X-X-X-X-X-X-X-X』{RESET}"
    elif amount > 90:
        return f"{RED}『 * * * * * * * * * *』{RESET}"
    elif amount > 80:
        return f"{YELLOW}『 * * * * * * * * *  』{RESET}" 
    elif amount > 70:
        return f"{YELLOW}『 * * * * * * * *    』{RESET}"
    elif amount > 60:
        return f"{YELLOW}『 * * * * * * *      』{RESET}"
    elif amount > 50:
        return f"{BLUE}『 * * * * * *        』{RESET}"
    elif amount > 40:
        return f"{BLUE}『 * * * * *          』{RESET}"
    elif amount > 30:
        return f"{BLUE}『 * * * *            』{RESET}"
    elif amount > 20:
        return f"{BLUE}『 * * *              』{RESET}"
    elif amount > 10:
        return f"{GREEN}『 * *                』{RESET}"
    elif amount < 10 and amount != 0:
        return f"{GREEN}『 *                  』{RESET}"
    elif amount == 0:
        return f"{GREEN}『                    』{RESET}"


def cleanNames (nameList):
    cleanedNames = []
    nameList = nameList.split(",")
    for n in nameList:
        cleanedNames.append(n.strip())
    return cleanedNames

def manipulateHandler(tool,data,path):
    if tool == "copy":
        items = cleanNames(data)
        returnItems = []
        doubleCheck = set()
        for item in items:
            
            targetPath = os.path.join(path, item)
            if os.path.exists(targetPath) and item not in doubleCheck:
                returnItems.append({
                    "name" : item,
                    "path" : targetPath,
                    "is_dir" : os.path.isdir(targetPath)
                })
                doubleCheck.add(item)
        
        return returnItems        


    if tool == "paste":
        if len(data) == 0:
            print(f"{RED}No files copied to paste in here{RESET}")
            return False
        else:
            for item in data:
                copiedPath = item['path']
                newPath = os.path.join(path,item['name'])
                
                try:
                    if item['is_dir']:
                        shutil.copytree(copiedPath,newPath)
                    else :
                        shutil.copy2(copiedPath,newPath)    
                    
                   
                
                except FileExistsError:
                    input(f"{RED}{FileExistsError}{RESET}, Press Enter")
                           
                except Exception as e:
                    input(f"{RED}{e}{RESET}, Press Enter")
                    
            return True        
    
    if tool == "delete":
        items = cleanNames(data)
        for item in items:
            targetPath = os.path.join(path,item)
            try:
                if os.path.exists(targetPath):
                    if os.path.isdir(targetPath):
                        shutil.rmtree(targetPath)
                    else:
                        os.remove(targetPath)    
            except Exception as e:    
                input(f"{RED}{e}{RESET}, Press Enter...")
                
    
    
    if tool == "new":
        items = cleanNames(data)
        for item in items:
            targetPath = os.path.join(path,item)
            try:
                with open (targetPath, 'w') as f:
                    pass
            except Exception as e:
                input(f"{RED}{e}{RESET}, Press Enter")
                            
    
    if tool == "new folder":

        items = cleanNames(data)
        for item in items:
            targetPath = os.path.join(path,item)
            try:
                os.makedirs(targetPath,exist_ok=True)
                
            except Exception as e:
                input(f"{RED}{e}{RESET}, Press Enter")                                