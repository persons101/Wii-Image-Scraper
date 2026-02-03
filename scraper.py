import urllib.request
import bs4
import string
import re
from pathlib import Path

def download_image(url, save_as):
    urllib.request.urlretrieve(url, save_as)

gameID = input("Define 6 digit game id: ")
saveDir = input("Define an output directory (default is currDir/images/ ): ")

if (saveDir == ""):
    saveDir = str(Path.cwd()) + "\\images\\"

previousChar = ""
for char in saveDir:
    char = char.capitalize()


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

#imgs = imgs.img["src", re("(?<=https:\/\/art\.gametdb\.com\/wii\/cover)[^B].[^B]")]


for img in imgs:
# #TODO LEARN HOW TO USE REGEX IN PYTHON AND BEAUTIFULSOUP4
    coverStr = re.search("(?<=https:\/\/art\.gametdb\.com\/wii\/cover)[^B].[^B]", img.get('src')) # outputs "/.." for regular, "3D/" for 3D, "ful" for full, and ignores all secondary covers

    fileType = (re.search("....$", img.get('src'))).group()

    if (coverStr):
        if (re.match("^/", coverStr.group())): # regular cover
            download_image(img.get("src"), saveDir + "2D\\" + gameID + ".png")
        elif (coverStr.group() == "3D/"): # 3D cover:
            download_image(img.get("src"), saveDir + "" + gameID + ".png")
        elif (coverStr.group() == "ful"): # full cover:
            download_image(img.get("src"), saveDir + "full\\" + gameID + fileType)
        elif (coverStr.group() == "dis"): # disc cover:
            download_image(img.get("src"), saveDir + "disc\\" + gameID + fileType)


    else:
        print(str(img) + ": None")
        print(img.get('src'))
    
    