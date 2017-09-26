from urllib2 import urlopen
from urllib2 import URLError, HTTPError
from bs4 import BeautifulSoup as Bs

def getHtml(url):
    try:
        html = urlopen(url)
    except (HTTPError,URLError) as e:
        return None
    try:
        bsObj = Bs(html.read(), "html.parser")
    except ArithmeticError as e:
        return None

    return bsObj

