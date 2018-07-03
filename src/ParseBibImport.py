import os
import sys
import time
import math
from datetime import datetime
from ReferenceStructure import *

class BibTeXParser():
    """
    Parser for reading BibTeX data files
    """

    def __init__(self, path):
        self.path = path
        self.referenceDictList = []
        self.readFile()

    def readFile(self):
        data = []
        with open(self.path, 'r') as inf:
            data = inf.readlines()
        startInds = []
        endInds = []
        indPairs = []
        fileEndInd = len(data)
        for term in BibTeXTypes:
            key = '@'+term
            tempInd = [i for i,x in enumerate(data) if key in x]
            startInds = startInds + tempInd
        startInds.sort()
        if len(startInds) == 1:
            indPairs.append([startInds[0],fileEndInd])
        elif len(startInds) > 1:
            for i in range(len(startInds)-1):
                indPairs.append([startInds[i], startInds[i+1]])
            indPairs.append([startInds[-1], fileEndInd])
        else:
            print("No valid BibTeX item found.")
        for pair in indPairs:
            refItem = self.parseBibItem(data[pair[0]:pair[1]] )
            self.referenceDictList.append(refItem)

    def parseBibItem(self, bibItemList):
        bibType = "article"
        ind1 = bibItemList[0].index('@')
        ind2 = bibItemList[0].index('{')
        ind3 = bibItemList[0].index(",\n")
        bibType = bibItemList[0][ind1+1:ind2].replace(" ", "")
        citeKey = bibItemList[0][ind2+1:ind3]
        refItem = {}
        refItem['MType'] = bibType.capitalize()
        refItem['Citekey'] = citeKey
        for line in bibItemList[1:]:
            if "=" in line and "\n" in line:
                tempInd1 = line.index("=")
                fieldKey = line[0:tempInd1].replace(" ", "").replace("\t","")
                tempInd2 = line.index("{")
                tempInd3 = tempInd2
                if "},\n" in line:
                    tempInd3 = line.index("},\n")
                elif "}\n" in line:
                    tempInd3 = line.index("}\n")
                fieldValue = line[tempInd2+1:tempInd3]
                fieldKey2 = fieldKey #.capitalize()
                if fieldKey2 == 'title':
                    fieldValue = fieldValue.replace("{","")
                    fieldValue = fieldValue.replace("}","")
                refItem[fieldKey2] = fieldValue
                if fieldKey2 == 'year':
                    refItem[fieldKey2] = fieldValue
            if 'Label' not in refItem:
                refItem['Label'] = ""
            currentTime = datetime.now()
            currentTimeStr = currentTime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            refItem['AddedTime'] = currentTimeStr
            tablename = refItem['MType']
            refItem['RefAbsID'] = int(DB_TypeCode[tablename]*math.pow(10,8))
            tempDBFieldsList = DB_BaseFields + DatabaseStandardStructure[tablename] + DB_ExtendFields
            for field in tempDBFieldsList[2:]:
                if field not in refItem:
                    refItem[field] = ""
        return refItem


if __name__ == "__main__":
    bp = BibTeXParser("My Collection.bib")
