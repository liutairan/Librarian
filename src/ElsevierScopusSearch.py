# https://dev.elsevier.com/sc_apis.html
# https://dev.elsevier.com/
# https://github.com/ElsevierDev/elsapy

"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json

class ElsevierScopusSearch:
    """ An instance of this class is a search command"""
    def __init__(self):
        self.loadConfig()
        self.initClient()

    def loadConfig(self):
        ## Load configuration
        try:
            con_file = open("esconfig.json")
            self.config = json.load(con_file)
            con_file.close()
        except:
            pass

    def initClient(self):
        ## Initialize client
        try:
            self.client = ElsClient(self.config['apikey'])
            self.client.inst_token = self.config['insttoken']
        except:
            pass

    def readFullDocWithPII(self, sd_piiID):
        ## ScienceDirect (full-text) document example using PII
        pii_doc = FullDoc(sd_pii = sd_piiID)
        if pii_doc.read(self.client):
            print(pii_doc)
            print ("pii_doc.title: ", pii_doc.title)
            pii_doc.write()
        else:
            print ("Read document failed.")

def main():
    obj = ElsevierScopusSearch()
    obj.readFullDocWithPII('S1270963817323015')

if __name__ == "__main__":
    main()
