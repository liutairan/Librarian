BibTeXTypes = set(['article', 'book', 'booklet', 'conference', 'inbook',
                   'incollection', 'inproceedings', 'manual', 'mastersthesis',
                   'misc', 'phdthesis', 'proceedings', 'techreport',
                   'unpublished'])

DatabaseReferenceStructure = ['ID', 'Title', 'Authors', 'Type', 'PubIn',
                              'Year', 'Labels', 'AddedTime']

# https://verbosus.com/bibtex-style-examples.html
ArticleFieldSet = set(["author", "title", "journal", "year", "number",
                        "pages", "month", "note", "volume", "abstract"])
BookFieldSet = set(["author", "title", "publisher", "year", "volume", "series",
                    "address", "edition", "month", "note", "isbn"])
BookletFieldSet = set(["author", "title", "howpublished", "address",
                       "month", "year", "note"])
ConferenceFieldSet = set(["author", "title", "conference", "volume", "number",
                          "year", "pages", "month", "note", "abstract"])
InbookFieldSet = set(["author", "title", "chapter", "pages", "publisher", "year",
                      "volume", "series", "address", "edition", "month", "note"])
IncollectionFieldSet = set(["author", "title", "booktitle", "publisher", "year",
                    "edition", "volume", "series", "chapter", "pages",
                    "address", "edition", "month", "note"])
InproceedingsFieldSet = set(["author", "title", "conference", "volume", "number",
                             "year", "pages", "month", "note", "abstract"])
ManualFieldSet = set(["author", "title", "organization", "address", "edition",
                      "month", "year", "note"])
MastersthesisFieldSet = set(["author", "title", "school", "year", "address",
                             "month", "note"])
MiscFieldSet = set(["author", "title", "howpublished", "month", "year", "note"])
PhdthesisFieldSet = set(["author", "title", "school", "year", "address",
                         "month", "note"])
ProceedingsFieldSet = set(["author", "title", "year", "editor", "volume",
                           "series", "address", "month", "organization",
                           "publisher", "note"])
TechreportFieldSet = set(["author", "title", "institution", "year", "number",
                          "address", "month", "note"])
UnpublishedFieldSet = set(["author", "title", "note", "month", "year"])

ReferenceStandardStructure = {'article':         ArticleFieldSet,
                              'book':            BookFieldSet,
                              'booklet':         BookletFieldSet,
                              'conference':      ConferenceFieldSet,
                              'inbook':          InbookFieldSet,
                              'incollection':    IncollectionFieldSet,
                              'inproceedings':   InproceedingsFieldSet,
                              'manual':          ManualFieldSet,
                              'mastersthesis':   MastersthesisFieldSet,
                              'misc':            MiscFieldSet,
                              'phdthesis':       PhdthesisFieldSet,
                              'proceedings':     ProceedingsFieldSet,
                              'techreport':      TechreportFieldSet,
                              'unpublished':     UnpublishedFieldSet
                             }
