# https://dev.elsevier.com/sc_apis.html
# https://dev.elsevier.com/
# https://github.com/ElsevierDev/elsapy

"""An example program that uses the elsapy module"""
"""Modified from the example given by https://github.com/ElsevierDev/elsapy"""
"""To do"""

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

    def readFullDocWithPII(self, sd_piiID='S1270963817323015'):
        ## ScienceDirect (full-text) document example using PII
        pii_doc = FullDoc(sd_pii = sd_piiID)
        if pii_doc.read(self.client):
            print(pii_doc)
            print ("pii_doc.title: ", pii_doc.title)
            pii_doc.write()
        else:
            print ("Read document failed.")

    def readFullDocWithDOI(self, doiID='10.1016/S1525-1578(10)60571-5'):
        ## ScienceDirect (full-text) document example using DOI
        doi_doc = FullDoc(doi = doiID)
        if doi_doc.read(self.client):
            print ("doi_doc.title: ", doi_doc.title)
            doi_doc.write()
        else:
            print ("Read document failed.")

    def readAbsDocWithScopusID(self, scpID='84872135457'):
        ## Scopus (Abtract) document example
        # Initialize document with Scopus ID.
        scp_doc = AbsDoc(scp_id = scpID)
        if scp_doc.read(self.client):
            print ("scp_doc.title: ", scp_doc.title)
            scp_doc.write()
        else:
            print ("Read document failed.")

    def readElsevierAuthor(self, authorID='7004367821'):
        ## Author example
        # Initialize author with uri
        my_auth = ElsAuthor(
                uri = 'https://api.elsevier.com/content/author/author_id/'+authorID)
        # Read author data, then write to disk
        if my_auth.read(self.client):
            print ("my_auth.full_name: ", my_auth.full_name)
            my_auth.write()
        else:
            print ("Read author failed.")

    def readElsevierAffiliation(self, affilID='60101411'):
        ## Affiliation example
        # Initialize affiliation with ID as string
        my_aff = ElsAffil(affil_id = affilID)
        if my_aff.read(self, self.client):
            print ("my_aff.name: ", my_aff.name)
            my_aff.write()
        else:
            print ("Read affiliation failed.")

    def readAllDocsFromAuthor(self, authorID='7004367821'):
        ## Read all documents for example author, then write to disk
        my_auth = ElsAuthor(
                uri = 'https://api.elsevier.com/content/author/author_id/'+authorID)
        if my_auth.read_docs(self.client):
            print ("my_auth.doc_list has " + str(len(my_auth.doc_list)) + " items.")
            my_auth.write_docs()
        else:
            print ("Read docs for author failed.")

    def readAllDocsFromAffiliation(self, affilID='60101411'):
        ## Read all documents for example affiliation, then write to disk
        my_aff = ElsAffil(affil_id = affilID)
        if my_aff.read_docs(client):
            print ("my_aff.doc_list has " + str(len(my_aff.doc_list)) + " items.")
            my_aff.write_docs()
        else:
            print ("Read docs for affiliation failed.")

    def elsevierSearchFromScopus(self):
        ## Initialize doc search object and execute search, retrieving all results
        doc_srch = ElsSearch('star+trek+vs+star+wars','scopus')
        doc_srch.execute(self.client, get_all = True)
        print ("doc_srch has", len(doc_srch.results), "results.")

    def elsevierSearchByAuthor(self):
        ## Initialize author search object and execute search
        auth_srch = ElsSearch('authlast(keuskamp)','author')
        auth_srch.execute(self.client)
        print ("auth_srch has", len(auth_srch.results), "results.")

    def elsevierSearchByAffiliation(self):
        ## Initialize affiliation search object and execute search
        aff_srch = ElsSearch('affil(amsterdam)','affiliation')
        aff_srch.execute(self.client)
        print ("aff_srch has", len(aff_srch.results), "results.")

def main():
    obj = ElsevierScopusSearch()
    obj.readFullDocWithPII('S1270963817323015')

if __name__ == "__main__":
    main()
