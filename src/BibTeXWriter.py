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
        bibItemStr = ""
        if refItem['Type'].lower() in BibTeXTypes:
            bibtexType = refItem['Type'].lower()
            fieldSet = ReferenceStandardStructure[bibtexType]
            citeKey = ""
            if 'Citekey' in refItem:
                if  len(refItem['Citekey']):
                    citeKey = refItem['Citekey']
            if len(citeKey) == 0:
                if len(refItem['Authors']):
                    tempS1 = refItem['Authors'].split(",")[0]
                    citeKey = citeKey + tempS1
                    tempS2 = str(refItem['Year'])
                    citeKey = citeKey + tempS2
                    if len(refItem['Title']):
                        tempS3 = refItem['Title'].split(" ")[0]
                        citeKey = citeKey + tempS3
            bibItemStr = bibItemStr + "@" + refItem['Type'].lower() + "{" + citeKey + ",\n"
            bibItemStr = bibItemStr + "}\n"
        return bibItemStr
