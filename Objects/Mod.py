import json
import datetime
class workshopMod:
    def __init__(self,id,name,fileSize,postDate,updateDate):
        self.id = id
        self.name = name
        self.fileSize = fileSize
        self.postDate = postDate
        self.updateDate = updateDate
    def toJSON(self):
        return json.dumps(self,default=lambda o: o.__dict__,sort_keys=True,indent=4)

    def fileSizeToMB(self):
        return str(self.fileSize/1000000)+"MB"
    def timeStampToDate(self):
        return datetime.datetime.utcfromtimestamp(self.updateDate)
