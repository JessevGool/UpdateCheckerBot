import requests
import json
from Objects.Mod import workshopMod
class ApiHandler:
    def __init__(self):
        print("ApiHandler created")

    def requestInfo(self,_modlist, errors = 0):
        """! requests mod info from the steam web api
        @param modlist list of mod ids
        @return list of workshopMods
        @see Mod#workshopMod() workshopMod
        """
        _data = {'itemcount': len(_modlist)}
        for idx, mod in enumerate(_modlist):
            _data["publishedfileids[{0}]".format(idx)] = mod
        with open('config/secrets.json') as secrets:
            secrets = json.load(secrets)
        response = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/?key={0}".format(secrets['steamAPIKey']), data=_data)
        try:
            modlist = response.json()
            modlist = modlist["response"]["publishedfiledetails"]
            gatheredModInfo = []
            for mod in modlist:
                gatheredModInfo.append(self.jsonToMod(mod))
            
            return gatheredModInfo
        except ValueError:
            if(errors <= 3):
                print("Error with JSON, retrying {0} more times".format( 3-errors))
                return self.requestInfo(_modlist,errors+1)
            else:
                return []

    def jsonToMod(self,modJson):
        """! converts a steamworkshop mod in json to a workshopMod object
        @param modJson steamworkshop mod in Json format
        @return steamworkshop mod in workshopMod format
        @see Mod#workshopMod() workshopMod
        """
        mod = workshopMod(modJson["publishedfileid"],modJson["title"],modJson["file_size"],modJson["time_created"],modJson["time_updated"])
        return mod