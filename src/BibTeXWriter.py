from DatabaseIO import *

class BibTeXWriter:
    def __init__(self, path, refDictList):
        self.path = path
        self.referenceDictList = refDictList
        self.writeFile()
        self.status = None

    def writeFile(self):
        print("Write")
        print(self.referenceDictList)
