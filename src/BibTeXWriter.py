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
            outputString = outputString + refStr
        with open(self.path, 'w') as outf:
            outf.write(outputString)


    def formatBibItem(self, refItem):
        print(refItem)
        bibItemStr = ""
        if refItem['Type'].lower() in BibTeXTypes:
            bibItemStr = bibItemStr + "@" + refItem['Type'].lower() + "{" + "\n"
            bibItemStr = bibItemStr + "}\n"
        return bibItemStr
