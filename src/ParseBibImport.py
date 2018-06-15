import os
import sys

from ReferenceStructure import *

class BibTeXParser():
    """
    Parser for reading BibTeX data files
    """

    def __init__(self, path):
        self.path = path
        self.readFile()
        self.referenceDictList = []

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
            self.parseBibString(''.join(data[pair[0]:pair[1]]) )

    def parseBibString(self, bibStr):
        pass

if __name__ == "__main__":
    bp = BibTeXParser("My Collection.bib")
