from DatabaseIO import *
from ReferenceStructure import *

class BibTeXWriter:
    def __init__(self, path, refDictList):
        self.path = path
        self.referenceDictList = refDictList
        self.writeFile()
        self.status = None

    def writeFile(self):
        outputString = ""
        for ref in self.referenceDictList:
            refStr = self.formatBibItem(ref)
            print(refStr)
            outputString = outputString + refStr
        print(outputString)


    def formatBibItem(self, refItem):
        bibItemStr = ""
        if refItem['Type'].lower() in BibTeXTypes:
            bibItemStr = bibItemStr + "@" + refItem['Type'].lower() + "{"
            bibItemStr = bibItemStr + "}\n"
        return bibItemStr
