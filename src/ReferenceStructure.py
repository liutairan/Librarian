BibTeXTypes = set(['article', 'book', 'booklet', 'conference', 'inbook',
                   'incollection', 'inproceedings', 'manual', 'mastersthesis',
                   'misc', 'phdthesis', 'proceedings', 'techreport',
                   'unpublished'])

DatabaseReferenceStructure = ['ID', 'Title', 'Authors', 'Type', 'PubIn',
                              'Year', 'Labels', 'AddedTime']

ArticleFieldSet = set(["author", "title", "journal", "volume", "number",
                       "year", "pages", "month", "note", "abstract"])
BookFieldSet = set(["author", "title", "volume", "number",
                    "year", "pages", "month", "note"])
BookletFieldSet = set(["author", "title", "volume", "number",
                       "year", "pages", "month", "note"])
ConferenceFieldSet = set(["author", "title", "conference", "volume", "number",
                          "year", "pages", "month", "note", "abstract"])
InbookFieldSet = set(["author", "title", "volume", "number",
                    "year", "pages", "month", "note"])
Incollection = set(["author"])
InproceedingsFieldSet = set(["author", "title", "conference", "volume", "number",
                             "year", "pages", "month", "note", "abstract"])
ManualFieldSet = set(["author"])
MastersthesisFieldSet = set(["author"])
MiscFieldSet = set(["author"])
PhdthesisFieldSet = set(["author"])
ProceedingsFieldSet = set(["author"])
TechreportFieldSet = set(["author"])
UnpublishedFieldSet = set(["author", "title", "note", "month", "year"])

ReferenceStandardStructure = {'article':         ArticleFieldSet,
                              'book':            BookFieldSet,
                              'booklet':         BookletFieldSet
                              'conference':      ConferenceFieldSet,
                              'inbook':          InbookFieldSet,
                              'inproceedings':   InproceedingsFieldSet,
                              'manual':          ManualFieldSet,
                              'mastersthesis':   MastersthesisFieldSet,
                              'misc':            MiscFieldSet,
                              'phdthesis':       PhdthesisFieldSet,
                              'proceedings':     ProceedingsFieldSet,
                              'techreport':      TechreportFieldSet,
                              'unpublished':     UnpublishedFieldSet
                             }
