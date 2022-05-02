import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from Objects.Mod import workshopMod
import json
class DataBaseHandler:
    def __init__(self):
        cred = credentials.Certificate("config/updateCheckerToken.json")
        with open("config/secrets.json") as secrets:
            secrets = json.load(secrets)
        try:
            firebase_admin.get_app()
        except:
            firebase_admin.initialize_app(cred, 
            {
            'databaseURL': secrets["databaseURL"]
            })
        self.collectionref = db.reference("/ModCollection")
        print("DataBaseHandler created")


    def getmodCollectionFromDB(self):
        modDict = self.collectionref.get()
        mods = []
        for _mod in modDict.items():
            mod = workshopMod(_mod[0],_mod[1]["name"],_mod[1]["fileSize"],_mod[1]["postDate"],_mod[1]["updateDate"])
            mods.append(mod)
        
        return(mods)

    def setModCollectionForDB(self,mods):
        for mod in mods:
            self.collectionref.child(str(mod.id)).set(
            {
                "name" : mod.name,
                "fileSize" : mod.fileSize,
                "postDate" : mod.postDate,
                "updateDate" : mod.updateDate
            }
            )
    def addModToCollection(self,mod):
         self.collectionref.child(str(mod.id)).set(
            {
                "name" : mod.name,
                "fileSize" : mod.fileSize,
                "postDate" : mod.postDate,
                "updateDate" : mod.updateDate
            }
            )

    def updateModInCollection(self,mod):
        self.collectionref.child(str(mod.id)).update(
            {
                "name" : mod.name,
                "fileSize" : mod.fileSize,
                "postDate" : mod.postDate,
                "updateDate" : mod.updateDate
            }
        )