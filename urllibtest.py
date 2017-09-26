from urllib2 import urlopen
from bs4 import BeautifulSoup as Bs
import getHtml
import re
import random
import datetime

random.seed(datetime.datetime.now())
def getLink(url):
    bsObj = getHtml.getHtml("https://en.wikipedia.org")
    data = bsObj.find("div", {"id":"content"}).findAll("a", href=re.compile("^(/wiki/)((?!:|\().)*$"))
    return data

links = getLink("/wiki/Kevin_Bacon")