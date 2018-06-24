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
UnpublishedFieldSet = set(["author"])

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

class Article:
    def __init__(self, author="", title="", journal="", volume="", number="", year="", pages="", month="", note="", abstract=""):
        self.data = {"author"    :author,
                     "title"     :title,
                     "journal"   :journal,
                     "volume"    :volume,
                     "number"    :number,
                     "year"      :year,
                     "pages"     :pages,
                     "month"     :month,
                     "note"      :note,
                     "abstract"  :abstract}

class Book:
    def __init__(self):
        self.data = None
class Booklet:
    def __init__(self):
        self.data = None

class Conference:
    def __init__(self):
        self.data = None

class Inbook:
    def __init__(self):
        self.data = None

class Incollection:
    def __init__(self):
        self.data = None

class Inproceedings:
    def __init__(self):
        self.data = None

class Manual:
    def __init__(self):
        self.data = None

class Mastersthesis:
    def __init__(self):
        self.data = None

class Misc:
    def __init__(self):
        self.data = None

class Phdthesis:
    def __init__(self):
        self.data = None

class Proceedings:
    def __init__(self):
        self.data = None

class Techreport:
    def __init__(self):
        self.data = None

class Unpublished:
    def __init__(self):
        self.data = None
