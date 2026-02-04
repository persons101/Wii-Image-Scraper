import urllib.request
import bs4
import string
import re
from pathlib import Path

from numpy import save

def download_image(url, save_as):
    urllib.request.urlretrieve(url, save_as)

gameID = input("Define 6 digit game id: ")
saveDir = input("Define an output directory (default is currDir/images/ ): ")

if (saveDir == ""):
    saveDir = str(Path.cwd()) + "\\images\\"

# previousChar = ""
# for char in saveDir:
#     char = char.capitalize()
if not saveDir.endswith(('\\','\/')):
    saveDir += "\\"


# TODO Make default save directory

html = urllib.request.urlopen("https://www.gametdb.com/Wii/" + gameID)
html = html.read()
# print(html)

soup = bs4.BeautifulSoup(html, 'html.parser')

# print(soup.prettify())
# print("\n"+'*'*10+"\n")

imgs = soup.find_all('img')
# re.compile("(?<=https:\/\/art\.gametdb\.com\/wii\/cover)[^B].[^B]")

# print(imgs, sep='\n')
# print("\n"+'*'*10+"\n")

imgs.reverse()
for i in range(6):
    imgs.pop()


# print(imgs, sep='\n')
# print("\n"+'*'*10+"\n")


i:int = 1
str_indent = ">>> "
str_indent_download = "|>>"

def createSaveDir(saveDir: str | Path):
    DirsNeeded = [None, "2D", "full", "disc"]
    saveDir = Path(saveDir)
    
    for dir in DirsNeeded:
        if dir == None:
            saveDir.mkdir(exist_ok=True)
        else:
            saveDir.joinpath(dir).mkdir(exist_ok=True)


    return

for img in imgs:
    print(i, img.get('src'), end="")
# 
#  #TODO LEARN HOW TO USE REGEX IN PYTHON AND BEAUTIFULSOUP4
    coverStr = re.search("(?<=https:\/\/art\.gametdb\.com\/wii\/)(disc|cover)([^Bc\/]*)\/", img.get('src')) # outputs "/.." for regular, "3D/" for 3D, "ful" for full, and ignores all secondary covers
    

    fileType = (re.search("\....(?=$|\?)", img.get('src'))).group()

    if (coverStr):
        try:
            createSaveDir(saveDir)

            if (coverStr.group() == "cover/"): # regular cover
                print("\n", str_indent_download, "Downloading 2D cover...")
                download_image(img.get("src"), saveDir + "2D\\" + gameID + fileType)
            elif (coverStr.group() == "cover3D/"): # 3D cover:
                print("\n", str_indent_download, "Downloading 3D cover...")
                download_image(img.get("src"), saveDir + "" + gameID + fileType)
            elif (coverStr.group() == "coverfull/"): # full cover:
                print("\n", str_indent_download, "Downloading full cover...")
                download_image(img.get("src"), saveDir + "full\\" + gameID + fileType)
            elif (coverStr.group() == "disc/"): # disc cover:
                print("\n", str_indent_download, "Downloading disc cover...")
                download_image(img.get("src"), saveDir + "disc\\" + gameID + fileType)
            else:
                print(str_indent, "Non-standard file: ", img.get('src'))
            
        except FileNotFoundError as e:
            print(str_indent, "File error:", e)
            pass
        except Exception as e:
            print(str_indent, e)
            pass 

    else:
        print(" ", str_indent, str(img) + ": None")
    
    i = i+1
    
    