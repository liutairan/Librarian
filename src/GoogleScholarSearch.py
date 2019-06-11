import os
import re
import sys
import warnings

from urllib.request import HTTPCookieProcessor, Request, build_opener
from urllib.parse import quote, unquote
from http.cookiejar import MozillaCookieJar

from bs4 import BeautifulSoup


unicode = str
encode = lambda s: unicode(s)

class GoogleScholarConfig:
    MaxNumPerPage = 10
    BaseSite = 'http://scholar.google.com'
    UserAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:42.0) Gecko/20100101 Firefox/42.0'

def main():
    pass

if __name__ == "__main__":
    main()
