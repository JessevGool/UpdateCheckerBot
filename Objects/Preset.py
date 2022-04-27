from bs4 import BeautifulSoup
import os
defaultPath = "config/preset/"
class Preset:
    def __init__(self,fileName):
        self.fileName = fileName
        self.updateTime = self.__getUpdateTime()
        self.modList = self.__getModList()

    def __getUpdateTime(self):
        return os.path.getmtime(defaultPath+self.fileName)

    def __getModList(self):
        mods = []
        preset = open(defaultPath+self.fileName,'r')
        soup = BeautifulSoup(preset.read(),features="html.parser")
        modslinks = soup.find_all('a',{'data-type':"Link"})
        for link in modslinks:
            splitLink = link.text.split("?id=")
            if(len(splitLink) == 2):
                mods.append(splitLink[1])
        return mods


