from DataBaseHandler import DataBaseHandler
from Preset import Preset
from ApiHandler import ApiHandler
import os
from os import listdir
from os.path import isfile, join
from discord.ext import commands
import discord

class UpdateChecker(commands.Cog):
    async def printDEBUG(self,message):
        print(message)
        DEBUG_CHANNEL = self.client.get_guild(535921542198984727).get_channel(701548889118998598)
        await DEBUG_CHANNEL.send(message)

    async def printDEBUGEMBED(self,message):
        DEBUG_CHANNEL = self.client.get_guild(535921542198984727).get_channel(701548889118998598)
        await DEBUG_CHANNEL.send(embed=message)

    def __init__(self,client):
        self.client = client
        print("UpdateChecker created")
        self.databaseHandler = DataBaseHandler()
        self.apiHandler = ApiHandler()
        self.presetList = self.__getPresets("/config/preset")
        self.currentModPack = self.setInitialModPackToCheck()

    def __getPresets(self, presetFolderPath):
        presetHtmls = [f for f in listdir(
            os.getcwd()+presetFolderPath) if isfile(join(os.getcwd()+presetFolderPath, f))]
        presets = []
        for html in presetHtmls:
            presets.append(Preset(html))
        return presets

    def setInitialModPackToCheck(self):
        """Sets the initial list of mods to check
        @return: list of mods to check
        """
        self.presetList = self.__getPresets("/config/preset")
        mods = []
        for preset in self.presetList:
            mods += preset.modList
        mods = list(dict.fromkeys(mods))
        return mods
    async def checkforModpackUpdates(self):
        """Updates the list of mods to check if necessary 
        """
        newPresets = self.__getPresets("/config/preset")
        for newPreset in newPresets:
            isInList = False;
            for oldPreset in self.presetList:
                if(newPreset.fileName == oldPreset.fileName):
                    isInList = True
                    if(newPreset.updateTime > oldPreset.updateTime):
                        await self.printDEBUG(newPreset.fileName + " has been updated")
                        self.presetList.remove(oldPreset)
                        self.presetList.append(newPreset)
                        for mod in newPreset.modList:
                            self.currentModPack.append(mod)
                            self.currentModPack = list(dict.fromkeys(self.currentModPack))
            if not isInList:
                await self.printDEBUG(newPreset.fileName + " has been added")
                self.presetList.append(newPreset)
                for mod in newPreset.modList:
                    self.currentModPack.append(mod)
                    self.currentModPack = list(dict.fromkeys(self.currentModPack))
        await self.compareDBModsToPresetMods()

            
    async def compareDBModsToPresetMods(self):
        dataBaseMods = self.databaseHandler.getmodCollectionFromDB()
        steamAPIMods = self.apiHandler.requestInfo(self.currentModPack)
        dataBaseModIds = []
        for DBmod in dataBaseMods:
            dataBaseModIds.append(DBmod.id)
        dataBaseModIds = self.__checkIfModIsInDB(dataBaseModIds,steamAPIMods)
        await self.__checkIfModHasUpdated(dataBaseMods,steamAPIMods)

    def __checkIfModIsInDB(self,databaseModIds,steamAPIMods):
        for mod in steamAPIMods:
            if(mod.id not in databaseModIds):
                self.databaseHandler.addModToCollection(mod)
                databaseModIds.append(mod.id)
        return databaseModIds

    async def __checkIfModHasUpdated(self,databaseMods,steamAPIMods):
        for mod in databaseMods:
            for steamMod in steamAPIMods:
                if(mod.id == steamMod.id):
                    updated = False
                    if(mod.updateDate != steamMod.updateDate):
                        mod.updateDate = steamMod.updateDate
                        updated = True
                    if(mod.fileSize != steamMod.fileSize):
                        mod.fileSize = steamMod.fileSize
                        updated = True
                    if(mod.name != steamMod.name):
                        mod.name = steamMod.name
                        updated = True
                    if(updated):
                        self.databaseHandler.updateModInCollection(mod)
                        await self.printDEBUGEMBED(self.createModEmbed(mod))

    def createModEmbed(self,mod):
         embedVar = discord.Embed(title=f'{mod["name"]} has been updated',description = "",color = 0x00ff00)
         embedVar.add_field(name="Filesize",value=mod.fileSizeToMB(),inline= False)
         embedVar.add_field(name="Update Time",value=mod.timeStampToDate,inline= False)
         return embedVar




                
                    
